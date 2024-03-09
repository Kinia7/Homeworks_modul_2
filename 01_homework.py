from collections import UserDict
import re
from datetime import datetime
from abc import ABC, abstractmethod

class AddressBook(UserDict):
    def __init__(self):
        self.contacts = {}
        self.notebook = Notebook()

    def add_contact(self, name):
        self.contacts[name] = Contact(name)

class Contact():
    def __init__(self, name, phone=None, address=None, email=None, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.address = Address(address)
        self.email = Email(email)
        self.birthday = Birthday(birthday)
        
    def add_phone(self, phone):
        self.phone = Phone(phone)       
        
    def delete_phone(self, phone=None):
        self.phone = Phone(phone)   

    def change_phone(self, new_phone):
        self.phone = Phone(new_phone) 
        
    def add_email(self, email):
        self.email = Email(email)

    def remove_email(self, email=None):
        self.email = Email(email)
        
    def add_address(self, address):
        self.address = Address(address)

    def remove_address(self, address = None):
        self.address = Address(address)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    @property
    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today()
            birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d")
            upcoming_birthday_date = datetime(today.year, birthday_date.month, birthday_date.day)
            if today.date() == upcoming_birthday_date.date():
                return 0
            elif today > upcoming_birthday_date:
                upcoming_birthday_date = datetime(today.year + 1, birthday_date.month, birthday_date.day)
            delta = upcoming_birthday_date - today
            return delta.days + 1
        else:
            return None

class Field(ABC):
    def __init__(self, value = None):
        self.value = value

    @abstractmethod
    def validate(self):
        pass
    
    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.validate()

class Name(Field):
    def validate(self):
        if not self.value:
            raise ValueError("Name is a mandatory field and cannot be empty!")       
        self.value = self.value.lower()

class Phone(Field):
    def validate(self):
        if self.value:
            number = self.value.strip()
            if not number.isdigit() or len(number) != 9:
                raise ValueError("Number must be 9 digits long and contain digits only.")
            self.value = f"{number[:3]}-{number[3:6]}-{number[6:]}"

class Address(Field):
    def validate(self):
        if self.value:
            if len(self.value) > 56:
                raise ValueError("Address should not exceed 56 characters.")
            self.value = self.value.title()


class Email(Field): 
    def validate(self):
        if self.value:
            pattern_email = r"^([A-Za-z0-9]+|[A-Za-z0-9][A-Za-z0-9\.\_]+[A-Za-z0-9])@([A-Za-z0-9]+|[A-Za-z0-9\_\-]+[A-Za-z0-9])\.([a-z]{,3}|[a-z]{3}\.[a-z]{2})$"
            if not re.match(pattern_email, self.value):
                raise ValueError("Wrong email format!")

class Birthday(Field):
    def validate(self):
        pass

class Notebook(UserDict):
    num_of_notes = 0

    def add_note(self, note, tags):
        try:
            Notebook.num_of_notes += 1
            while True:
                if Notebook.num_of_notes in self.data.keys():
                    Notebook.num_of_notes += 1
                else:
                    break
            self.num_of_note = Notebook.num_of_notes
            self.data[self.num_of_note] = [Note(note).value, Tags(tags).value]
            return True
        
        except ValueError as e:
            print(e)
            return False
        
    def show_notes(self):
        width = 154
        all_notes = ''
        all_notes += "\n+" + "-" * width + "+\n"
        all_notes += '|{:^20}|{:^100}|{:^32}|\n'.format("NUMBER OF NOTE", "NOTE", "TAGS")
        all_notes += "+" + "-" * width + "+\n"
        for num_of_note, note_and_tags in self.data.items():
            note = note_and_tags[0]
            tags = note_and_tags[1]
            str_tags = ''
            for tag in tags:
                str_tags += f'{tag}; '
            all_notes += f'|{str(num_of_note):^20}|{str(note):^100}|{str_tags:^32}|\n'
        all_notes += "+" + "-" * width + "+"
        return all_notes
    
    def search_note_by_tags(self, searched_tags):
        width = 154
        finded_notes_data = []
        searched_tags = Tags(searched_tags).internal_value
        finded_notes = ''
        finded_notes += "\n+" + "-" * width + "+\n"
        finded_notes += '|{:^20}|{:^100}|{:^32}|\n'.format("NUMBER OF NOTE", "NOTE", "TAGS")
        finded_notes += "+" + "-" * width + "+\n"
        for num_of_note, note_and_tags in self.data.items():
            note = note_and_tags[0]
            tags = note_and_tags[1]
            
            if searched_tags <= tags:
                str_tags = ''
                for tag in tags:
                    str_tags += f'{tag}; '
                finded_notes_data.append(num_of_note)
                finded_notes += f'|{str(num_of_note):^20}|{str(note):^100}|{str_tags:^32}|\n'
        
        finded_notes += "+" + "-" * width + "+"
        if finded_notes_data == []:
            return f'Notes not find'
        else:
            return finded_notes
    
    def edit_note(self, num_of_note):
        if num_of_note not in str(self.data.keys()):
            print('Number of note doesn\'t exists')
            return False
        else:
            try:
                note = input('Enter new note text: ')
                tags = input("Enter new tags: ")
                self.data[int(num_of_note)] = [Note(note).internal_value, Tags(tags).internal_value]
                return True
            
            except ValueError as e:
                print(e)
                return False
            
    def remove_note(self, num_of_note):
        if num_of_note == 'all':
            Notebook.num_of_notes = 0
            self.data.clear()
            return True
    
        elif num_of_note not in str(self.data.keys()):
            print('Number of note doesn\'t exists')
            return False
        else:
            self.data.pop(int(num_of_note))
            return True

    def remove_all_notes(self):
        self.note = ''

    def change_notebook(self, note):
        self.note = Notebook(note).value
    
class Note(Field):
    def validate(self):
        if not self.value.strip():
            raise ValueError("Note must include any characters")

class Tags(Field):
    def validate(self):
        if not self.value.strip():
            raise ValueError("Tags cannot be empty.")
        tags = self.value.lower().split(';')
        self.value = [tag.strip() for tag in tags if tag.strip()]
