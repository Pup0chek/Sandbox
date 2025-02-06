from enum import verify

import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# Отключаем предупреждения об SSL
requests.packages.urllib3.disable_warnings()

class CustomTLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False  # Отключаем проверку имени хоста
        context.verify_mode = ssl.CERT_NONE  # Отключаем проверку сертификата
        context.set_ciphers("DEFAULT:@SECLEVEL=1")  # Разрешаем слабые ключи DH
        kwargs['ssl_context'] = context
        super().init_poolmanager(*args, **kwargs)

# Создаём сессию с кастомным TLS-адаптером
session = requests.Session()
session.mount("https://", CustomTLSAdapter())

# Добавляем заголовки, чтобы сервер не блокировал Python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class Bypass:
    def __init__(self, url):
        self.url = url

    def methods_brute(self, method: str):
        """Проверка обхода через разные HTTP-методы"""
        try:
            match method:
                case 'POST':
                    response = session.post(self.url, headers=HEADERS, verify=False)
                case 'GET':
                    response = session.get(self.url, headers=HEADERS, verify=False)
                case 'PUT':
                    response = session.put(self.url, headers=HEADERS, verify=False)
                case 'PATCH':
                    response = session.patch(self.url, headers=HEADERS, verify=False)
                case _:
                    return [None, f"Неизвестный метод: {method}"]

            return [response.status_code, f'-X {method} {self.url}']
        except requests.exceptions.RequestException as e:
            return ["Ошибка", f'{method} запрос не удался: {str(e)}']

    def headers_brute(self):
        """Проверка обхода через подделку заголовков"""
        headers_list = [
            {"X-Originating-IP": "127.0.0.1"},
            {"X-Forwarded-For": "127.0.0.1"},
            {"X-Forwarded": "127.0.0.1"},
            {"Forwarded-For": "127.0.0.1"},
            {"X-Remote-IP": "127.0.0.1"},
            {"X-Remote-Addr": "127.0.0.1"},
            {"X-ProxyUser-Ip": "127.0.0.1"},
            {"X-Original-URL": "127.0.0.1"},
            {"Client-IP": "127.0.0.1"},
            {"True-Client-IP": "127.0.0.1"},
            {"Cluster-Client-IP": "127.0.0.1"},
            {"Host": "localhost"}
        ]

        results = []
        for header in headers_list:
            try:
                response = session.get(self.url, headers={**HEADERS, **header}, verify=False)
                results.append([response.status_code, f'{self.url} -H {str(header)[1:-1]}'])
            except requests.exceptions.RequestException as e:
                results.append(["Ошибка", f'Запрос с заголовком {header} не удался: {str(e)}'])

        return results
