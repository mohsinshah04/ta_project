from django.test import TestCase
import sys

sys.path.append("C:\Users\emmet\AppData\Local\Programs\Python\Python312\Lib\unittest\loader.py")

class TestApp(TestCase):
    def test_simple(self):
        self.assertTrue(True)