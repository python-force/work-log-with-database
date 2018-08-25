import time
import os, sys
from collections import OrderedDict
from peewee import *

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

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()

def add_entry():
    """Hello Dude"""

def view_entries():
    """Hello Dude"""

def search_entries():
    """Hello Dude"""

menu = OrderedDict([
    ('1', add_entry),
    ('2', view_entries),
    ('3', search_entries),
])

# Script doesn't execute when imported
if __name__ == '__main__':
    # The script will keep running till the user is satisfied
    main_menu()

    print("Thank you and have a very safe and productive day. "
          "Work Safe. Work Smart.")
