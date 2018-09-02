from models import *
from classes import WorkLog

# Script doesn't execute when imported
if __name__ == '__main__':
    # The script will keep running till the user is satisfied
    initialize()
    WorkLog().main_menu()

    print("Thank you and have a very safe and productive day. "
          "Work Safe. Work Smart.")
