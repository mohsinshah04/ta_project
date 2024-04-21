from django.test import TestCase, Client
from ta_app.models import Role, User

class AccountSearchTest(TestCase, Client):

    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(Role_Name="Supervisor")
        self.test_role = Role(Role_Name='Instructor')
        self.test_role_ta = Role(Role_Name='TA')
        self.test_role.save()
        self.test_role_ta.save()
        self.role.save()
        self.user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD>", User_Role=self.role,
                                        User_Home_Address="123, Ridgeview Ct, Portage WI", User_FName="Generic",
                                        User_LName="User", User_Phone_Number="1+(608)654-2321")
        self.test_user = User.objects.create(User_Role=self.role, User_Email="Super@uwm.edu", User_FName="John",
                                             User_LName="Johnson", User_Phone_Number="1+(608)542-2343",
                                             User_Home_Address="123, Ridgeview Ct")

        self.test_user_in = User.objects.create(User_Role=self.test_role, User_Email="Instrc@uwm.edu",
                                                User_FName="Jose", User_LName="Johnson",
                                                User_Phone_Number="1+(608)532-2343",
                                                User_Home_Address="123, Ridgeview Ct")

        self.test_user_ta = User.objects.create(User_Role=self.test_role_ta, User_Email="TA@uwm.edu",
                                                User_FName="Joann",
                                                User_LName="Johnson",
                                                User_Phone_Number="1+(608)522-2343",
                                                User_Home_Address="123, Ridgeview Ct")
        self.user.save()
        self.test_user_ta.save()
        self.test_user_in.save()
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)
        self.objects = User.objects.all()
        self.names_list = [obj.User_FName + " " + obj.User_LName for obj in self.objects]
        self.emails_list = [obj.User_Email for obj in self.objects]
        self.phone_list = [obj.User_Phone_Number for obj in self.objects]
        self.address_list = [obj.User_Home_Address for obj in self.objects]
        self.roles_list = [obj.User_Role.Role_Name for obj in self.objects]
        self.zip_list = zip(self.names_list, self.emails_list, self.phone_list, self.address_list, self.roles_list)

    def test_view_account(self):
        response = self.client.get('/accountsView/')
        for i, j in zip(response.context['Accounts'], self.zip_list):
            self.assertEqual(i, j)

    """
        def test_user_doesnt_exist(self):
        response = self.client.post('/accountSearch/', {'First Name': "I am", 'Last Name': "Not a User"})
        self.assertEqual(response.context['message'], "Invalid account: I am Not a User")

    """
    def test_in_view_su(self):
        self.client.post("/", {"Email": self.test_user_in.User_Email, "Password": self.test_user_in.User_Password}, follow=True)
        response = self.client.get('/accountsView/')
        self.assertEqual(response.context['message'], "You do not have permission to view other users")

    def test_ta_view_su(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_ta.User_Password}, follow=True)
        response = self.client.get('/accountsView/')
        self.assertEqual(response.context['message'], "You do not have permission to view other users")

    def test_ta_view_in(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_ta.User_Password}, follow=True)
        response = self.client.get('/accountsView/')
        self.assertEqual(response.context['message'], "You do not have permission to view other users")


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
                                             User_LName="Johnson", User_Phone_Number="1+(608)542-2343",
                                             User_Home_Address="123, Ridgeview Ct")

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
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role.Role_Name, "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "User was created successfully")

    def test_create_user_invalid_password(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": "HEAVEN",
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role.Role_Name,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "User was not created successfully")

    def test_create_user_already_exists(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number,
                                                        "Role": self.user_Role.Role_Name, "First Name": self.user_FName,
                                                        "Last Name": self.user_LName})
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number,
                                                        "Role": self.user_Role.Role_Name, "First Name": self.user_FName,
                                                        "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "This user already exists, please go to the update page if you would like to edit this user instead")

    def test_create_user_invalid_name(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role.Role_Name,
                                                        "First Name": "", "Last Name": ""})
        self.assertEqual(response.context['message'], "User was not created successfully")

    def test_create_user_invalid_phone(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": "1+(608)543-123211", "Role": self.user_Role.Role_Name,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "User was not created successfully")

    def test_create_user_invalid_role(self):
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": "Guy",
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "Please enter a valid role")

    def test_create_user_as_in(self):
        self.client.post("/", {"Email": self.test_user_in.User_Email, "Password": self.test_user_in.User_Password}, follow=True)
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role.Role_Name,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "You do not have permission to create users")

    def test_create_user_as_ta(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_ta.User_Password}, follow=True)
        response = self.client.post("/accountCreate/", {"Email": self.user_Email, "Password": self.user_Password,
                                                        "Address": self.user_Home_Address,
                                                        "Phone Number": self.user_Phone_Number, "Role": self.user_Role.Role_Name,
                                                        "First Name": self.user_FName, "Last Name": self.user_LName})
        self.assertEqual(response.context['message'], "You do not have permission to create users")


class AccountsEditSelf(TestCase, Client):

    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(Role_Name="Supervisor")
        self.role.save()
        self.user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD>",
                                        User_Role=self.role,
                                        User_Home_Address="123, Ridgeview Ct, Portage WI", User_FName="Generic",
                                        User_LName="User", User_Phone_Number="1+(608)654-2321")
        self.user.save()
        self.update_email = "joseJoe@uwm.edu"
        self.update_FName = "Jose"
        self.update_LName = "Joe"
        self.update_password = "<PASS124>"
        self.update_address = "456, Ridgeview Ct, Portage WI"
        self.update_phone_number = "1+(608)554-2321"
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)

    def test_edit_self(self):
        response = self.client.post("/accountEditSelf/", {"Old Password": self.user.User_Password, "Email": self.update_email, "Password": self.update_password,
                                                        "Address": self.update_address,
                                                        "Phone Number": self.update_phone_number,
                                                        "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertTrue(User.objects.filter(User_Email=self.update_email).exists())
        self.assertEqual(response.context['message'], "Account was updated successfully")

    def test_edit_self_empty_Strings(self):
        response = self.client.post("/accountEditSelf/",
                                    {"Old Password": self.user.User_Password, "Email": "", "Password": "", "Address": "", "Phone Number": "",
                                     "First Name": "", "Last Name": ""})
        self.assertEqual(response.context['message'], "Account was updated successfully")


    def test_edit_self_ids_dont_match(self):
        response = self.client.post("/accountEditSelf/",
                                    {"Old Password": "notAuser@uwm.edu", "Email": self.update_email, "Password": self.update_password,
                                     "Address": self.update_address,
                                     "Phone Number": self.update_phone_number,
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Account passwords do not match")

    def test_edit_self_bad_password(self):
        response = self.client.post("/accountEditSelf/",
                                    {"Old Password": self.user.User_Password, "Email": self.update_email, "Password": "HEAVEN",
                                     "Address": self.update_address,
                                     "Phone Number": self.update_phone_number,
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Account was not updated successfully")

    def test_edit_self_bad_phone(self):
        response = self.client.post("/accountEditSelf/",
                                    {"Old Password": self.user.User_Password, "Email": self.update_email, "Password": "HEAVEN",
                                     "Address": self.update_address,
                                     "Phone Number": "1+(608)543-123211",
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Account was not updated successfully")


class AccountsEditOthers(TestCase, Client):

    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(Role_Name="Supervisor")
        self.test_role = Role(Role_Name='Instructor')
        self.test_role_ta = Role(Role_Name='TA')
        self.role.save()
        self.test_role.save()
        self.test_role_ta.save()
        self.user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD>",
                                        User_Role=self.role,
                                        User_Home_Address="123, Ridgeview Ct, Portage WI", User_FName="Generic",
                                        User_LName="User", User_Phone_Number="1+(608)654-2321")
        self.test_user_in = User.objects.create(User_Role=self.test_role, User_Email="Instrc@uwm.edu",
                                                User_FName="Jose", User_LName="Johnson",
                                                User_Phone_Number="1+(608)532-2343",
                                                User_Home_Address="123, Ridgeview Ct",
                                                User_Password="<PASSWORD>")

        self.test_user_ta = User.objects.create(User_Role=self.test_role_ta, User_Email="TA@uwm.edu",
                                                User_FName="Joann",
                                                User_LName="Johnson",
                                                User_Phone_Number="1+(608)522-2343",
                                                User_Home_Address="123, Ridgeview Ct",
                                                User_Password="<PASSWORD>")
        self.user.save()
        self.test_user_ta.save()
        self.test_user_in.save()
        self.update_email = "joseJoe@uwm.edu"
        self.update_FName = "Jose"
        self.update_LName = "Joe"
        self.update_password = "<PASS124>"
        self.update_address = "456, Ridgeview Ct, Portage WI"
        self.update_phone_number = "1+(608)554-2321"
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)


    def test_edit_user_in(self):
        response = self.client.post("/accountEditOther/", {"User Email": self.test_user_in.User_Email, "Email": self.update_email,
                                                        "Password": self.update_password,
                                                        "Address": self.update_address,
                                                        "Phone Number": self.update_phone_number,
                                                        "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Account was updated successfully")

    def test_edit_user_ta(self):
        response = self.client.post("/accountEditOther/", {"User Email": self.test_user_ta.User_Email, "Email": self.update_email,
                                                        "Password": self.update_password,
                                                        "Address": self.update_address,
                                                        "Phone Number": self.update_phone_number,
                                                        "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Account was updated successfully")

    def test_edit_user_not_found(self):
        response = self.client.post("/accountEditOther/",
                                    {"User Email": "self.test_user_ta.User_Email", "Email": self.update_email,
                                     "Password": self.update_password,
                                     "Address": self.update_address,
                                     "Phone Number": self.update_phone_number,
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Invalid account email: self.test_user_ta.User_Email")

    def test_edit_self_empty_Strings(self):
        response = self.client.post("/accountEditOther/",
                                    {"User Email": self.test_user_in.User_Email, "Email": "", "Password": "", "Address": " ", "Phone Number": "",
                                     "First Name": "", "Last Name": ""})
        self.assertEqual(response.context['message'], "Account was updated successfully")

    def test_edit_self_bad_password(self):
        response = self.client.post("/accountEditOther/",
                                    {"User Email": self.test_user_in.User_Email, "Email": self.update_email, "Password": "HEAVEN",
                                     "Address": self.update_address,
                                     "Phone Number": self.update_phone_number,
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Account was not updated successfully")

    def test_edit_self_bad_phone(self):
        response = self.client.post("/accountEditOther/",
                                    {"User Email": self.test_user_in.User_Email, "Email": self.update_email, "Password": self.update_password,
                                     "Address": self.update_address,
                                     "Phone Number": "1+(608)543-123211",
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "Account was not updated successfully")

    def test_edit_as_in(self):
        self.client.post("/", {"Email": self.test_user_in.User_Email, "Password": self.test_user_in.User_Password},
                         follow=True)
        response = self.client.post("/accountEditOther/",
                                    {"User Email": self.user.User_Email, "Email": self.update_email, "Password": self.update_password,
                                     "Address": self.update_address,
                                     "Phone Number": "1+(608)543-123211",
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "You do not have permission to create users")

    def test_edit_as_ta(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_in.User_Password},
                         follow=True)
        response = self.client.post("/accountEditOther/",
                                    {"User Email": self.user.User_Email, "Email": self.update_email, "Password": self.update_password,
                                     "Address": self.update_address,
                                     "Phone Number": "1+(608)543-123211",
                                     "First Name": self.update_FName, "Last Name": self.update_LName})
        self.assertEqual(response.context['message'], "You do not have permission to create users")


class AccountsDelete(TestCase, Client):

    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(Role_Name="Supervisor")
        self.test_role = Role(Role_Name='Instructor')
        self.test_role_ta = Role(Role_Name='TA')
        self.role.save()
        self.test_role.save()
        self.test_role_ta.save()
        self.user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD>",
                                        User_Role=self.role,
                                        User_Home_Address="123, Ridgeview Ct, Portage WI", User_FName="Generic",
                                        User_LName="User", User_Phone_Number="1+(608)654-2321")
        self.test_user_in = User.objects.create(User_Role=self.test_role, User_Email="Instrc@uwm.edu",
                                                User_FName="Jose", User_LName="Johnson",
                                                User_Phone_Number="1+(608)532-2343",
                                                User_Home_Address="123, Ridgeview Ct")

        self.test_user_ta = User.objects.create(User_Role=self.test_role_ta, User_Email="TA@uwm.edu",
                                                User_FName="Joann",
                                                User_LName="Johnson",
                                                User_Phone_Number="1+(608)522-2343",
                                                User_Home_Address="123, Ridgeview Ct")
        self.user.save()
        self.test_user_ta.save()
        self.test_user_in.save()
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)

    def test_delete_account_in(self):
        response = self.client.post('/deleteAccounts/', {"User Email": self.test_user_in.User_Email})
        self.assertEqual(response.context['message'], "You have successfully deleted account: " + self.test_user_in.User_Email)
        self.assertFalse(User.objects.filter(id=self.test_user_in.id).exists())

    def test_delete_account_ta(self):
        response = self.client.post('/deleteAccounts/', {"User Email": self.test_user_ta.User_Email})
        self.assertEqual(response.context['message'], "You have successfully deleted account: " + self.test_user_ta.User_Email)
        self.assertFalse(User.objects.filter(id=self.test_user_ta.id).exists())

    def test_delete_account_as_in(self):
        self.client.post("/", {"Email": self.test_user_in.User_Email, "Password": self.test_user_in.User_Password},
                         follow=True)
        response = self.client.post('/deleteAccounts/', {"User Email": self.user.User_Email})
        self.assertEqual(response.context['message'], "You do not have permission to delete accounts")

    def test_delete_account_as_ta(self):
        self.client.post("/", {"Email": self.test_user_ta.User_Email, "Password": self.test_user_ta.User_Password},
                         follow=True)
        response = self.client.post('/deleteAccounts/', {"User Email": self.user.User_Email})
        self.assertEqual(response.context['message'], "You do not have permission to delete accounts")








