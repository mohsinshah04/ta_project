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
        response = self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)
        self.assertRedirects(response, "/home/")

    def test_login_wrong_password(self):
        response = self.client.post("/", {"Email": self.user.User_Email, "Password": "WrongPassword"}, follow=True)
        self.assertEqual(response.context['message'], "Incorrect Email or Password, please try again.")

    def test_login_wrong_email(self):
        response = response = self.client.post("/", {"Email": "self.user.User_Email", "Password": self.user.User_Password}, follow=True)
        self.assertEqual(response.context['message'], "Email and password do not exist. Please contact your supervisor to get your account created")

    def test_login_user_doesnt_exist(self):
        response = response = self.client.post("/", {"Email": "thisUserDoesntExist@uwm.edu", "Password": "thisIsNotAPassowrd"}, follow=True)
        self.assertEqual(response.context['message'], "Email and password do not exist. Please contact your supervisor to get your account created")

    def test_session_is_active(self):
        response = self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)
        session = self.client.session
        check_session = session.get("id")
        self.assertNotEqual(check_session, None)

    """
        def test_user_is_active(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)
        response = self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)
        self.assertEqual(response.context['message'], "User already logged in")
    """