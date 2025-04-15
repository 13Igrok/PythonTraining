import requests
import json
from datetime import datetime
import os
import time
from typing import Optional

# Список стран для исключения
EXCLUDED_COUNTRIES = ['Russia', 'Belarus', 'Ukraine']
PROXY_FILE = 'proxy_list.txt'

class ProxyManager:
    def __init__(self):
        self.current_proxy = None
        self.proxy_list = []
        self.last_update = 0
        self.update_interval = 300  # 5 минут

    def get_proxy(self) -> Optional[dict]:
        current_time = time.time()
        if current_time - self.last_update > self.update_interval or not self.proxy_list:
            self.update_proxy_list()
        
        if self.proxy_list:
            self.current_proxy = self.proxy_list.pop(0)
            return self.current_proxy
        return None

    def update_proxy_list(self):
        try:
            # Здесь можно добавить API для получения прокси
            # Например, через requests.get('https://api.proxy-provider.com/proxies')
            # Для примера используем тестовые прокси
            self.proxy_list = [
                {
                    'http': 'http://proxy1.example.com:8080',
                    'https': 'http://proxy1.example.com:8080'
                },
                {
                    'http': 'http://proxy2.example.com:8080',
                    'https': 'http://proxy2.example.com:8080'
                }
            ]
            self.last_update = time.time()
        except Exception as e:
            print(f"Ошибка при обновлении списка прокси: {e}")

    def get_current_proxy(self) -> Optional[dict]:
        return self.current_proxy

def load_existing_proxies():
    """
    Загрузка существующих прокси из файла
    """
    if not os.path.exists(PROXY_FILE):
        return []
    
    existing_proxies = []
    try:
        with open(PROXY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.split('#')
                    proxy_str = parts[0].strip()
                    protocol, address = proxy_str.split('://')
                    ip, port = address.split(':')
                    country = parts[1].split('(')[0].strip()
                    uptime = float(parts[1].split('uptime:')[1].split('%')[0].strip())
                    
                    existing_proxies.append({
                        'ip': ip,
                        'port': port,
                        'protocol': protocol,
                        'country': country,
                        'uptime': uptime
                    })
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
    return existing_proxies

def test_proxy(proxy):
    """
    Проверка работоспособности прокси
    """
    try:
        proxy_url = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']}"
        response = requests.get(
            'http://icanhazip.com',
            proxies={proxy['protocol']: proxy_url},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def get_proxies_from_api():
    """
    Получение списка прокси с API
    """
    try:
        # Используем бесплатный API для получения прокси
        response = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=100&page=1&sort_by=lastChecked&sort_type=desc')
        if response.status_code == 200:
            return response.json()['data']
        return []
    except Exception as e:
        print(f"Ошибка при получении прокси: {e}")
        return []

def filter_proxies(proxies):
    """
    Фильтрация прокси по странам
    """
    filtered_proxies = []
    for proxy in proxies:
        if proxy.get('country') not in EXCLUDED_COUNTRIES:
            proxy_data = {
                'ip': proxy.get('ip'),
                'port': proxy.get('port'),
                'protocol': proxy.get('protocols', ['http'])[0],
                'country': proxy.get('country'),
                'uptime': proxy.get('uptime', 0)
            }
            filtered_proxies.append(proxy_data)
    return filtered_proxies

def save_proxies_to_file(proxies):
    """
    Сохранение прокси в файл
    """
    with open(PROXY_FILE, 'w', encoding='utf-8') as f:
        for proxy in proxies:
            proxy_str = f"{proxy['protocol']}://{proxy['ip']}:{proxy['port']} # {proxy['country']} (uptime: {proxy['uptime']}%)\n"
            f.write(proxy_str)
    
    print(f"Сохранено {len(proxies)} прокси в файл {PROXY_FILE}")

def main():
    print("Начинаем обновление списка прокси...")
    
    # Загружаем существующие прокси
    existing_proxies = load_existing_proxies()
    print(f"Загружено {len(existing_proxies)} существующих прокси")
    
    # Проверяем работоспособность существующих прокси
    working_proxies = []
    for proxy in existing_proxies:
        if test_proxy(proxy):
            working_proxies.append(proxy)
    
    print(f"Рабочих прокси из существующих: {len(working_proxies)}")
    
    # Получаем новые прокси
    new_proxies = get_proxies_from_api()
    if not new_proxies:
        print("Не удалось получить новые прокси")
        return
    
    print(f"Получено {len(new_proxies)} новых прокси")
    filtered_new_proxies = filter_proxies(new_proxies)
    print(f"После фильтрации осталось {len(filtered_new_proxies)} новых прокси")
    
    # Объединяем существующие рабочие прокси с новыми
    all_proxies = working_proxies + filtered_new_proxies
    
    # Удаляем дубликаты
    unique_proxies = []
    seen = set()
    for proxy in all_proxies:
        proxy_key = (proxy['ip'], proxy['port'])
        if proxy_key not in seen:
            seen.add(proxy_key)
            unique_proxies.append(proxy)
    
    print(f"Всего уникальных прокси: {len(unique_proxies)}")
    
    if unique_proxies:
        save_proxies_to_file(unique_proxies)
    else:
        print("Нет подходящих прокси для сохранения")

if __name__ == "__main__":
    main()