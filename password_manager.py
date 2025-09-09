from cryptography.fernet import Fernet
import secrets
import string
import os
from colorama import init, Fore, Style

# Ініціалізація colorama для кольорового виведення в консолі
init()

def generate_key():
    # Генерація та збереження ключа шифрування.
    if not os.path.exists("key.key"):
        print(f"{Fore.YELLOW}Генеруємо новий ключ шифрування...{Style.RESET_ALL}")
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        print(f"{Fore.GREEN}Ключ успішно збережено у key.key!{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}Ключ уже існує, використовуємо наявний.{Style.RESET_ALL}")

def load_key():
    # Завантаження ключа шифрування з файлу.
    try:
        with open("key.key", "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Помилка: Файл ключа (key.key) не знайдено!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Спочатку згенеруйте ключ.{Style.RESET_ALL}")
        exit(1)

def generate_password(length=12):
    # Генерація випадковий пароль заданої довжини.
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def view_passwords(fernet):
    # Виведення збережених паролів.
    try:
        with open('passwords.txt', 'r', encoding='utf-8') as f:
            if os.path.getsize('passwords.txt') == 0:
                print(f"{Fore.YELLOW}Файл паролів порожній.{Style.RESET_ALL}")
                return
            print(f"\n{Fore.CYAN}{'='*40}\nСписок збережених паролів:\n{'='*40}{Style.RESET_ALL}")
            for line in f:
                data = line.rstrip()
                try:
                    user, passw = data.split("|")
                    decrypted_pass = fernet.decrypt(passw.encode()).decode()
                    print(f"{Fore.GREEN}Обліковий запис: {Style.RESET_ALL}{user}")
                    print(f"{Fore.GREEN}Пароль: {Style.RESET_ALL}{decrypted_pass}")
                    print(f"{Fore.CYAN}{'—'*40}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Помилка розшифрування для {user}: {e}{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}Файл паролів (passwords.txt) не знайдено!{Style.RESET_ALL}")

def add_password(fernet):
    #Додавання нового пароля до файлу.
    name = input(f"{Fore.CYAN}Введіть назву облікового запису: {Style.RESET_ALL}")
    if not name.strip():
        print(f"{Fore.RED}Назва облікового запису не може бути порожньою!{Style.RESET_ALL}")
        return

    print(f"{Fore.YELLOW}Бажаєте згенерувати пароль автоматично? (т/н): {Style.RESET_ALL}", end="")
    gen_choice = input().lower()
    if gen_choice == 'т':
        pwd = generate_password()
        print(f"{Fore.GREEN}Згенеровано пароль: {pwd}{Style.RESET_ALL}")
    else:
        pwd = input(f"{Fore.CYAN}Введіть пароль: {Style.RESET_ALL}")
        if not pwd.strip():
            print(f"{Fore.RED}Пароль не може бути порожнім!{Style.RESET_ALL}")
            return

    try:
        with open('passwords.txt', 'a', encoding='utf-8') as f:
            f.write(f"{name}|{fernet.encrypt(pwd.encode()).decode()}\n")
        print(f"{Fore.GREEN}Пароль успішно додано для {name}!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Помилка при збереженні пароля: {e}{Style.RESET_ALL}")

def main():
    print(f"{Fore.BLUE}{'='*40}\nВітаємо у менеджері паролів! \n{'='*40}{Style.RESET_ALL}")

    # Генерація або завантаження ключа
    generate_key()
    key = load_key()
    fernet = Fernet(key)

    while True:
        print(f"\n{Fore.CYAN}Виберіть дію:{Style.RESET_ALL}")
        print(f"1. Переглянути збережені паролі (введіть: перегляд)")
        print(f"2. Додати новий пароль (введіть: додати)")
        print(f"3. Вийти (введіть: в)")
        mode = input(f"{Fore.YELLOW}Ваш вибір: {Style.RESET_ALL}").lower()

        if mode == "в":
            print(f"{Fore.BLUE}Дякуємо за використання менеджера паролів!{Style.RESET_ALL}")
            break
        elif mode == "перегляд":
            view_passwords(fernet)
        elif mode == "додати":
            add_password(fernet)
        else:
            print(f"{Fore.RED}Невірна команда. Спробуйте ще раз.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()