import os
import logging
import glob
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import NetworkError, TimedOut
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Проверка наличия токена
if not TOKEN:
    logger.error("Токен бота не найден в переменных окружения!")
    raise ValueError("Токен бота не найден в переменных окружения!")

# Список разрешенных пользователей (замените на реальные ID)
ALLOWED_USERS = {
    123456789,  # Пример ID пользователя
}

def is_user_allowed(user_id: int) -> bool:
    """Проверяет, имеет ли пользователь доступ к боту"""
    return user_id in ALLOWED_USERS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        logger.warning(f"Неавторизованный доступ от пользователя {user_id}")
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return

    logger.info(f'Пользователь {user_id} запустил бота')
    await update.message.reply_text(
        'Привет! Я бот для работы с картинками.\n'
        'Используйте команду /help для просмотра всех доступных команд.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        logger.warning(f"Неавторизованный доступ от пользователя {user_id}")
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return

    logger.info(f'Пользователь {user_id} запросил помощь')
    help_text = (
        '📚 Доступные команды:\n\n'
        '/start - Начать работу с ботом\n'
        '/help - Показать это сообщение\n'
        '/search - Показать все сохраненные изображения\n\n'
        '📸 Как использовать бот:\n'
        '1. Отправьте мне любое изображение, и я сохраню его\n'
        '2. Используйте команду /search для просмотра всех сохраненных изображений\n'
        '3. Только авторизованные пользователи могут использовать бота'
    )
    await update.message.reply_text(help_text)

async def search_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        logger.warning(f"Неавторизованный доступ от пользователя {user_id}")
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return

    logger.info(f'Пользователь {user_id} запросил поиск изображений')
    try:
        # Получаем список всех изображений
        images = glob.glob("images/*.jpg")
        
        if not images:
            await update.message.reply_text('Нет сохраненных изображений.')
            return
            
        # Отправляем сообщение с количеством найденных изображений
        await update.message.reply_text(f'Найдено {len(images)} изображений:')
        
        # Отправляем каждое изображение с задержкой
        for image_path in images:
            try:
                with open(image_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        timeout=60
                    )
                await asyncio.sleep(3)
            except (NetworkError, TimedOut) as e:
                logger.error(f'Ошибка сети при отправке изображения {image_path}: {e}')
                await update.message.reply_text(f'Ошибка при отправке изображения {image_path}. Попробуйте позже.')
            except Exception as e:
                logger.error(f'Ошибка при отправке изображения {image_path}: {e}')
                await update.message.reply_text(f'Ошибка при отправке изображения {image_path}')
                
    except Exception as e:
        logger.error(f'Ошибка при поиске изображений: {e}')
        await update.message.reply_text('Ошибка при поиске изображений')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        logger.warning(f"Неавторизованный доступ от пользователя {user_id}")
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return

    logger.info(f'Пользователь {user_id} отправил фото')
    try:
        # Получаем фото с наилучшим качеством
        photo = update.message.photo[-1]
        
        # Загружаем фото
        file = await context.bot.get_file(photo.file_id)
        
        # Генерируем уникальное имя файла
        file_name = f"images/{photo.file_id}.jpg"
        
        # Создаем директорию для сохранения, если её нет
        os.makedirs("images", exist_ok=True)
        
        # Скачиваем и сохраняем файл
        await file.download_to_drive(file_name)
        logger.info(f'Фото успешно сохранено как {file_name}!')
        await update.message.reply_text(f'Фото успешно сохранено как {file_name}!')
    except (NetworkError, TimedOut) as e:
        logger.error(f'Ошибка сети при сохранении фото: {e}')
        await update.message.reply_text('Ошибка сети при сохранении фото. Попробуйте позже.')
    except Exception as e:
        logger.error(f'Ошибка при сохранении фото: {e}')
        await update.message.reply_text('Ошибка при сохранении фото')

async def main():
    # Настройки прокси (если нужно)
    proxy_url = None  # Замените на ваш прокси, если нужно
    # proxy_url = 'http://proxy.example.com:8080'
    
    # Создаем приложение с настройками подключения
    application = (
        Application.builder()
        .token(TOKEN)
        .proxy_url(proxy_url)
        .build()
    )

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_images))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем бота с обработкой ошибок
    logger.info('Бот запущен...')
    try:
        await application.initialize()
        await application.start()
        await application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            read_timeout=60,
            write_timeout=60,
            connect_timeout=60,
            pool_timeout=60
        )
    except (NetworkError, TimedOut) as e:
        logger.error(f'Ошибка сети: {e}')
        # Пробуем переподключиться через 5 секунд
        await asyncio.sleep(5)
        await main()
    except Exception as e:
        logger.error(f'Неожиданная ошибка: {e}')
    finally:
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
