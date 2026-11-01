import json
import requests
from settings import TOKEN

class IpifyClient:
    def __init__(self, url):
        self.url = url
    def get_json(self):
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json()
        return data['ip']
class IpInfoClient:
    def __init__(self, url):
        self.url = url
    def get_city(self, ip):
        response = requests.get(f'{self.url}/{ip}/geo')
        response.raise_for_status()
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
    def upload_file(self, data_dict, remote_path):
        params = {
            'path': remote_path,
            'overwrite': 'true'
        }
        response = requests.get(f'{self.base_url}/upload', headers=self.headers, params=params)
        response.raise_for_status()
        url = response.json()['href']
        json_data = json.dumps(data_dict, ensure_ascii=False, indent=4)
        put_response = requests.put(url, data=json_data.encode('utf-8'))
        if put_response.status_code in {200, 201, 202}:
            print("Файл загружен")
        else:
            print(f"Ошибка загрузки: {put_response.status_code}")
def main():
    my_ip = IpifyClient('https://api64.ipify.org?format=json')
    ip = my_ip.get_json()
    if not ip:
        print('Не удалось получить IP')
        return
    print(f'Мой IP: {ip}')
    my_ip_city = IpInfoClient('https://ipinfo.io')
    city = my_ip_city.get_city(ip)
    print(f'Город: {city}')
    data = {
        'city': city,
        'ip': ip,
    }
    myclient = YandexDiskClient(TOKEN)
    myclient.create_folder('/test2')
    myclient.upload_file(data, '/test2/result.json')

if __name__ == '__main__':
    main()



