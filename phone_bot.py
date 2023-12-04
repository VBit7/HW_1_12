def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "KeyError: Enter user name."
        except ValueError:
            return "ValueError: Give me name and phone please."
        except IndexError:
            return "IndexError: Invalid input. Please try again."
    
    return wrapper


contacts = {}


@input_error
def hello(params):
    return "How can I help you?"


@input_error
def add(params):
    
    name, phone = params
    contacts[name] = phone

    return f"Contact {name} with phone {phone} added."


@input_error
def change(params):
    return "change"


@input_error
def phone(params):
    return "phone"


@input_error
def show(params):
    return "show all"


def help(params):

    help_msg = """
    Possible commands:
        hello                       - responds with "How can I help you?"
        add name phone              - saves a new contact
                                        name    - contact's name
                                        phone   - phone number, separated by a space
        change name phone           - updates the phone number of an existing contact
                                        name    - contact's name
                                        phone   - new phone number, separated by a space
        phone name                  - outputs the phone number for the specified contact
                                        name    - name of the contact whose number needs to be shown
        show all                    - displays all saved contacts with phone numbers
        good bye | close | exit     - any of these commands will terminate the bot's operation
        help                        - displays this text
    """

    if len(params) != 0:
        if params[0] in ["ua", "ukr"]:
            help_msg = """
    Можливі команди:
        hello                       - відповідає "How can I help you?"
        add name phone              - зберігає новий контакт
                                        name     - ім'я контакту
                                        phone    - номер телефону, обов'язково через пробіл
        change name phone           - зберігає новий номер телефону існуючого контакту
                                        name     - ім'я контакту
                                        phone    - номер телефону, обов'язково через пробіл
        phone name                  - виводить номер телефону для зазначеного контакту
                                        name     - ім'я контакту, чий номер треба показати
        show all                    - виводить всі збереженні контакти з номерами телефонів
        good bye | close | exit     - по будь-якій з цих команд бот завершує свою роботу
        help                        - виводить цей текст
    """
    return help_msg


commands = {
    "hello": hello,
    "add": add,
    "change": change,
    "phone": phone,
    "show": show,
    "help": help,
}


def main():
    
    while True:
        user_input = input("Enter a command: ").lower().strip()

        if user_input in ["good bye", "close", "exit", "."]:
            break

        params = user_input.split(" ")

        while "" in params:
            params.remove("")
        
        if params[0] in commands:
            print(params)
            response = commands[params[0]](params[1:])
            print(response)
        else:
            print("Unknown command. Type 'help' to see available commands.")
    
    print("Good bye!")

    return None


if __name__ == "__main__":
    main()



