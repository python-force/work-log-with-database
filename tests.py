import datetime
import io
import unittest
from unittest.mock import patch
from unittest import mock
from models import Employee

from classes import WorkLog


class WorkLogTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Prepare Name DB Testing"""
        cls.bob_all_records = Employee.select().where(Employee.name.contains("Bob"))

    def setUp(self):
        self.work_log = WorkLog()

    def test_clear_screen(self):
        """
        Checks clear screen is being ran
        """
        # mock.path takes the normal os.system() command and over-rides it
        # then we are able to call assertions to see if it ran.

        # It also lets us test the clear() function without having to
        # worry about what os.system will do.
        with mock.patch('os.system') as mock_clear_screen:
            # We need to run the command in order to see if anything
            # was called
            self.work_log.clear_screen()

            # Check that the os.system command was indeed called
            mock_clear_screen.assert_called()

    @patch('classes.WorkLog.clear_screen')
    # We don't care about getting a variable for this patch, and
    # just want .clear_screen to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_main_menu_text_output(self, *args):
        """
        Checks to see if main_menu text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['3']
        with patch('builtins.input', side_effect=user_input):
            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.main_menu()

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "1) Add a new record\n2) Search Records\n3) Exit\n"
        )

    @patch('classes.WorkLog.clear_screen')
    # We don't care about getting a variable for this patch, and
    # just want .clear_screen to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_search_main_menu_text_output(self, *args):
        """
        Checks to see if search_main_menu text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['6', '3']
        with patch('builtins.input', side_effect=user_input):
            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.search_main_menu()

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "1) Search by Date Range\n2) Search by Date\n3) Search by Time Spent\n4) Search by Name\n5) Search by Term (Title, Notes)\n6) Go to Main Menu\n"
        )

    def test_search_by_term(self):
        """Checks to see if search_by_term calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['hello', 'ignored_second_value']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):

            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.view_entries') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.search_by_term()

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called_with(["Notes"], "\\bhello\\b", "", "")

    def test_search_by_date(self):
        """Checks to see if search_by_date calls the correct method"""
        # We can do the same thing here
        user_input = ['2018/04/04']
        with patch('builtins.input', side_effect=user_input):
            with patch('classes.WorkLog.view_entries') as view_entry_patch:
                self.work_log.search_by_date()

        entry_date = datetime.datetime(2018, 4, 4)
        view_entry_patch.assert_called_with(["pub_date"], entry_date, "", "")

    # Instead of using a with command you could add the patch as a decorator
    @patch('classes.WorkLog.view_entries')
    # patch will pass itself into the function as an argument, so you will
    # need to catch it
    def test_search_by_date_value_error_checker(self, view_entry_patch):
        """
        Checks to see if search_by_date calls the correct method,
        along with casing a temporary ValueError
        """
        # With a bad input for the first input() call the except ValueError
        # block will be triggered
        user_input = ['bad input', '2018/04/04']
        with patch('builtins.input', side_effect=user_input):
            self.work_log.search_by_date()

        entry_date = datetime.datetime(2018, 4, 4)
        view_entry_patch.assert_called_once_with(
            ["pub_date"], entry_date, "", ""
        )

    @patch('classes.WorkLog.view_entries')
    # We don't care about getting a variable for this patch, and
    # just want .view_entries to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_search_by_date_value_error_text_output(self, *args):
        """
        Checks to see if search_by_date's ValueError text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['bad input', '2018/04/04']
        with patch('builtins.input', side_effect=user_input):

            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.search_by_date()

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "Date you specified is not valid, please try again.\n"
        )

    def test_by_time_spent(self):
        """Checks to see if search_by_time_spent calls the correct method"""

        user_input = ['5']
        with patch('builtins.input', side_effect=user_input):
            with patch('classes.WorkLog.view_entries') as view_entry_patch:
                self.work_log.search_by_time_spent()

        view_entry_patch.assert_called_with(["Time Spent"], 5, "", "")

    # Instead of using a with command you could add the patch as a decorator
    @patch('classes.WorkLog.view_entries')
    # patch will pass itself into the function as an argument, so you will
    # need to catch it
    def test_by_time_spent_value_error_checker(self, view_entry_patch):
        """
        Checks to see if search_by_tiem_spent calls the correct method,
        along with casing a temporary ValueError
        """
        # With a bad input for the first input() call the except ValueError
        # block will be triggered
        user_input = ['bad input', '5']
        with patch('builtins.input', side_effect=user_input):
            self.work_log.search_by_time_spent()

        view_entry_patch.assert_called_once_with(
            ["Time Spent"], 5, "", ""
        )

    @patch('classes.WorkLog.view_entries')
    # We don't care about getting a variable for this patch, and
    # just want .view_entries to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_by_time_spent_value_error_text_output(self, *args):
        """
        Checks to see if search_by_time_spend's ValueError text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['bad input', '5']
        with patch('builtins.input', side_effect=user_input):

            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.search_by_time_spent()

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "Your selection is not a whole number, please try again: \n"
        )

    def test_search_by_date_range(self):
        """Checks to see if search_by_date_range calls the correct method"""

        user_input = ['2018/04/04', '2018/05/05']
        with patch('builtins.input', side_effect=user_input):
            with patch('classes.WorkLog.view_entries') as view_entry_patch:
                self.work_log.search_by_date_range()

        start_date = datetime.datetime(2018, 4, 4)
        end_date = datetime.datetime(2018, 5, 5)

        view_entry_patch.assert_called_with(["pub_date"], "", start_date, end_date)

    # Instead of using a with command you could add the patch as a decorator
    @patch('classes.WorkLog.view_entries')
    # patch will pass itself into the function as an argument, so you will
    # need to catch it
    def test_search_by_date_range_value_error_checker(self, view_entry_patch):
        """
        Search by Date Range ValueError
        """
        # With a bad input for the first input() call the except ValueError
        # block will be triggered
        user_input = ['Bad Input', '2018/04/04', 'Bad Input', '2018/04/04', '2018/05/05']
        with patch('builtins.input', side_effect=user_input):
            self.work_log.search_by_date_range()

        start_date = datetime.datetime(2018, 4, 4)
        end_date = datetime.datetime(2018, 5, 5)

        view_entry_patch.assert_called_with(["pub_date"], "", start_date, end_date)

    @patch('classes.WorkLog.view_entries')
    # We don't care about getting a variable for this patch, and
    # just want .view_entries to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_search_by_date_range_value_error_text_output(self, *args):
        """
        Checks to see if search_by_date_range's ValueError text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['Bad Input', '2018/04/04', 'Bad Input', '2018/04/04', '2018/05/05']
        with patch('builtins.input', side_effect=user_input):
            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.search_by_date_range()

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "Date you specified is not valid, please try again.\nDate you specified is not valid, please try again.\n"
        )

    def test_search_by_name(self):
        """Checks to see if search_by_name calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['hello', 'ignored_second_value']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):

            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.view_entries') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.search_by_name()

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called_with(["Name"], "\\bhello\\b", "", "")

    def test_add_entry(self):
        """Checks to see if add_entry calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['Radek', 'Developer', '5', 'Working on python tests']

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):

            # Here we are patching the models.Employee.create method so it does not
            # get called.
            # Notice we need the full path to it with 'models.'
            with patch('models.Employee.create') as employee_create_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.add_entry()

        # The patch employee_create_patch will hold onto whether or not it was
        # called and with what variables.

        employee_name = 'Radek'
        task_title = 'Developer'
        task_time_spent = 5
        task_notes = 'Working on python tests'

        employee_create_patch.assert_called_with(name=employee_name, task_name=task_title, time_spent=task_time_spent, notes=task_notes)

    # Instead of using a with command you could add the patch as a decorator
    @patch('models.Employee.create')
    # patch will pass itself into the function as an argument, so you will
    # need to catch it
    def test_by_add_entry_value_error_checker(self, create_entry_patch):
        """
        Add Entry Value Error ValueError
        """
        # With a bad input for the first input() call the except ValueError
        # block will be triggered
        user_input = ['Radek', 'Developer', 'Bad Input', '5', 'New Notes']
        with patch('builtins.input', side_effect=user_input):
            self.work_log.add_entry()

        employee_name = 'Radek'
        task_title = 'Developer'
        task_time_spent = 5
        task_notes = 'New Notes'

        create_entry_patch.assert_called_once_with(
            name=employee_name, task_name=task_title, time_spent=task_time_spent, notes=task_notes
        )

    @patch('classes.Employee.create')
    # We don't care about getting a variable for this patch, and
    # just want .classes.Employee.create to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_by_add_entry_value_error_text_output(self, *args):
        """
        Checks to see if search_by_date's ValueError text output
        is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['Radek', 'Developer', 'Bad Input', '5', 'New Notes']
        with patch('builtins.input', side_effect=user_input):
            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.add_entry()

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "Your selection is not a number, please try again: \n"
        )

    @patch('classes.Employee.create')
    # We don't care about getting a variable for this patch, and
    # just want .classes.Employee.create to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_by_add_entry_value_error_text_output_negative(self, *args):
        """
        Checks to see if add_entry's ValueError text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['Radek', 'Developer', 'Bad Input', '-5', '5', 'New Notes']
        with patch('builtins.input', side_effect=user_input):
            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.add_entry()

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "Your selection is not a number, please try again: \nSorry, your response must not be negative.\n"
        )

    @patch('classes.WorkLog.clear_screen')
    # We don't care about getting a variable for this patch, and
    # just want .classes.WorkLog.clear_screen to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_edit_record_value_error_text_output(self, *args):
        """
        Checks to see if edit_record's ValueError text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['y', 'Gus Gus', 'featherlight', 'bad input', '27', 'New Album']
        with patch('builtins.input', side_effect=user_input):
            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.edit_record(3)

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "Name is currently set to: Gus Gus\nTitle is currently set to: featherlight\nTime Spent is currently set to: 27\nYour selection is not a number, please try again: \nTime Spent is currently set to: 27\nNotes are currently set to: New Album\n"
        )

    @patch('classes.WorkLog.clear_screen')
    # We don't care about getting a variable for this patch, and
    # just want .classes.WorkLog.clear_screen to not run.
    # We could just *args everything if we had two uncared about patches.
    # Obviously the less patches the better though
    def test_edit_record_value_error_text_output_negative(self, *args):
        """
        Checks to see if edit_record's ValueError text output is correct
        """
        # If you want to test if the print() value was called and if the
        # value is what was expected you can do something like the following.
        user_input = ['y', 'Gus Gus', 'featherlight', '-27', '27', 'New Album']
        with patch('builtins.input', side_effect=user_input):
            # Over-ride the standard print() output's functionality so we can
            # see what was going to be printed to the console
            with patch('sys.stdout', new=io.StringIO()) as print_output:
                self.work_log.edit_record(3)

        # Get the "printed" information out of the mock
        printed_string = print_output.getvalue()

        self.assertEqual(
            printed_string,
            "Name is currently set to: Gus Gus\nTitle is currently set to: featherlight\nTime Spent is currently set to: 27\nSorry, your response must not be negative.\nTime Spent is currently set to: -27\nNotes are currently set to: New Album\n"
        )

    def test_view_entries_name(self):
        """Checks to see if view_entries calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['r']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):
            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.clear_screen') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.view_entries(["Name"], "\\bhello\\b", "", "")

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called()

    def test_view_entries_time_spent(self):
        """Checks to see if view_entries_time_spent calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['r']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):
            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.clear_screen') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.view_entries(["Time Spent", "Name"], 27, "", "")

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called()

    def test_view_entries_notes(self):
        """Checks to see if view_entries_notes calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['r']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):
            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.clear_screen') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.view_entries(["Notes"], "\\bNew Album\\b", "", "")

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called()

    def test_view_entries_date_range(self):
        """Checks to see if view_entries_date_range calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['r']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):
            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.clear_screen') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.view_entries(["pub_date"], "", "2018-08-29 00:00:00", "2018-09-01 00:00:00")

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called()

    def test_view_entries_date(self):
        """Checks to see if view_entries_date calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['r']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):
            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.clear_screen') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.view_entries(["pub_date"], "2018-08-29 00:00:00", "", "")

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called()


    def test_name_view_entries(self):
        """Checks to see if name_view_entries calls the correct method"""

        # Create a user_input variable to hold onto the input statement
        # we will fake into input()

        user_input = ['1']
        # The second string never gets called and is ignored in this method

        # We can patch the input() statements by over-riding 'builtins.input'
        # side_effect can take the list of items we want to put into
        # the input call
        with patch('builtins.input', side_effect=user_input):
            # Here we are patching the view_entries method so it does not
            # get called.
            # Notice we need the full path to it with 'classes.'
            with patch('classes.WorkLog.clear_screen') as view_entry_patch:
                # Now we need to call the function so everything will run
                # and the mock object will get triggered
                self.work_log.name_view_entries(self.bob_all_records, "\\bBob\\b")

        # The patch view_entry_patch will hold onto whether or not it was
        # called and with what variables.

        view_entry_patch.assert_called()

    # TO DO
    # Test Delete and Search Entries Methods
    """
    @mock.patch('classes.WorkLog.clear_screen', autospec=True)
    def test_search_entries(self, mock_clear_screen):
        self.work_log.search_entries()
        mock_clear_screen.assert_called()
  
   
    def test_delete(self):
        user_input = ['y']
        with patch('builtins.input', side_effect=user_input):
            with patch('classes.WorkLog.clear_screen') as delete_instance_patch:
                self.work_log.delete(Employee.select().where(Employee.time_spent==23).first())

            delete_instance_patch.assert_called()

    """

    # NOTE FOR MYSELF AS DEVELOPER
    # In order to test more complex functions you would need to do similar
    # things to the above tests. More patches or user inputs could be needed.

    # If values are changed in a class those could be tested as well.
    # Obviously the more complex the function the more complex the test, so
    # breaking things down as far as possible helps.

    # unit tests are only as good as you make them, but if all your time is
    # spent writing detailed unit tests you would not have time to code. Thus,
    # it is a balancing act. How far or to what extend you go is up to you.


if __name__ == '__main__':
    unittest.main()