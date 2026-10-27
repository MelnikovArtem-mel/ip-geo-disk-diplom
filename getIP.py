import requests
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
def main():
    my_ip = Ipify('https://api64.ipify.org?format=json')
    ip = my_ip.get_json()
    if not ip:
        print('Не удалось получить IP')
        return
    print(f'Мой IP: {ip}')
    city = my_ip.get_city(ip)
    print(f'Город: {city}')
if __name__ == '__main__':
    main()


