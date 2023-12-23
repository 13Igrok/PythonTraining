import requests
from googlesearch import search

def get_proxy_urls():
    proxy_urls = []
    for j in search("site:txt best proxies list", num_results=50):
        response = requests.get(j)
        for line in response.text.split("\n"):
            if "proxy" in line:
                proxy_urls.append(line)
    return proxy_urls

def get_proxy_servers():
    proxy_urls = get_proxy_urls()
    proxy_servers = []
    for url in proxy_urls:
        try:
            ip = url.split(":")[0]
            port = url.split(":")[1]
            proxy_servers.append({"http": f"http://{ip}:{port}", "https": f"https://{ip}:{port}"})
        except Exception as e:
            print(f"Error: {e}")
    return proxy_servers

def test_proxy(proxy):
    try:
        response = requests.get("http://icanhazip.com", proxies=proxy, timeout=5)
        return response.text.replace("\n", "")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout: {e}")
        return None

def check_proxies():
    proxies = get_proxy_servers()
    for proxy in proxies:
        print(f"Checking proxy: {proxy}")
        ip = test_proxy(proxy)
        if ip:
            print(f"Working proxy: {proxy}, IP: {ip}")

check_proxies()