from unittest import TestCase
from config.configuration import getDatabase


class TestConfiguration(TestCase):

    def test_getDatabase(self):
        config = getDatabase()
        self.assertEqual("water", config.database)
