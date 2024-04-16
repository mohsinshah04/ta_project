from django.test import TestCase
from ta_app.models import User, Role
from classes.Stand_Alone_Functions import Stand_Alone_Functions\



class TestLoginUser(TestCase):

    def setUp(self):
        self.user_Role = Role(User_Name='Supervisor')
        self.user_ID = 1234
        self.user_Role.save()
        self.user_email = "genericUser@uwm.edu"
        self.user_pass = "<PASSWORD>"
        User.objects.create(User_Email=self.user_email, User_Password=self.user_pass, User_Role=self.user_Role,
                            User_Home_Address="123, Ridgeview Ct, Portage WI",
                            User_FName="Generic", User_LName="User", User_Phone_Number="1+(608)654-2321", User_ID=self.user_ID)

    def test_user_doesnt_exist(self):
        pass