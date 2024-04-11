from django.test import TestCase
from UserAbstactClass import UserAbstractClass
from djangoProject1.ta_app.models import User, Role

class UserAbstractClassTest(TestCase):
    def setUp(self):
        self.testRole = Role(name='Supervisor')
        self.testAbstractUser = UserAbstractClass(self.testRole)

    def test_no_parameteters(self):
        with self.assertRaises(TypeError, msg="The role given was not a supervisor"):
            a = UserAbstractClass()

    def test_supervisor_role(self):
        self.assertEqual(self.testAbstractUser.role, self.testRole)

    def test_instructor_role(self):
        instructor = Role(name="Instructor")
        with self.assertRaises(TypeError, msg="The role given was not a supervisor"):
            a = UserAbstractClass(instructor)

    def test_TA_role(self):
        TA = Role(name="TA")
        with self.assertRaises(TypeError, msg="The role given was not a supervisor"):
            a = UserAbstractClass(TA)

class TestCreateUser(TestCase):
    def setUp(self):
        self.role = Role(name='Supervisor')
        self.abstractUser = UserAbstractClass(self.role)
        self.user_Email = "genericUser@uwm.edu"
        self.user_Role = self.role
        self.user_FName = "Generic"
        self.user_LName = "User"
        self.user_Password = "<PASSWORD>"
        self.user_Home_Address = "123, Ridgeview Ct, Portage WI"


    def test_create_user(self):
        self.assertTrue(self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Password,
                                                      self.user_Home_Address, self.user_FName, self.user_LName))

    def test_create_existing_user(self):
        self.assertFalse(self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Password,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))

    def test_create_bad_user(self):
        a = User
        a.User_FName = "John"
        a.User_LName = "Doe"
        a.User_Password = "<PASSWORD>"
        self.assertFalse(self.abstractUser.create_user(a.User_FName, a.User_LName, a.User_Password))

    def test_create_empty_user(self):
        a = User
        self.assertFalse(self.abstractUser.create_user(a))

    def test_password_verification(self):
        bad_Password = "<PASSWORD123>"
        self.assertFalse(self.abstractUser.create_user(self.user_Email, bad_Password, self.user_Role, self.user_Password,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))

    def test_user_in_database(self):
        self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Password,
                                      self.user_Home_Address, self.user_FName, self.user_LName)
        self.assertTrue(User.objects.filter(email=self.user_Email).exists())


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.role = Role(name='Supervisor')
        self.abstractUser = UserAbstractClass(self.role)
        self.user = User(User_ID=12321)


    def test_delete_user(self):
        self.assertTrue(self.abstractUser.delete_user(self.user))

    def test_user_does_not_exist(self):
        user = User
        self.assertFalse(self.abstractUser.delete_user(user))

    def test_user_in_database(self):
        self.abstractUser.delete_user(self.user)
        self.assertFalse(User.objects.filter(user_ID=self.user).exists())










