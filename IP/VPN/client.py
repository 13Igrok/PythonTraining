#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

class WireGuardClient:
    def __init__(self, config_file):
        self.config_file = Path(config_file)
        self.interface = "wg0"
        
    def start_client(self):
        """Запуск клиента WireGuard"""
        subprocess.run(f"wg-quick up {self.config_file}", shell=True)
        
    def stop_client(self):
        """Остановка клиента WireGuard"""
        subprocess.run(f"wg-quick down {self.config_file}", shell=True)
        
    def show_status(self):
        """Показать статус подключения"""
        subprocess.run("wg show", shell=True)

if __name__ == "__main__":
    config_file = input("Введите путь к файлу конфигурации клиента: ")
    client = WireGuardClient(config_file)
    
    try:
        client.start_client()
        print("Клиент WireGuard запущен")
        client.show_status()
    except KeyboardInterrupt:
        print("\nОстанавливаем клиент...")
        client.stop_client()
        print("Клиент остановлен") 