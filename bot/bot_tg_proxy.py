import subprocess
import time
import sys
import os
from proxy import ProxyManager

def run_bot_with_proxy():
    proxy_manager = ProxyManager()
    
    while True:
        try:
            # Получаем новый прокси
            proxy = proxy_manager.get_proxy()
            if not proxy:
                print("Не удалось получить прокси. Ожидание обновления...")
                time.sleep(60)
                continue

            # Формируем команду для запуска бота с прокси
            proxy_str = f"{proxy['http']}"
            env = os.environ.copy()
            env['HTTPS_PROXY'] = proxy_str
            env['HTTP_PROXY'] = proxy_str

            print(f"Запуск бота через прокси: {proxy_str}")
            
            # Запускаем бота
            process = subprocess.Popen(
                [sys.executable, 'bot_telegram.py'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'  # Заменяем недопустимые символы
            )

            # Ожидаем завершения процесса
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print(f"Бот завершился с ошибкой. Код возврата: {process.returncode}")
                if stderr:
                    try:
                        print(f"Ошибка: {stderr}")
                    except UnicodeDecodeError:
                        print("Ошибка: Не удалось декодировать вывод ошибки")
            
            print("Перезапуск бота через 5 секунд...")
            time.sleep(5)

        except KeyboardInterrupt:
            print("\nЗавершение работы...")
            break
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    run_bot_with_proxy()
