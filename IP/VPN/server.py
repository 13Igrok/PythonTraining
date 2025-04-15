#!/usr/bin/env python3
import subprocess
import os
import json
from pathlib import Path

class WireGuardServer:
    def __init__(self, interface="wg0", port=51820):
        self.interface = interface
        self.port = port
        self.config_dir = Path("/etc/wireguard")
        self.config_file = self.config_dir / f"{interface}.conf"
        
    def generate_keys(self):
        """Генерация ключей для сервера"""
        private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
        public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).decode().strip()
        return private_key, public_key
        
    def create_server_config(self):
        """Создание конфигурации сервера"""
        private_key, public_key = self.generate_keys()
        
        config = f"""[Interface]
PrivateKey = {private_key}
Address = 10.0.0.1/24
ListenPort = {self.port}
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
"""
        
        # Создаем директорию если её нет
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Записываем конфигурацию
        with open(self.config_file, 'w') as f:
            f.write(config)
            
        # Устанавливаем правильные права
        os.chmod(self.config_file, 0o600)
        
        return public_key
        
    def start_server(self):
        """Запуск сервера WireGuard"""
        subprocess.run(f"wg-quick up {self.interface}", shell=True)
        
    def stop_server(self):
        """Остановка сервера WireGuard"""
        subprocess.run(f"wg-quick down {self.interface}", shell=True)
        
    def create_client_config(self, client_name):
        """Создание конфигурации для нового клиента"""
        client_private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
        client_public_key = subprocess.check_output(f"echo {client_private_key} | wg pubkey", shell=True).decode().strip()
        
        # Читаем публичный ключ сервера
        with open(self.config_file, 'r') as f:
            server_config = f.read()
            server_public_key = server_config.split('PrivateKey = ')[1].split('\n')[0]
            server_public_key = subprocess.check_output(f"echo {server_public_key} | wg pubkey", shell=True).decode().strip()
        
        # Генерируем IP для клиента
        client_ip = f"10.0.0.{len(os.listdir(self.config_dir)) + 1}/32"
        
        # Создаем конфигурацию клиента
        client_config = f"""[Interface]
PrivateKey = {client_private_key}
Address = {client_ip}
DNS = 8.8.8.8

[Peer]
PublicKey = {server_public_key}
AllowedIPs = 0.0.0.0/0
Endpoint = YOUR_SERVER_IP:{self.port}
PersistentKeepalive = 25
"""
        
        # Сохраняем конфигурацию клиента
        client_config_file = Path(f"{client_name}.conf")
        with open(client_config_file, 'w') as f:
            f.write(client_config)
            
        # Добавляем клиента в конфигурацию сервера
        with open(self.config_file, 'a') as f:
            f.write(f"\n[Peer]\nPublicKey = {client_public_key}\nAllowedIPs = {client_ip}\n")
            
        return client_config_file

if __name__ == "__main__":
    server = WireGuardServer()
    server_public_key = server.create_server_config()
    print(f"Сервер настроен. Публичный ключ сервера: {server_public_key}")
    
    # Создаем конфигурацию для нового клиента
    client_name = input("Введите имя нового клиента: ")
    client_config_file = server.create_client_config(client_name)
    print(f"Конфигурация клиента сохранена в файле: {client_config_file}")
    
    # Запускаем сервер
    server.start_server()
    print("Сервер WireGuard запущен")
