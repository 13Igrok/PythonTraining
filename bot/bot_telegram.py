import os
import logging
import glob
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info('Пользователь запустил бота')
    await update.message.reply_text(
        'Привет! Я бот для работы с картинками.\n'
        'Доступные команды:\n'
        '/start - показать это сообщение\n'
        '/search - показать все доступные изображения\n'
        'Просто отправьте мне картинку, и я сохраню её.'
    )

async def search_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info('Пользователь запросил поиск изображений')
    try:
        # Получаем список всех изображений
        images = glob.glob("images/*.jpg")
        
        if not images:
            await update.message.reply_text('Нет сохраненных изображений.')
            return
            
        # Отправляем сообщение с количеством найденных изображений
        await update.message.reply_text(f'Найдено {len(images)} изображений:')
        
        # Отправляем каждое изображение
        for image_path in images:
            with open(image_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
                
    except Exception as e:
        logger.error(f'Ошибка при поиске изображений: {e}')
        await update.message.reply_text('Ошибка при поиске изображений')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info('Пользователь отправил фото')
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
    except Exception as e:
        logger.error(f'Ошибка при сохранении фото: {e}')
        await update.message.reply_text('Ошибка при сохранении фото')

def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search_images))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем бота
    logger.info('Бот запущен...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
