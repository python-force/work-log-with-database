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
    employee_name = input("Enter the name: ")
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
    Employee.create(name=employee_name, task_name=task_title, time_spent=task_time_spent, notes=task_notes)


def view_entries():
    """View Records"""
    clear_screen()
    all_records = Employee.select().order_by(Employee.pub_date.desc())
    for record in all_records:
        print(record.pub_date)
        print(record.name)
        print(record.task_name)
        print(record.time_spent)
        print(record.notes)
        action = input("[N]ext, "
                       "[D]elete, "
                       "[E]dit, "
                       "[R]eturn to the Menu ")
        action = action.lower()
        if action == "n":
            clear_screen()
            continue
        elif action == "d":
            delete(record)
        elif action == "e":
            edit_record(record.id)
        elif action == "r":
            break

def search_entries():
    """Search Records"""

def delete(record):
    """Delete Record"""
    clear_screen()
    if input("Are you sure you would like to delete " + record.task_name + " ? ").lower() == "y":
        record.delete_instance()

def edit_record(record_id):
    """Edit Record"""
    clear_screen()
    record = Employee.get(Employee.id==record_id)
    if input("Are you sure you would like to update " + record.task_name + " ? ").lower() == "y":
        print("Name is currently set to: " + record.name)
        record.name = input("Enter the name: ")
        print("Title is currently set to: " + record.task_name)
        record.task_name = input("Enter a title: ")
        while True:
            try:
                print("Time Spent is currently set to: " + str(record.time_spent))
                record.time_spent = int(input("Enter time spent: "))
            except ValueError:
                print("Your selection is not a number, please try again: ")
                continue
            if record.time_spent < 0:
                print("Sorry, your response must not be negative.")
                continue
            else:
                print("Notes are currently set to: " + record.notes)
                record.notes = input("Enter a notes: ")
                break
        record.save()

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
