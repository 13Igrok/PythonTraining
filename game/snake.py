import random
import pygame
import math
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import json
import os
from datetime import datetime
import logging

# Настройка TensorFlow для оптимизации производительности
tf.config.threading.set_inter_op_parallelism_threads(2)
tf.config.threading.set_intra_op_parallelism_threads(2)
tf.config.set_soft_device_placement(True)

# Настройка логирования
logging.basicConfig(
    filename='bot_learning.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

pygame.init()

# Определение цветов
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)
orange = (255, 165, 0)
pink = (255, 192, 203)

# Цвета для ботов
bot_colors = [blue, yellow, white]

# Определение размеров экрана
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка игра')

clock = pygame.time.Clock()

snake_block = 10
initial_snake_speed = 15
snake_speed = initial_snake_speed

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 0.1  # Уменьшаем случайность
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        self.batch_size = 64
        self.train_every = 2  # Увеличиваем частоту обучения
        
    def _build_model(self):
        model = Sequential([
            Dense(64, input_shape=(self.state_size,), activation='relu'),  # Увеличиваем размер сети
            Dense(64, activation='relu'),
            Dense(self.action_size, activation='linear')
        ])
        model.compile(
            loss='mse',
            optimizer=Adam(learning_rate=self.learning_rate),
            metrics=['accuracy']
        )
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = np.reshape(state, [1, self.state_size])
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
            
        minibatch = random.sample(self.memory, batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.reshape(states, [batch_size, self.state_size])
        next_states = np.reshape(next_states, [batch_size, self.state_size])

        targets = rewards + self.gamma * (np.amax(self.target_model.predict(next_states, verbose=0), axis=1) * (1 - dones))
        target_f = self.model.predict(states, verbose=0)
        
        for i, action in enumerate(actions):
            target_f[i][action] = targets[i]
            
        self.model.train_on_batch(states, target_f)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class BotLogger:
    def __init__(self):
        self.log_file = 'bot_learning_data.json'
        self.error_log_file = 'bot_errors.json'
        self.learning_data = self.load_learning_data()
        self.error_data = self.load_error_data()
        
    def load_learning_data(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return {
            'games_played': 0,
            'best_score': 0,
            'average_score': 0,
            'total_score': 0,
            'learning_progress': [],
            'common_mistakes': {}
        }
    
    def load_error_data(self):
        if os.path.exists(self.error_log_file):
            with open(self.error_log_file, 'r') as f:
                return json.load(f)
        return {
            'collision_errors': {},
            'movement_errors': {},
            'decision_errors': {}
        }
    
    def save_learning_data(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.learning_data, f, indent=4)
    
    def save_error_data(self):
        with open(self.error_log_file, 'w') as f:
            json.dump(self.error_data, f, indent=4)
    
    def log_game_result(self, score, moves, mistakes):
        self.learning_data['games_played'] += 1
        self.learning_data['total_score'] += score
        self.learning_data['average_score'] = self.learning_data['total_score'] / self.learning_data['games_played']
        
        if score > self.learning_data['best_score']:
            self.learning_data['best_score'] = score
            logging.info(f"Новый рекорд: {score} очков")
        
        self.learning_data['learning_progress'].append({
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'moves': moves,
            'mistakes': mistakes
        })
        
        # Сохраняем только последние 100 игр
        if len(self.learning_data['learning_progress']) > 100:
            self.learning_data['learning_progress'] = self.learning_data['learning_progress'][-100:]
        
        self.save_learning_data()
    
    def log_error(self, error_type, state, action, reward):
        error_key = f"{state[0]}_{state[1]}_{state[2]}_{state[3]}"
        
        if error_type == 'collision':
            if error_key not in self.error_data['collision_errors']:
                self.error_data['collision_errors'][error_key] = []
            self.error_data['collision_errors'][error_key].append({
                'action': action,
                'reward': reward,
                'timestamp': datetime.now().isoformat()
            })
        
        elif error_type == 'movement':
            if error_key not in self.error_data['movement_errors']:
                self.error_data['movement_errors'][error_key] = []
            self.error_data['movement_errors'][error_key].append({
                'action': action,
                'reward': reward,
                'timestamp': datetime.now().isoformat()
            })
        
        elif error_type == 'decision':
            if error_key not in self.error_data['decision_errors']:
                self.error_data['decision_errors'][error_key] = []
            self.error_data['decision_errors'][error_key].append({
                'action': action,
                'reward': reward,
                'timestamp': datetime.now().isoformat()
            })
        
        self.save_error_data()
        logging.warning(f"Зафиксирована ошибка типа {error_type} в состоянии {state}")

    def analyze_mistakes(self):
        analysis = {
            'most_common_collision_states': [],
            'worst_decisions': [],
            'improvement_suggestions': []
        }
        
        # Анализ ошибок столкновений
        collision_counts = {}
        for state, errors in self.error_data['collision_errors'].items():
            collision_counts[state] = len(errors)
        
        if collision_counts:
            most_common = max(collision_counts.items(), key=lambda x: x[1])
            analysis['most_common_collision_states'].append({
                'state': most_common[0],
                'count': most_common[1]
            })
        
        # Анализ худших решений
        decision_rewards = {}
        for state, errors in self.error_data['decision_errors'].items():
            avg_reward = sum(e['reward'] for e in errors) / len(errors)
            decision_rewards[state] = avg_reward
        
        if decision_rewards:
            worst_decisions = sorted(decision_rewards.items(), key=lambda x: x[1])[:3]
            analysis['worst_decisions'].extend(worst_decisions)
        
        # Генерация рекомендаций
        if analysis['most_common_collision_states']:
            analysis['improvement_suggestions'].append(
                f"Избегайте состояний, ведущих к столкновениям в позиции {analysis['most_common_collision_states'][0]['state']}"
            )
        
        return analysis

class BotBrain:
    def __init__(self):
        self.state_size = 5
        self.action_size = 4
        self.agent = DQNAgent(self.state_size, self.action_size)
        self.score = 0
        self.best_score = 0
        self.logger = BotLogger()
        self.moves_count = 0
        self.mistakes_count = 0
        self.last_train_step = 0
        
    def get_state(self, snake_head, food, snake_list):
        state = np.array([
            snake_head[0] / dis_width,
            snake_head[1] / dis_height,
            food[0] / dis_width,
            food[1] / dis_height,
            len(snake_list) / 100
        ], dtype=np.float32)
        return state
    
    def get_reward(self, snake_head, food, snake_list, done, score):
        reward = 0
        if done:
            reward = -100
            self.logger.log_error('collision', 
                                [snake_head[0], snake_head[1], food[0], food[1]], 
                                'collision', 
                                reward)
            self.mistakes_count += 1
        elif snake_head[0] == food[0] and snake_head[1] == food[1]:
            self.score += 1
            if self.score > self.best_score:
                self.best_score = self.score
                reward = 100
            else:
                reward = 50
        else:
            dx = snake_head[0] - food[0]
            dy = snake_head[1] - food[1]
            current_dist = math.sqrt(dx*dx + dy*dy)
            reward = -current_dist / (dis_width + dis_height) + 0.1
            
            if reward < -0.5:
                self.logger.log_error('decision',
                                    [snake_head[0], snake_head[1], food[0], food[1]],
                                    'move_away',
                                    reward)
                self.mistakes_count += 1
        
        return reward
    
    def choose_action(self, state):
        action = self.agent.act(state)
        self.moves_count += 1
        return action
    
    def remember(self, state, action, reward, next_state, done):
        self.agent.remember(state, action, reward, next_state, done)
        if self.moves_count - self.last_train_step >= self.agent.train_every:
            self.replay()
            self.last_train_step = self.moves_count
    
    def replay(self):
        self.agent.replay(self.agent.batch_size)
        if self.score % 10 == 0:
            self.agent.update_target_model()
            analysis = self.logger.analyze_mistakes()
            logging.info(f"Анализ ошибок: {analysis}")

class Snake:
    def __init__(self, x, y, color, is_bot=False):
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.length = 1
        self.color = color
        self.is_bot = is_bot
        self.score = 0
        self.best_score = 0
        if is_bot:
            self.brain = BotBrain()
            self.brain.logger = BotLogger()

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        snake_head = [self.x, self.y]
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.length:
            del self.snake_list[0]

    def draw(self):
        for x in self.snake_list:
            pygame.draw.rect(dis, self.color, [x[0], x[1], snake_block, snake_block])

    def check_collision(self):
        if (self.x >= dis_width or self.x < 0 or 
            self.y >= dis_height or self.y < 0):
            return True
        for x in self.snake_list[:-1]:
            if x == [self.x, self.y]:
                return True
        return False

class Food:
    def __init__(self):
        self.items = []
        self.max_items = 100
        self.add_food(2)  # Начальное количество еды
        
    def add_food(self, count=1):
        for _ in range(count):
            if len(self.items) < self.max_items:
                x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                self.items.append([x, y])
    
    def remove_food(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
    
    def draw(self):
        for food in self.items:
            pygame.draw.rect(dis, green, [food[0], food[1], snake_block, snake_block])

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def bot_move(x1, y1, foodx, foody, x1_change, y1_change, bot_brain, snake_list):
    state = bot_brain.get_state([x1, y1], [foodx, foody], snake_list)
    action = bot_brain.choose_action(state)
    
    current_state = state
    
    if action == 0 and x1_change != snake_block:  # Влево
        x1_change, y1_change = -snake_block, 0
    elif action == 1 and x1_change != -snake_block:  # Вправо
        x1_change, y1_change = snake_block, 0
    elif action == 2 and y1_change != snake_block:  # Вверх
        x1_change, y1_change = 0, -snake_block
    elif action == 3 and y1_change != -snake_block:  # Вниз
        x1_change, y1_change = 0, snake_block
    
    next_state = bot_brain.get_state([x1 + x1_change, y1 + y1_change], [foodx, foody], snake_list)
    reward = bot_brain.get_reward([x1 + x1_change, y1 + y1_change], [foodx, foody], snake_list, False, bot_brain.score)
    
    bot_brain.remember(current_state, action, reward, next_state, False)
    bot_brain.replay()
    
    return x1_change, y1_change

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width/2, dis_height/2))
    dis.blit(mesg, text_rect)


def gameLoop():
    game_over = False
    game_close = False
    
    # Создаем ботов
    bots = []
    num_bots = 3
    
    # Создаем ботов в разных позициях
    for i in range(num_bots):
        x = random.randrange(0, dis_width - snake_block, snake_block)
        y = random.randrange(0, dis_height - snake_block, snake_block)
        bots.append(Snake(x, y, bot_colors[i], True))
    
    # Создаем еду
    food = Food()

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("Нажмите Q-Выход или C-Играть снова", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Движение ботов
        for bot in bots:
            if bot.is_bot:
                # Находим ближайшую еду для бота
                closest_food = None
                min_dist = float('inf')
                for i, food_item in enumerate(food.items):
                    dist = calculate_distance(bot.x, bot.y, food_item[0], food_item[1])
                    if dist < min_dist:
                        min_dist = dist
                        closest_food = (food_item[0], food_item[1])
                
                if closest_food:
                    bot.x_change, bot.y_change = bot_move(
                        bot.x, bot.y, closest_food[0], closest_food[1], 
                        bot.x_change, bot.y_change, 
                        bot.brain, bot.snake_list
                    )

        # Обновление позиций
        for bot in bots:
            bot.move()

        # Проверка столкновений
        for bot in bots:
            if bot.check_collision():
                if bot.is_bot:
                    bot.brain.logger.log_game_result(bot.score, bot.brain.moves_count, bot.brain.mistakes_count)
                    x = random.randrange(0, dis_width - snake_block, snake_block)
                    y = random.randrange(0, dis_height - snake_block, snake_block)
                    bot.x = x
                    bot.y = y
                    bot.x_change = 0
                    bot.y_change = 0
                    bot.snake_list = []
                    bot.length = 1
                    bot.score = 0

        # Проверка поедания еды
        for bot in bots:
            for i, food_item in enumerate(food.items):
                if bot.x == food_item[0] and bot.y == food_item[1]:
                    food.remove_food(i)
                    bot.length += 1
                    bot.score += 1
                    if bot.is_bot:
                        bot.brain.score = bot.score
                    food.add_food(2)  # Добавляем 2 новые еды
                    break

        # Отрисовка
        dis.fill(blue)
        food.draw()
        
        for bot in bots:
            bot.draw()
        
        # Отображение счета
        for i, bot in enumerate(bots):
            score_text = f"Бот {i+1}: {bot.score}"
            score_surface = score_font.render(score_text, True, bot.color)
            dis.blit(score_surface, [10, 10 + i * 40])
        
        # Отображение количества еды
        food_text = f"Еда: {len(food.items)}"
        food_surface = score_font.render(food_text, True, white)
        dis.blit(food_surface, [10, 130])
        
        pygame.display.update()
        clock.tick(snake_speed * 2)  # Увеличиваем скорость игры в 2 раза

    pygame.quit()

gameLoop()
