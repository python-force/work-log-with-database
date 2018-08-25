import time
import os, sys
from collections import OrderedDict
import datetime
from peewee import *

db = SqliteDatabase('catalogue.db')

class Employee(Model):
    pub_date = DateTimeField(default=datetime.datetime.now)
    name = CharField(max_length=50)
    task_name = CharField(max_length=50)
    time_spent = IntegerField()
    notes = TextField()

    class Meta:
        database = db

def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Employee], safe=True)

def clear_screen():
    """
    Clear screen
    :return:
    """
    if os.system == "nt":
        os.system('cls')
    else:
        os.system('clear')

def main_menu():
    """Main Menu for the App"""
    choice = None

    while choice != '4':
        clear_screen()
        for key, value in menu.items():
            if value == "Exit":
                print('{}) {}'.format(key, value))
            else:
                print('{}) {}'.format(key, value.__doc__))
        choice = input('What would you like to do?: ').lower().strip()

        if choice in menu and choice != "4":
            menu[choice]()

def add_entry():
    """Add a new record"""
    clear_screen()
    while True:
        task_date = input("Enter a date: ")
        try:
            datetime.datetime.strptime(task_date, '%Y/%m/%d')
        except ValueError:
            print("Date you specified is not valid, please try again.")
            continue
        else:
            task_title = input("Enter a title: ")
            while True:
                try:
                    task_time_spent = int(input("Enter time spent: "))
                except ValueError:
                    print("Your selection is not a number, please try again: ")
                    continue
                if task_time_spent < 0:
                    print("Sorry, your response must not be negative.")
                    continue
                else:
                    task_notes = input("Enter a notes: ")
                    break
            break


def view_entries():
    """View Records"""

def search_entries():
    """Search Records"""

menu = OrderedDict([
    ('1', add_entry),
    ('2', view_entries),
    ('3', search_entries),
    ('4', "Exit"),
])

# Script doesn't execute when imported
if __name__ == '__main__':
    # The script will keep running till the user is satisfied
    initialize()
    main_menu()

    print("Thank you and have a very safe and productive day. "
          "Work Safe. Work Smart.")
