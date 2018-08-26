import time
import os, sys
from collections import OrderedDict
import datetime
from peewee import *
import re

db = SqliteDatabase('catalogue.db')

class Employee(Model):
    pub_date = DateTimeField(default=datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d'))
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

    while choice != '3':
        clear_screen()
        for key, value in menu.items():
            if value == "Exit":
                print('{}) {}'.format(key, value))
            else:
                print('{}) {}'.format(key, value.__doc__))
        choice = input('What would you like to do?: ').lower().strip()

        if choice in menu and choice != "3":
            menu[choice]()


def search_main_menu():
    """Search Menu for the App"""
    choice = None

    while choice != '6':
        clear_screen()
        for key, value in search_menu.items():
            if value == "Go to Main Menu":
                print('{}) {}'.format(key, value))
            else:
                print('{}) {}'.format(key, value.__doc__))
        choice = input('What would you like to do?: ').lower().strip()

        if choice in search_menu and choice != "6":
            search_menu[choice]()

def search_by_date():
    """Search by Date"""
    while True:
        try:
            search_data = input("What date you looking for? "
                                "Format YYYY/MM/DD: ")
            search_data = datetime.datetime.strptime(search_data, '%Y/%m/%d')
        except ValueError:
            print("Date you specified is not valid, please try again.")
            continue
        else:
            break

    header = ["pub_date"]
    start_date = ""
    end_date = ""
    view_entries(header, search_data, start_date, end_date)

def search_by_date_range():
    """Search by Date Range"""
    while True:
        try:
            start_date = input("What is your starting date? "
                               "Format YYYY/MM/DD: ")
            start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
            end_date = input("What is your ending date? "
                             "Format YYYY/MM/DD: ")
            end_date = datetime.datetime.strptime(end_date, '%Y/%m/%d')
        except ValueError:
            print("Date you specified is not valid, please try again.")
            continue
        else:
            break

    header = ["pub_date"]
    search_data = ""
    view_entries(header, search_data, start_date, end_date)

def search_by_time_spent():
    """Search by Time Spent"""
    while True:
        try:
            search_data = int(input("What time you looking for?: "))
        except ValueError:
            print("Your selection is not a whole number, "
                  "please try again: ")
            continue
        else:
            break

    header = ["Time Spent"]
    start_date = ""
    end_date = ""
    view_entries(header, search_data, start_date, end_date)

def search_by_term():
    """Search by Term (Title, Notes)"""
    search_data = input("Enter a string you looking for: ")
    search_data = r'\b{0}\b'.format(search_data)
    header = ["Notes"]
    start_date = ""
    end_date = ""
    view_entries(header, search_data, start_date, end_date)

def search_by_name():
    """Search by Name"""
    search_data = input("Enter a string you looking for: ")
    search_data = r'\b{0}\b'.format(search_data)
    header = ["Name"]
    start_date = ""
    end_date = ""
    view_entries(header, search_data, start_date, end_date)


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


def view_entries(header, search_data, start_date, end_date):
    """View Records"""
    if header[0] == "Notes":
        all_records = Employee.select()
        found = []
        for record in all_records:
            found_record = re.search(search_data, record.task_name, re.I)
            if found_record:
                found.append(record)
            else:
                found_record = re.search(search_data, record.notes, re.I)
                if found_record:
                    found.append(record)
        all_records = found
    elif header[0] == "Name":
        all_records = Employee.select()
        found = []
        for record in all_records:
            found_record = re.match(search_data, record.name, re.I)
            if found_record:
                found.append(record)
        all_records = found
    elif header[0] == "Time Spent":
        all_records = Employee.select().where(Employee.time_spent == search_data).order_by(Employee.pub_date.desc())
    elif search_data == "" and start_date != "":
        all_records = Employee.select().where((Employee.pub_date >= start_date) & (Employee.pub_date <= end_date)).order_by(Employee.pub_date.desc())
    else:
        all_records = Employee.select().where(Employee.pub_date == search_data).order_by(Employee.pub_date.desc())
    step = 1
    for record in all_records:
        clear_screen()
        print(record.pub_date)
        print(record.name)
        print(record.task_name)
        print(record.time_spent)
        print(record.notes)
        if step == len(all_records):
            action = input("[D]elete, "
                           "[E]dit, "
                           "[R]eturn to the Menu ")
        else:
            action = input("[N]ext, "
                           "[D]elete, "
                           "[E]dit, "
                           "[R]eturn to the Menu ")
            step += 1
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
    clear_screen()
    search_main_menu()


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
    ('2', search_entries),
    ('3', "Exit"),
])

search_menu = OrderedDict([
    ('1', search_by_date_range),
    ('2', search_by_date),
    ('3', search_by_time_spent),
    ('4', search_by_name),
    ('5', search_by_term),
    ('6', "Go to Main Menu"),
])

# Script doesn't execute when imported
if __name__ == '__main__':
    # The script will keep running till the user is satisfied
    initialize()
    main_menu()

    print("Thank you and have a very safe and productive day. "
          "Work Safe. Work Smart.")
