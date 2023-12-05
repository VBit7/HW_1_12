"""
Homework Assignment. Python Core. Module 12
For a description of the task, please refer to the README.md file
"""

from datetime import datetime, timedelta
from collections import UserDict

import random
import json


class Field:
    """
    Базовий клас для полів запису.
    Буде батьківським для всіх полів.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Клас для зберігання імені контакту.
    Обов'язкове поле.
    """
    def __init__(self, name):
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name


class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Має валідацію формату (10 цифр).
    Необов'язкове поле з телефоном. Один запис Record може містити декілька.
    """
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_phone):
        if self.check_number(new_phone):
            self._value = new_phone
        else:
            raise ValueError("Invalid phone: phone should consist of 10 digits only")

    @staticmethod
    def check_number(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()


class Birthday(Field):
    """
    Клас "Дні народження"
    """
    def __init__(self, birthday):
        self._birthday = None
        self.birthday = birthday

    form = '%Y-%m-%d'

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, new_bd):
        self._birthday = datetime.strptime(new_bd, self.form)

    def __str__(self):
        if self._birthday:
            return self._birthday.strftime(self.form)
        else:
            return "Birthday not set!"


class Record:
    """
    Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name
    """
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else birthday

    # Додавання телефонів
    def add_phone(self, phone_number):
        phone = phone_number
        self.phones.append(Phone(phone))

    # Додавання дня народження
    def add_birthday(self, bd):
        self.birthday = Birthday(bd)
        return self.birthday

    # Повертає кількість днів до наступного дня народження
    def days_to_bd(self):
        if not self.birthday:
            return "Birthday not set"

        now = datetime.now()
        bd = self.birthday.birthday
        certain_year = now.year
        bd = bd.replace(year=certain_year)
        if bd < now:
            bd = bd.replace(year=certain_year + 1)
        days_to_bdd = (bd.date() - now.date()).days

        return f"{days_to_bdd} days before the birthday"

    # Видалення телефонів
    def remove_phone(self, phone):
        for el in self.phones:
            if el.value == phone:
                self.phones.remove(el)
                return f"Phone {phone} has been deleted"
        return f"Phone {phone} is not found"

    # Редагування телефонів
    def edit_phone(self, old_phone, new_phone):
        for ind, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[ind] = Phone(new_phone)
                return f"Phone number has been updated for {self.name.name}"
        raise ValueError

    # Пошук телефону
    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone
        return None

    # Перетворює дані об'єкту у формат словника
    def to_dict(self):
        return {
            "name": self.name.name,
            "phones": [str(phone) for phone in self.phones],
            "birthday": str(self.birthday) if self.birthday else "not set"
        }

    def __str__(self):
        phone_numbers = ', '.join(str(phone) for phone in self.phones)
        birthday = self.birthday if self.birthday else "not set"

        return f'{self.name.name} - {phone_numbers}, birthday - {birthday}'


class AddressBookIterator:
    """
    Генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.
    """
    def __init__(self, address_book, per_page=10):
        self.address_book = address_book
        self.keys = list(address_book.data.keys())
        self.per_page = per_page
        self.current_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        start_idx = self.current_page * self.per_page
        end_idx = (self.current_page + 1) * self.per_page

        if start_idx >= len(self.keys):
            raise StopIteration

        page_keys = self.keys[start_idx:end_idx]
        page_records = [self.address_book.data[key] for key in page_keys]

        self.current_page += 1

        return page_records


class AddressBook(UserDict):
    """
    Клас для зберігання та управління записами.
    Успадковується від UserDict, та містить логіку пошуку за записами до цього класу
    """

    def __init__(self):
        super().__init__()
        self.load_from_json("address_book.json")

    # Додавання записів
    def add_record(self, record: Record):
        self.data[record.name.name] = record

    # Пошук записів за іменем
    def find(self, name):
        return self.data.get(name, None)

    # Видалення записів за іменем
    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
            return f"{name} has been deleted from the AddressBook"
        return f"{name} is not in the AddressBook"

    # Відновлення адресної книги з диска
    def load_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                records_data = json.load(file)

                for name, data in records_data.items():
                    record = Record(data["name"])
                    lenght = range(len(data["phones"]))

                    for i in lenght:
                        record.add_phone(data["phones"][i])

                    if data["birthday"] != "not set":
                        record.add_birthday(data["birthday"])

                    self.data[name] = record

        except FileNotFoundError:
            pass

    # Збереження адресної книги на диск
    def save_to_json(self, filename):
        records_data = {name: record.to_dict() for name, record in self.data.items()}
        with open(filename, "w") as file:
            json.dump(records_data, file, indent=3)

    # Здійснює пошук в адресній книзі за ім'ям користувача або номером телефону.
    # Підтримує пошук за частиною імені або номеру телефону.
    def find_data_in_book(self, search_string):
        found_users = []

        for record in self.data.values():
            if search_string in record.name.name:
                found_users.append(record)

            for phone in record.phones:
                if search_string in phone.value:
                    found_users.append(record)

        if found_users:
            print("Found users:\n")
            for record in found_users:
                print(f"Name: {record.name.name}")
                print(f"Phones: {', '.join(phone.value for phone in record.phones)}")
                print(f"Birthday: {record.birthday}\n")
        else:
            print("This data is not found.")


# Генерація рандомної дати народження
def generate_random_birthdate(start_date='1970-01-01', end_date='2000-12-31', date_format='%Y-%m-%d'):
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)

    random_days = random.randint(0, (end_date - start_date).days)
    random_birthdate = start_date + timedelta(days=random_days)

    return random_birthdate.strftime(date_format)


if __name__ == "__main__":
    # Створення нової адресної книги
    # Якщо файл address_book.json існує, він автоматично буде завантажений
    book = AddressBook()

    # Додаємо запис в адресну книгу з рандомними іменем, номером телефону та датою народження
    user_number = random.randint(100, 999)
    data_record = Record(f'User-{user_number}')
    phone_number = ''.join(map(str, [random.randint(0, 9) for _ in range(10)]))
    data_record.add_phone(phone_number)
    data_record.add_birthday(generate_random_birthdate())
    book.add_record(data_record)

    # # Пошук в адресній книзі по імені користувача
    # print("Search by username:")
    # book.find_data_in_book("John")
    # # Пошук в адресній книзі по номеру телефона
    # print("Search by phone number:")
    # book.find_data_in_book("0987654321")

    # Пошук в адресній книзі по частині імені користувача
    print("Search by partial username")
    book.find_data_in_book("Jo")
    # Пошук в адресній книзі по частині номеру телефона
    print("Search by partial phone number")
    book.find_data_in_book("098765")

    # Зберігаємо адресну книгу в файл
    book.save_to_json("address_book.json")

    print("Good bye!")
