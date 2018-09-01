import datetime
import io
import unittest
from unittest.mock import patch
from unittest import mock

from classes import WorkLog

class WorkLogTest(unittest.TestCase):

    def setUp(self):
        self.work_log = WorkLog()

    def test_clear_screen(self):
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

        # Everything checks out


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
        Checks to see if search_by_date's ValueError text output
        is correct
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