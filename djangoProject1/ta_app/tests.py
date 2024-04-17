from django.test import TestCase, Client
import tests_UnitTests.test_UserClass
from models import User, Role


class TestAbstractUser(TestCase):
    def test_all(self):
        self.assertTrue(tests_UnitTests.test_UserClass)

