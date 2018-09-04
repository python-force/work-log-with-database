import os
import re
import datetime

from models import Employee
from collections import OrderedDict


class WorkLog:

    def clear_screen(self):
        """
        Clear screen
        :return:
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        """Main Menu for the App"""
        choice = None

        while choice != '3':
            self.clear_screen()
            for key, value in self.menu.items():
                if value == "Exit":
                    print('{}) {}'.format(key, value))
                else:
                    print('{}) {}'.format(key, value.__doc__))
            choice = input('What would you like to do?: ').lower().strip()

            if choice in self.menu and choice != "3":
                self.menu[choice](self)

    def search_main_menu(self):
        """Search Menu for the App"""
        choice = None

        while choice != '6':
            self.clear_screen()
            for key, value in self.search_menu.items():
                if value == "Go to Main Menu":
                    print('{}) {}'.format(key, value))
                else:
                    print('{}) {}'.format(key, value.__doc__))
            choice = input('What would you like to do?: ').lower().strip()

            if choice in self.search_menu and choice != "6":
                self.search_menu[choice](self)

    def search_by_date(self):
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
        self.view_entries(header, search_data, start_date, end_date)

    def search_by_date_range(self):
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
        self.view_entries(header, search_data, start_date, end_date)

    def search_by_time_spent(self):
        """Search by Time Spent"""
        while True:
            try:
                search_data = int(input("What time you looking for?: "))
            except ValueError:
                print("Your selection is not a whole number, please try again: ")
                continue
            else:
                break

        header = ["Time Spent"]
        start_date = ""
        end_date = ""
        self.view_entries(header, search_data, start_date, end_date)

    def search_by_term(self):
        """Search by Term (Title, Notes)"""
        search_data = input("Enter a string you looking for: ")
        search_data = r'\b{0}\b'.format(search_data)
        header = ["Notes"]
        start_date = ""
        end_date = ""
        self.view_entries(header, search_data, start_date, end_date)

    def search_by_name(self):
        """Search by Name"""
        search_data = input("Enter a string you looking for: ")
        search_data = r'\b{0}\b'.format(search_data)
        header = ["Name"]
        start_date = ""
        end_date = ""
        self.view_entries(header, search_data, start_date, end_date)

    def add_entry(self):
        """Add a new record"""
        self.clear_screen()
        employee_name = input("Enter the name: ")
        task_title = input("Enter a title: ")
        while True:
            try:
                task_time_spent = int(input("Enter time spent: "))
                if task_time_spent < 0:
                    print("Sorry, your response must not be negative.")
                    continue
            except ValueError:
                print("Your selection is not a number, please try again: ")
                continue
            else:
                task_notes = input("Enter a notes: ")
                break
        Employee.create(name=employee_name,
                        task_name=task_title,
                        time_spent=task_time_spent,
                        notes=task_notes)

    def name_view_entries(self, all_records, search_data):
        self.clear_screen()
        count = 1
        action = None
        all_records_dict = {}
        for record in all_records:
            all_records_dict[count] = record
            count += 1

        for key, value in all_records_dict.items():
            print(str(key) + ". " + value.name)

        while action is None:
            while True:
                try:
                    action = int(input("Please choose which " + (search_data[2:])[:-2] + ":"))
                    if action < 0:
                        print("Sorry, your response must not be negative.")
                        continue
                    elif action not in all_records_dict.keys():
                        print("Sorry, that many " + (search_data[2:])[:-2] + "s do not exist, please try again")
                        continue
                except ValueError:
                    print("Your selection is not a whole number, please try again: ")
                    continue
                else:
                    break

        for key, value in all_records_dict.items():
            if int(key) == int(action):
                return([value])

    def view_entries(self, header, search_data, start_date, end_date):
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
                found_record = re.search(search_data, record.name, re.I)
                if found_record:
                    found.append(record)
            all_records = found
            if len(all_records) > 1:
                all_records = self.name_view_entries(all_records, search_data)

        elif header[0] == "Time Spent":
            all_records = Employee.select().where(
                Employee.time_spent == search_data).order_by(Employee.pub_date.desc())
        elif search_data == "" and start_date != "":
            all_records = Employee.select().where(
                (Employee.pub_date >= start_date) &
                (Employee.pub_date <= end_date)).order_by(
                Employee.pub_date.desc())
        else:
            all_records = Employee.select().where(
                Employee.pub_date == search_data).order_by(Employee.pub_date.desc())
        step = 1
        for record in all_records:
            self.clear_screen()
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
                self.clear_screen()
                continue
            elif action == "d":
                self.delete(record)
            elif action == "e":
                self.edit_record(record.id)
            elif action == "r":
                break

    def search_entries(self):
        """Search Records"""
        self.clear_screen()
        self.search_main_menu()

    def delete(self, record):
        """Delete Record"""
        self.clear_screen()
        if input("Are you sure you would like to delete " + record.task_name + " ? ").lower() == "y":
            record.delete_instance()

    def edit_record(self, record_id):
        """Edit Record"""
        self.clear_screen()
        record = Employee.get(Employee.id == record_id)
        if input("Are you sure you would like to update " + record.task_name + " ? ").lower() == "y":
            print("Name is currently set to: " + record.name)
            record.name = input("Enter the name: ")
            print("Title is currently set to: " + record.task_name)
            record.task_name = input("Enter a title: ")
            while True:
                try:
                    print("Time Spent is currently set to: " + str(record.time_spent))
                    record.time_spent = int(input("Enter time spent: "))
                    if record.time_spent < 0:
                        print("Sorry, your response must not be negative.")
                        continue
                except ValueError:
                    print("Your selection is not a number, please try again: ")
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
