import numpy as np
from collections import deque
import random
import time
from mineflayer import Bot  # Или другой API для взаимодействия с Minecraft

# Параметры обучения
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 10000
EPSILON = 1.0
EPSILON_DECAY = 0.9995
MIN_EPSILON = 0.01

# Простая среда для копания (упрощённая модель)
class MiningEnvironment:
    def __init__(self, bot):
        self.bot = bot
        self.block_map = {}  # Карта блоков вокруг бота
        self.last_position = None
        self.inventory_size = 0
        self.update_environment()
    
    def update_environment(self):
        """Обновляет информацию об окружающих блоках"""
        self.last_position = self.bot.entity.position
        # Здесь должна быть логика сканирования блоков вокруг бота
        # В упрощённой версии мы имитируем это
        self.block_map = self._simulate_blocks_around()
        self.inventory_size = len(self.bot.inventory.items())
    
    def _simulate_blocks_around(self):
        """Имитация блоков вокруг бота для демонстрации"""
        blocks = {}
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0:
                        continue
                    # Имитация разных типов блоков
                    block_type = random.choice(['dirt', 'stone', 'coal_ore', 'iron_ore', 'air'])
                    blocks[(dx, dy, dz)] = block_type
        return blocks
    
    def get_state(self):
        """Преобразует окружение в состояние для Q-обучения"""
        # Упрощённое представление состояния: тип блока перед ботом и заполненность инвентаря
        front_block = self.block_map.get((0, 0, 1), 'air')
        inventory_full = 1 if self.inventory_size >= 36 else 0  # Предполагаем 36 слотов
        
        # Кодируем состояние в числовой формат
        block_types = {'air': 0, 'dirt': 1, 'stone': 2, 'coal_ore': 3, 'iron_ore': 4}
        block_code = block_types.get(front_block, 0)
        
        return (block_code, inventory_full)
    
    def get_possible_actions(self):
        """Возвращает возможные действия"""
        return ['dig_forward', 'turn_left', 'turn_right', 'move_forward', 'move_back', 'idle']
    
    def perform_action(self, action):
        """Выполняет действие и возвращает награду"""
        reward = 0
        
        if action == 'dig_forward':
            front_block = self.block_map.get((0, 0, 1), 'air')
            if front_block != 'air':
                # Награда зависит от типа блока
                rewards = {'dirt': 1, 'stone': 2, 'coal_ore': 5, 'iron_ore': 10}
                reward = rewards.get(front_block, 0)
                self.bot.dig()  # В реальности нужно указать направление и блок
                self.inventory_size += 1
            else:
                reward = -1  # Штраф за копание воздуха
        elif action in ['turn_left', 'turn_right']:
            # Поворот не даёт награды, но и не штрафуется
            getattr(self.bot, action)(90)
        elif action in ['move_forward', 'move_back']:
            # Движение может привести к столкновению
            getattr(self.bot, action)()
            reward = -0.1  # Небольшой штраф за бесцельное движение
        
        # Обновляем окружение после действия
        self.update_environment()
        
        # Проверяем, заполнен ли инвентарь
        if self.inventory_size >= 36:
            reward += 20  # Большая награда за заполнение инвентаря
            return reward, True  # Эпизод завершён
        
        return reward, False

# Q-обучение с нейронной сетью (упрощённая версия)
class QLearningAgent:
    def __init__(self, env):
        self.env = env
        self.actions = env.get_possible_actions()
        self.q_table = {}
        self.epsilon = EPSILON
        
    def get_q_value(self, state, action):
        """Возвращает Q-значение для состояния и действия"""
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in self.actions}
        return self.q_table[state][action]
    
    def choose_action(self, state):
        """Выбирает действие с учётом стратегии epsilon-greedy"""
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = {a: self.get_q_value(state, a) for a in self.actions}
            return max(q_values, key=q_values.get)
    
    def learn(self, state, action, reward, next_state, done):
        """Обновляет Q-значения на основе опыта"""
        current_q = self.get_q_value(state, action)
        
        if done:
            max_next_q = 0
        else:
            max_next_q = max([self.get_q_value(next_state, a) for a in self.actions])
        
        # Формула Q-обучения
        new_q = current_q + LEARNING_RATE * (reward + DISCOUNT * max_next_q - current_q)
        self.q_table[state][action] = new_q
        
        # Уменьшаем epsilon
        if not done:
            self.epsilon = max(MIN_EPSILON, self.epsilon * EPSILON_DECAY)
    
    def save_model(self, filename):
        """Сохраняет модель (в данном случае Q-таблицу)"""
        import pickle
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load_model(self, filename):
        """Загружает модель"""
        import pickle
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

# Основной цикл обучения
def train_bot():
    # Создаём бота Minecraft (в реальности нужно указать параметры подключения)
    bot = Bot({'host': 'localhost', 'port': 25565, 'username': 'MiningBot'})
    
    # Инициализируем среду и агента
    env = MiningEnvironment(bot)
    agent = QLearningAgent(env)
    
    # Попробуем загрузить предыдущую модель
    try:
        agent.load_model('mining_bot_qtable.pkl')
        print("Загружена предыдущая модель")
    except:
        print("Начинаем обучение с нуля")
    
    # Цикл обучения
    for episode in range(EPISODES):
        env.update_environment()
        state = env.get_state()
        total_reward = 0
        done = False
        
        while not done:
            # Выбираем и выполняем действие
            action = agent.choose_action(state)
            reward, done = env.perform_action(action)
            next_state = env.get_state()
            
            # Обучаем агента
            agent.learn(state, action, reward, next_state, done)
            
            state = next_state
            total_reward += reward
            
            # Небольшая задержка для наблюдения (в реальности не нужно)
            time.sleep(0.1)
        
        print(f"Эпизод: {episode}, Награда: {total_reward}, Epsilon: {agent.epsilon:.2f}")
        
        # Периодически сохраняем модель
        if episode % 100 == 0:
            agent.save_model('mining_bot_qtable.pkl')
    
    # Сохраняем финальную модель
    agent.save_model('mining_bot_qtable_final.pkl')

if __name__ == "__main__":
    train_bot()