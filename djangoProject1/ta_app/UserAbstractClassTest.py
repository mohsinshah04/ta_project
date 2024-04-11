from django.test import TestCase
import UserAbstractClass


class TestCreateUser(TestCase):
    def setUp(self):
        self.user = UserAbstractClass.User()
        self.role = UserAbstractClass.Role()
        self.role.Role_Name = "Supervisor"
        self.user.User_Email = "genericUser@uwm.edu"
        self.user.User_Role = self.role
        self.user.User_FName = "Generic"
        self.user.User_LName = "User"
        self.user.User_Password = "<PASSWORD>"
        self.user.User_Home_Address = "123, Ridgeview Ct, Portage WI"


    def test_create_user(self):
        self.assertTrue(UserAbstractClass.create_user(self.user))

    def test_create_existing_user(self):
        self.assertFalse(UserAbstractClass.create_user(self.user))

    def test_create_bad_user(self):
        a = UserAbstractClass.User()
        a.User_FName = "John"
        a.User_LName = "Doe"
        a.User_Password = "<PASSWORD>"
        self.assertFalse(UserAbstractClass.create_user(a))



