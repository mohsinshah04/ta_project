from django.test import TestCase, Client
import tests_UnitTests.test_UserClass
from models import User, Role


class TestAbstractUser(TestCase):
    def test_all(self):
        self.assertTrue(tests_UnitTests.test_AbstractUser)


class TestLogin(TestCase, Client):

    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(Role_Name="Supervisor")
        self.role.save()
        self.user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD>", User_Role=self.role, User_Home_Address="123, Ridgeview Ct, Portage WI",
                            User_FName="Generic", User_LName="User", User_Phone_Number="1+(608)654-2321")
        self.user.save()

    def test_login(self):
        response = self.client.post("/", data={"Email": self.user.User_Email, "Password": self.user.User_Password})
        self.assertEqual(response["Location"], "/home/")


