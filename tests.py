import unittest
from unittest.mock import patch
from collections import OrderedDict

import classes

class WorkLogTest(unittest.TestCase):

    @patch('WorkLog')
    def test_search_by_term(self, WorkLog):
        foo = WorkLog()
        foo.search_by_term()
        WorkLog.view_entries.assert_called_with("Notes", "hello", "", "")

if __name__ == '__main__':
    unittest.main()