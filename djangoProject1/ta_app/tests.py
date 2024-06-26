from django.test import TestCase
import tests_UnitTests.test_UserClass
import tests_UnitTests.test_Course
from tests_AcceptanceTests.test_Accounts import AccountSearchTest, AccountCreationTests, AccountsDelete, AccountsEditOthers, AccountsEditSelf
from tests_AcceptanceTests.test_Login import TestLogin
from tests_AcceptanceTests.test_Courses import TestCoursesCreate, TestCoursesEdit, TestCoursesView
from tests_AcceptanceTests.test_Sections import TestSectionCreate, TestSectionsView, TestSectionEdit
from tests_AcceptanceTests.test_Annoucment import AnnouncementTests

class TestUserClass(TestCase):
    def test_all(self):
        self.assertTrue(tests_UnitTests.test_UserClass)


class TestCourseClass(TestCase):
    def test_all(self):
        self.assertTrue(tests_UnitTests.test_Course)


class TestAccounts(TestCase):
    def test_all(self):
        self.assertTrue(AccountSearchTest, AccountCreationTests)
        self.assertTrue(AccountsDelete, AccountsEditOthers)
        self.assertTrue(AccountsEditSelf, AccountsEditSelf)

class TestSections(TestCase):
    def test_all(self):
        self.assertTrue(TestSectionCreate, TestSectionsView)
        self.assertTrue(TestSectionEdit)

class TestAnnoucements(TestCase):
    def test_all(self):
        self.assertTrue(AnnouncementTests)



class TestLoginClass(TestCase):
    def test_all(self):
        self.assertTrue(TestLogin)


class TestCourses(TestCase):
    def test_all(self):
        self.assertTrue(TestCoursesView, TestCoursesCreate)
        self.assertTrue(TestCoursesEdit)










