from django.test import TestCase, Client
from ta_app.models import Role, User

class AccountsTest(TestCase, Client):

    def setUp(self):
        self.client = Client()
        self.SUuser_Role = Role(Role_Name="Supervisor")
        self.role = Role.objects.create(Role_Name="Supervisor")
        self.test_role = Role(Role_Name='Instructor')
        self.test_role_ta = Role(Role_Name='TA')
        self.test_role.save()
        self.test_role_ta.save()
        self.role.save()
        self.SUuser_Role.save()
        self.user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD>", User_Role=self.role, User_Home_Address="123, Ridgeview Ct, Portage WI", User_FName="Generic", User_LName="User",
                                            User_Phone_Number="1+(608)654-2321")
        self.user.save()
        self.test_user = User.objects.create(User_Role=self.SUuser_Role, User_Email= "Super@uwm.edu", User_FName = "John",
                                             User_LName = "Johnson", User_Phone_Number = "1+(608)542-2343",
                                             User_Home_Address = "123, Ridgeview Ct")

        self.test_user_in = User.objects.create(User_Role=self.test_role, User_Email="Instrc@uwm.edu",
                                                User_FName="Jose", User_LName="Johnson",
                                                User_Phone_Number="1+(608)532-2343",
                                                User_Home_Address="123, Ridgeview Ct")

        self.test_user_ta = User.objects.create(User_Role=self.test_role_ta, User_Email="TA@uwm.edu",
                                                User_FName="Joann",
                                                User_LName="Johnson",
                                                User_Phone_Number="1+(608)522-2343",
                                                User_Home_Address="123, Ridgeview Ct")
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)

    def test_view_account(self):
        response = self.client.post('/accounts/', {'id': self.test_user.id})
        self.assertEqual(response.context['name'], 'John, Johnson') and self.assertEqual(response.context['role'], 'Supervisor')

    def test_user_doesnt_exist(self):
        response = self.client.post('/accounts/', {'id': 12323})
        self.assertEqual(response.context['message'], "Invalid account id: 12323")

    def test_in_view_su(self):
        self.client.post("/", {"Email": self.test_user_in.User_Email, "Password": self.test_user_in.User_Password}, follow=True)
        response = self.client.post('/accounts/', {'id': self.test_user.id})
        self.assertEqual(response.context['message'], "You cannot view this account because of your role")

    def test_ta_view_su(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_ta.User_Password}, follow=True)
        response = self.client.post('/accounts/', {'id': self.test_user.id})
        self.assertEqual(response.context['message'], "You cannot view this account because of your role")

    def test_ta_view_in(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_ta.User_Password}, follow=True)
        response = self.client.post('/accounts/', {'id': self.test_user_in.id})
        self.assertEqual(response.context['message'], "You cannot view this account because of your role")




class AccountCreationTests(TestCase, Client):
    def setUp(self):
        self.client = Client()
        self.role = Role(Role_Name='Supervisor')
        self.test_role = Role(Role_Name='Instructor')
        self.test_role_ta = Role(Role_Name='TA')
        self.role.save()
        self.test_role.save()
        self.test_role_ta.save()
        self.user_Email = "genericUser@uwm.edu"
        self.user_Role = self.test_role
        self.user_FName = "Generic"
        self.user_LName = "User"
        self.user_Password = "<PASSWORD>"
        self.user_Home_Address = "123, Ridgeview Ct, Portage WI"
        self.user_Phone_Number = "1+(608)654-2321"
        self.test_user = User.objects.create(User_Role=self.role, User_Email="Super@uwm.edu", User_Password="<PASSWORD>", User_FName="John",
                                             User_LName="Johnson", User_Phone_Number="1+(608)542-2343", User_Home_Address="123, Ridgeview Ct")
        self.test_user_in = User.objects.create(User_Role=self.test_role, User_Email="Instrc@uwm.edu",
                                                User_FName="Jose", User_LName="Johnson",
                                                User_Phone_Number="1+(608)532-2343",
                                                User_Home_Address="123, Ridgeview Ct")

        self.test_user_ta = User.objects.create(User_Role=self.test_role_ta, User_Email="TA@uwm.edu", User_FName="Joann",
                                                User_LName="Johnson",
                                                User_Phone_Number="1+(608)522-2343",
                                                User_Home_Address="123, Ridgeview Ct")
        self.client.post("/", {"Email": self.test_user.User_Email, "Password": self.test_user.User_Password}, follow=True)


    def test_create_user(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password, "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role, "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "User was created successfully")

    def test_create_user_invalid_password(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": "HEAVEN",
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "User was not created successfully")

    def test_create_user_invalid_name(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role,
                                                        "First Name": "", "Last Name": ""})
        self.assertEqual(response.context['message'], "User was not created successfully")

    def test_create_user_invalid_phone(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": "1+(608)543-123211", "Role": self.user_Role,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "User was not created successfully")

    def test_create_user_invalid_role(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": "Guy",
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "Please enter in all information")

    def test_create_user_as_in(self):
        self.client.post("/", {"Email": self.test_user_in.User_Email, "Password": self.test_user_in.User_Password}, follow=True)
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "You do not have permission to create users")

    def test_create_user_as_ta(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_ta.User_Password}, follow=True)
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "You do not have permission to create users")

