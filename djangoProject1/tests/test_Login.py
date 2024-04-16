from django.test import TestCase, Client
from ta_app.models import Role, User

class TestLogin(TestCase, Client):

    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(Role_Name="Supervisor")
        self.role.save()
        self.user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD>", User_Role=self.role, User_Home_Address="123, Ridgeview Ct, Portage WI",
                            User_FName="Generic", User_LName="User", User_Phone_Number="1+(608)654-2321")
        self.user.save()

    def test_login(self):
        response = self.client.post("login", data={"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)
        self.assertRedirects(response, "home.html")