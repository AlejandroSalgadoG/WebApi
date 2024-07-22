from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# mock method that checks if the wait_for_db command executed successfully
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):

    # the mocking sends a new parameter with the mocked function
    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")  # do not actually sleep in the test to avoid waiting
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # list of elements that will be returned from the mocked function
        # first 2 calls will return Psycopg2Error
        # next 3 OperationalError
        # finally a successfull execution
        patched_check.side_effect = [
            Psycopg2Error,
            Psycopg2Error,
            OperationalError,
            OperationalError,
            OperationalError,
            True,
        ]

        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
