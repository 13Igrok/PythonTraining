import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот для работы с картинками. Отправь мне картинку, и я сохраню её.')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(f'Фото успешно сохранено как {file_name}!')

def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
