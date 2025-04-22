import requests
import re
import json
import socket
from bs4 import BeautifulSoup
import phonenumbers
from urllib.parse import quote
import time

"""
  _____ _______ ______ _____  _____  
 |  ___|__   __|  ____|  __ \|  __ \ 
 | |__   _| |  | |__  | |  | | |__) |
 |  __| | | |  |  __| | |  | |  _  / 
 | |____| | |  | |____| |__| | | \ \ 
 |______|_|_|  |______|_____/|_|  \_\
                                     
 OSINT Tool by FazDox (GitHub: Fazic12)
"""

def get_ip_info(ip_address):
    """Получение информации об IP-адресе"""
    try:
        # Проверка валидности IP
        socket.inet_aton(ip_address)
        
        print(f"\n[+] Поиск информации для IP: {ip_address}")
        
        # Проверка через ip-api.com
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
        data = response.json()
        
        if data.get('status') == 'success':
            print("\n=== Географическая информация ===")
            print(f"Страна: {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})")
            print(f"Регион: {data.get('regionName', 'N/A')} ({data.get('region', 'N/A')})")
            print(f"Город: {data.get('city', 'N/A')}")
            print(f"Район: {data.get('district', 'N/A')}")
            print(f"Почтовый индекс: {data.get('zip', 'N/A')}")
            print(f"Координаты: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
            print(f"Часовой пояс: {data.get('timezone', 'N/A')}")
            
            print("\n=== Сетевая информация ===")
            print(f"Провайдер: {data.get('isp', 'N/A')}")
            print(f"Организация: {data.get('org', 'N/A')}")
            print(f"AS номер: {data.get('as', 'N/A')}")
            print(f"AS имя: {data.get('asname', 'N/A')}")
            print(f"Обратный DNS: {data.get('reverse', 'N/A')}")
            
            print("\n=== Техническая информация ===")
            print(f"Мобильное соединение: {'Да' if data.get('mobile') else 'Нет'}")
            print(f"Прокси/VPN: {'Да' if data.get('proxy') else 'Нет'}")
            print(f"Хостинг: {'Да' if data.get('hosting') else 'Нет'}")
        else:
            print(f"Ошибка: {data.get('message', 'Неизвестная ошибка')}")
            
    except socket.error:
        print("Ошибка: Неверный формат IP-адреса")

def check_vk_by_phone(phone_number):
    """Проверка номера телефона во ВКонтакте"""
    try:
        # Форматирование номера телефона
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            print("Ошибка: Неверный формат номера телефона")
            return
            
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        print(f"\n[+] Поиск во ВКонтакте для номера: {formatted_number}")
        
        # Создание сессии
        session = requests.Session()
        
        # Получение страницы входа
        response = session.get("https://vk.com")
        if response.status_code != 200:
            print("Ошибка: Не удалось загрузить страницу ВКонтакте")
            return
            
        # Попытка найти пользователя по номеру телефона
        response = session.get(f"https://vk.com/phone/{formatted_number}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Поиск информации о пользователе
            profile_link = soup.find('a', {'href': re.compile(r'/id\d+')})
            
            if profile_link:
                user_id = profile_link['href']
                user_name = profile_link.get_text(strip=True)
                print(f"\n[+] Найден профиль ВКонтакте:")
                print(f"Имя: {user_name}")
                print(f"Ссылка: https://vk.com{user_id}")
            else:
                print("\n[-] Профиль ВКонтакте не найден или скрыт настройками приватности")
        else:
            print("\n[-] Ошибка при поиске профиля")
            
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def check_whatsapp(phone_number):
    """Проверка наличия номера в WhatsApp"""
    try:
        # Форматирование номера телефона
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            print("Ошибка: Неверный формат номера телефона")
            return
            
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        print(f"\n[+] Проверка WhatsApp для номера: {formatted_number}")
        
        # Создание сессии
        session = requests.Session()
        
        # Получение страницы WhatsApp
        response = session.get("https://web.whatsapp.com/")
        if response.status_code != 200:
            print("Ошибка: Не удалось загрузить страницу WhatsApp")
            return
            
        # Проверка номера через API WhatsApp
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = session.get(
            f"https://web.whatsapp.com/v3/existence/{formatted_number}?in=null&_={int(time.time()*1000)}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print("\n[+] Номер зарегистрирован в WhatsApp")
                print(f"Ссылка для чата: https://wa.me/{formatted_number}")
            else:
                print("\n[-] Номер не зарегистрирован в WhatsApp или неверный формат")
        else:
            print("\n[-] Ошибка при проверке номера в WhatsApp")
            
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def main():
    print("""
  _____ _______ ______ _____  _____  
 |  ___|__   __|  ____|  __ \|  __ \ 
 | |__   _| |  | |__  | |  | | |__) |
 |  __| | | |  |  __| | |  | |  _  / 
 | |____| | |  | |____| |__| | | \ \ 
 |______|_|_|  |______|_____/|_|  \_\
                                     
 OSINT Tool by FazDox (GitHub: Fazic12)
    """)
    
    while True:
        print("\nМеню:")
        print("1. Поиск информации по IP-адресу")
        print("2. Поиск профиля ВКонтакте по номеру телефона")
        print("3. Проверить номер в WhatsApp")
        print("4. Выход")
        
        choice = input("\nВыберите действие (1-4): ")
        
        if choice == '1':
            ip = input("Введите IP-адрес: ").strip()
            get_ip_info(ip)
        elif choice == '2':
            phone = input("Введите номер телефона (с кодом страны): ").strip()
            check_vk_by_phone(phone)
        elif choice == '3':
            phone = input("Введите номер телефона (с кодом страны): ").strip()
            check_whatsapp(phone)
        elif choice == '4':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 4.")

if __name__ == "__main__":
    main()
