import datetime
import unittest
from unittest.mock import MagicMock

from google_calendar_tool.__main__ import get_free_slots


class TestCli(unittest.TestCase):
    """

    """

    def setUp(self):
        """
        Sets up the test environment by initializing a mock service and date range.

        :return: None
        """
        self.service_mock = MagicMock()
        self.start_date = datetime.date(2024, 5, 1)
        self.end_date = datetime.date(2024, 5, 10)

    def test_get_free_slots(self):
        """
        :description: Tests the get_free_slots function for retrieving available time slots
                      when no events are scheduled in the provided date range.
        :method: test_get_free_slots
        :raises: AssertionError if the time_slots is None
        :return: None
        """
        self.service_mock.events().list().execute.return_value = {'items': []}
        time_slots = get_free_slots(self.service_mock, self.start_date, self.end_date)
        self.assertIsNotNone(time_slots)

    def test_get_free_slots_with_events(self):
        """
        Test the get_free_slots function with mocked events within a specific date range.

        :return: Asserts that the returned time slots are not None and their length is greater than zero.
        """
        self.service_mock.events().list().execute.return_value = {
            'items': [
                {'summary': 'Test Event 1', 'start': {'dateTime': '2024-05-01T10:30:00'},
                 'end': {'dateTime': '2024-05-01T11:30:00'}},
                {'summary': 'Test Event 2', 'start': {'dateTime': '2024-05-01T14:00:00'},
                 'end': {'dateTime': '2024-05-01T15:00:00'}}
            ]
        }
        time_slots = get_free_slots(self.service_mock, self.start_date, self.end_date)
        self.assertIsNotNone(time_slots)
        self.assertTrue(len(time_slots) > 0)

    def test_get_free_slots_no_working_days(self):
        """
        Tests the `get_free_slots` function for a scenario where there are no working days in the specified date range.

        :return: Asserts that the number of free time slots is zero when the start and end dates fall on weekend days.
        """
        self.service_mock.events().list().execute.return_value = {'items': []}
        start_date = datetime.date(2024, 5, 4)  # Saturday
        end_date = datetime.date(2024, 5, 5)  # Sunday
        time_slots = get_free_slots(self.service_mock, start_date, end_date)
        self.assertEqual(len(time_slots), 0)

    def test_get_free_slots_invalid_date_range(self):
        """
        Test case for get_free_slots function with an invalid date range.
        This test ensures that the function raises a ValueError when the end_date comes before the start_date.

        :return: None
        """
        self.service_mock.events().list().execute.return_value = {'items': []}
        start_date = datetime.date(2024, 5, 10)
        end_date = datetime.date(2024, 5, 1)
        with self.assertRaises(ValueError):
            get_free_slots(self.service_mock, start_date, end_date)


if __name__ == '__main__':
    unittest.main()
