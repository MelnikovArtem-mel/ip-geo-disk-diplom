import json
import requests
from settings import TOKEN
import os

class Ipify:
    def __init__(self, url):
        self.url = url
    def get_json(self):
        response = requests.get(self.url)
        data = response.json()
        return data['ip']
    def get_city(self, ip):
        response = requests.get(f'https://ipinfo.io/{ip}/geo')
        data = response.json()
        return data.get('city', 'Город не найден!')

class YandexDiskClient:
    def __init__(self, token):
        self.token = token
        self.base_url ='https://cloud-api.yandex.net/v1/disk/resources'
        self.headers = {
            'Authorization': f'OAuth {self.token}',
        }
    def create_folder(self, folder_name):
        params = {
            'path': folder_name
        }
        response = requests.put(self.base_url, headers=self.headers, params=params)
        if response.status_code in {200, 201}:
            print(f"Папка {folder_name} создана")
        elif response.status_code == 409:
            print(f"Папка {folder_name} уже существует")
        else:
            print(f"Ошибка: {response.status_code}")
    def upload_file(self, local_path, remote_path):
        params = {
            'path': remote_path,
            'overwrite': 'true'
        }
        response = requests.get(f'{self.base_url}/upload', headers=self.headers, params=params)
        url = response.json()['href']
        with open(local_path, 'rb') as f:
            put_response = requests.put(url, data=f)
            if put_response.status_code in {200, 201, 202}:
                print("Файл загружен")
            else:
                print(f"Ошибка загрузки: {put_response.status_code}")
FILENAME = 'result.json'
def main():
    my_ip = Ipify('https://api64.ipify.org?format=json')
    ip = my_ip.get_json()
    if not ip:
        print('Не удалось получить IP')
        return
    print(f'Мой IP: {ip}')
    city = my_ip.get_city(ip)
    print(f'Город: {city}')
    data = {
        'city': city,
        'ip': ip,
    }
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    myclient = YandexDiskClient(TOKEN)
    myclient.create_folder('/test')
    myclient.upload_file(FILENAME, '/test/result.json')
    os.remove(FILENAME)
    print(f'Локальный файл {FILENAME} удалён')

if __name__ == '__main__':
    main()



