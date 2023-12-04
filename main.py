"""
Homework Assignment. Python Core. Module 11
For a description of the task, please refer to the README.md file
"""

from datetime import datetime
from collections import UserDict


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

'''
    def __init__(self):
        super().__init__()
        self.load_from_json("address_book.json")

    def __iter__(self):
        return AddressBookIterator(self)

    def add_record(self, record: Record):
        self.data[record.name.name] = record

    def pp(self):
        print(self.data)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None
    
    def find_phone_in_book(self, phone):
        for user, record in self.data.items():
            for phone_record in record.phones:
                if phone == phone_record.value:
                    return user
        return f"Phone {phone} is not found"

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
            return f"{name} has been deleted from the AddressBook"
        return f"{name} is not in the AddressBook"
      
    def load_from_json(self, filename):
        try:
            with open(filename, "r") as file_js:
                records_data = json.load(file_js)
                for name, record_data in records_data.items():
                    record = Record(record_data["name"])
                    lenght = range(len(record_data["phones"]))
                    for i in lenght: 
                        record.add_phone(record_data["phones"][i])
                    if record_data["birthday"] != "not set":
                        record.add_birthday(record_data["birthday"])
                    self.data[name] = record
        except FileNotFoundError:
            pass

    def save_to_json(self, filename):
        records_data = {name: record.to_dict() for name, record in self.data.items()}
        with open(filename, "w") as file_js:
            json.dump(records_data, file_js, indent=3)
            
    def find_data(self):
        search_string = input("Enter a search data: ")

        found_users = []

        for record in self.data.values():
            if search_string in record.name.name:
                found_users.append(record)

            for phone in record.phones:
                if search_string in phone.value:
                    found_users.append(record)

        if found_users:
            print("Found users:")
            for record in found_users:
                print(f"Name: {record.name.name}")
                print(f"Phones: {', '.join(phone.value for phone in record.phones)}")
                print(f"Birthday: {record.birthday}")
        else:
            print("This data is not found.") 

'''





if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення записів для перевірки
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_birthday("2010-11-10")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("2004-11-11")
    book.add_record(jane_record)

    alice_record = Record("Alice")
    alice_record.add_phone("5551112222")
    book.add_record(alice_record)

    bob_record = Record("Bob")
    bob_record.add_phone("9998887777")
    book.add_record(bob_record)

    # Перевірка виведення всіх записів у книзі
    print("All records in the address book:")
    for _, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    # Виведення імені запису John
    print("Name of the John's record:")
    print(john.name.name)

    # Виведення телефонів запису John
    print("Phones in the John's record:")
    for phone in john.phones:
        print(phone.value)

    # Перевірка кількості днів до наступного дня народження
    print("\nNumber of days until the next birthday:")
    for name, record in book.data.items():
        print(f"{name}: {record.days_to_bd()}")

    # Перевірка AddressBookIterator
    print("\nIterating through the address book using AddressBookIterator:")
    iterator = iter(AddressBookIterator(book, 2))
    for page in iterator:
        print("Page:")
        for record in page:
            print(record)


'''
def main():
    print("""
    List of Commands:
    1 - Show all records in the address book.
    2 - Show records in parts (paginated).
    3 - Find data in the address book by a search string.
    4 - Edit data for a specific record.
    5 - Add a new record to the address book.
    6 - Delete a specific record from the address book.
    7 - Save data in file
    hello - Display a welcome message.
    good bye, close, exit - Save the address book to a file and exit the program.
    """)
    
    book = AddressBook()

    try:
        while True:
            user_input = input(">>> ")
            if user_input == "hello":
                print(hello())
                
            elif user_input == "1":
                for _, record in book.data.items():
                    print(record)
                    
            elif user_input == "2":
                number = 0
                for page in book:
                    number += 1
                    print(f"Page {number}")
                    for record in page:
                        print(record)
                        
            elif user_input == "3":
                book.find_data()
                
            elif user_input == "4":
                name = input("Input name of the record to edit --> ")
                dataname = book.find(name)
                while dataname:
                    print("Choice command:\nfind phone\nedit phone\nremove phone\nback")
                    inp1 = input(">>> ")

                    if inp1 == "find phone":
                        phone_to_find = input("Enter the phone number to find:\n")
                        found_phone = dataname.find_phone(phone_to_find)
                        if found_phone:
                            print(f"Phone number of {dataname.name.value}: {found_phone.value}")
                        else:
                            print(f"Phone number not found for {dataname.name.value}")

                    elif inp1 == "edit phone":
                        old_ph = input("Enter the phone number you want to change:\n")
                        new_ph = input("Enter a new phone number:\n")
                        try:
                            dataname.edit_phone(old_ph, new_ph)
                            print(f"Phone number updated for {dataname.name.value}")
                        except ValueError:
                            print("Invalid input. Phone not updated.")

                    elif inp1 == "remove phone":
                        rem = input("Enter the phone number you want to delete:\n")
                        result = dataname.remove_phone(rem)
                        print(result)

                    elif inp1 == "back":
                        break

                    else:
                        print("Error command!")

            elif user_input == "5":
                name = input("Input new name --> ")
                name_record = Record(name)
                while True:
                    print("Choice command:\nadd phone\nadd bd\nback\nsave record")
                    inp = input(">>> ")
                    if inp == "add phone":
                        phone = input("Phone --> ")
                        try:
                            name_record.add_phone(phone)
                            print(f"Phone added for {name_record.name.name}\n")
                        except ValueError:
                            print("Invalid phone number. Phone not added.")

                    elif inp == "add bd":
                        bd = input("BD (Y-m-d) --> ")
                        name_record.add_birthday(bd)
                        print(f"Birthday added for {name_record.name.value}")

                    elif inp == "save record":
                        book.add_record(name_record)
                        print(f"Record saved for {name_record.name.value}")

                    elif inp == "back":
                        zap = input("Do you want to save data? (y): ")
                        if zap.lower() == "y":
                            book.add_record(name_record)
                            print(f"Record saved for {name_record.name.value}")
                            break
                        else:
                            break
                    else:
                        print("Error command!")

            elif user_input == "6":
                delet = input("Enter the name of the record you want to delete: ")
                result = book.delete(delet)
                print(result)
                
            elif user_input == "7":
               book.save_to_json("address_book.json") 
                
            elif user_input in ("good bye", "close", "exit"):
                book.save_to_json("address_book.json")
                print("Good bye!")
                break
            
            else:
                print("Error command!")
                 
    except Exception as e:
        book.save_to_json("address_book.json")
        return e
'''