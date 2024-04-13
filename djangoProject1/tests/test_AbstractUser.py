from django.test import TestCase
from classes.UserAbstractClass import UserAbstractClass
from ta_app.models import User, Role, Assign_User_Junction

class UserAbstractClassTest(TestCase):
    def setUp(self):
        self.testSRole = Role(Role_Name='Supervisor')
        self.testIRole = Role(Role_Name='Instructor')
        self.testTRole = Role(Role_Name='TA')

    def test_no_parameters(self):
        with self.assertRaises(TypeError, msg="Please specify a valid role"):
            a = UserAbstractClass(None)

    def test_no_role(self):
        with self.assertRaises(TypeError, msg="Please specify a valid role"):
            a = UserAbstractClass("Teach")
    def test_role_supervisor(self):
        a = UserAbstractClass(Role(Role_Name='Supervisor'))
        self.assertEqual('Supervisor', a.role.Role_Name)

    def test_role_instructor(self):
        a = UserAbstractClass(Role(Role_Name='Instructor'))
        self.assertEqual('Instructor', a.role.Role_Name)

    def test_role_TA(self):
        a = UserAbstractClass(Role(Role_Name='TA'))
        self.assertEqual('TA', a.role.Role_Name)



class TestCreateUser(TestCase):
    def setUp(self):
        self.role = Role(Role_Name='Supervisor')
        self.abstractUser = UserAbstractClass(self.role)
        self.user_Email = "genericUser@uwm.edu"
        self.user_Role = self.role
        self.user_FName = "Generic"
        self.user_LName = "User"
        self.user_Password = "<PASSWORD>"
        self.user_Home_Address = "123, Ridgeview Ct, Portage WI"
        self.user_Phone_Number = "1+(608)654-2321"


    def test_create_user(self):
        self.assertTrue(self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                      self.user_Home_Address, self.user_FName, self.user_LName))

    def test_create_existing_user(self):
        self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                      self.user_Home_Address, self.user_FName, self.user_LName)
        self.assertFalse(self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))
    """
    def test_create_bad_user(self):
        a = User
        a.User_FName = "John"
        a.User_LName = "Doe"
        a.User_Password = "<PASSWORD>"
        with self.assertRaises("TypeError" ):
            self.abstractUser.create_user(a.User_FName, a.User_LName, a.User_Password)
    """


    def test_create_empty_user(self):
        a = User
        self.assertFalse(self.abstractUser.create_user(None, None, None, None,
                                                       None, None, None))



    def test_password_verification(self):
        bad_Password = "HEAVEN"
        self.assertFalse(self.abstractUser.create_user(self.user_Email, bad_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))

    def test_user_in_database(self):
        self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                      self.user_Home_Address, self.user_FName, self.user_LName)
        self.assertTrue(User.objects.filter(User_Email=self.user_Email).exists())

    def test_create_with_instructor(self):
        a = UserAbstractClass(Role(Role_Name="Instructor"))
        self.assertFalse(a.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))

    def test_create_with_TA(self):
        a = UserAbstractClass(Role(Role_Name="TA"))
        self.assertFalse(a.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                       self.user_Home_Address, self.user_FName, self.user_LName))


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.role = Role(Role_Name='Supervisor')
        self.abstractUser = UserAbstractClass(self.role)
        self.SUuser_ID = 1234
        self.SUuser_Role = Role(Role_Name='Supervisor')
        self.SUuser_Role.save()
        User.objects.create(User_ID=self.SUuser_ID, User_Role=self.SUuser_Role, User_Email="Super@uwm.edu", User_FName="John", User_LName="Johnson",
                            User_Phone_Number="1+(608)542-2343", User_Home_Address="123, Ridgeview Ct")


    def test_delete_user(self):
        self.assertTrue(self.abstractUser.delete_user(self.SUuser_ID))

    def test_user_does_not_exist(self):
        self.assertFalse(self.abstractUser.delete_user(1111))

    def test_user_in_database(self):
        self.abstractUser.delete_user(self.SUuser_ID)
        self.assertFalse(User.objects.filter(User_ID=self.SUuser_ID).exists())

    def test_delete_user_instructor(self):
        a = UserAbstractClass(Role(Role_Name='Instructor'))
        self.assertFalse(a.delete_user(self.SUuser_ID))

    def test_delete_user_TA(self):
        a = UserAbstractClass(Role(Role_Name='TA'))
        self.assertFalse(a.delete_user(self.SUuser_ID))


class TestEditUser(TestCase):
    def setUp(self):
        self.role = Role(Role_Name='Supervisor')
        self.abstractUser = UserAbstractClass(self.role)
        self.role.save()
        self.user_ID = 12321
        User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD", User_Role=self.role, User_Home_Address="123, Ridgeview Ct, Portage WI",
                            User_FName="Generic", User_LName="User", User_Phone_Number="1+(608)654-2321", User_ID=12321)
        self.updateEmail = "joseJoe@uwm.edu"
        self.updateRole = Role(Role_Name='Supervisor')
        self.updateRole.save()
        self.updateFName = "Jose"
        self.updateLName = "Joe"
        self.updatePassword = "<PASS124>"
        self.updateAddress = "456, Ridgeview Ct, Portage WI"
        self.updatePhoneNumber = "1+(608)554-2321"

    def test_edit_user(self):
        self.assertTrue(self.abstractUser.edit_user(self.user_ID, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))
        self.assertTrue(User.objects.filter(User_ID=self.user_ID, User_Email=self.updateEmail).exists())

    def test_edit_user_does_not_exist(self):
        self.assertFalse(self.abstractUser.edit_user(1234, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_password(self):
        self.assertFalse(self.abstractUser.edit_user(self.user_ID, self.updateEmail, "HEAVEN",
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_email(self):
        self.assertFalse(self.abstractUser.edit_user(self.user_ID, None, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_phoneNumber(self):
        self.assertFalse(self.abstractUser.edit_user(self.user_ID, self.updateEmail, self.updatePassword,
                                                     "123+(312)-1232", self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_fName_lName(self):
        self.assertFalse(self.abstractUser.edit_user(self.user_ID, self.updateEmail, self.updatePassword,
                                        self.updatePassword, self.updateAddress, None, None))

    def test_delete_user_instructor(self):
        a = UserAbstractClass(Role(Role_Name='Instructor'))
        self.assertFalse(a.edit_user(self.user_ID, self.updateEmail, self.updatePassword,
                                     self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_delete_user_TA(self):
        a = UserAbstractClass(Role(Role_Name='TA'))
        self.assertFalse(a.edit_user(self.user_ID, self.updateEmail, self.updatePassword,
                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))
class TestAccountRole(TestCase):
    def setUp(self):
        self.SUuser_ID = 1234
        self.INuser_ID = 4567
        self.TAuser_ID = 7890
        self.SUuser_Role = Role(Role_Name='Supervisor')
        self.INuser_Role = Role(Role_Name='Instructor')
        self.TAuser_Role = Role(Role_Name='TA')
        self.SUuser_Role.save()
        self.INuser_Role.save()
        self.TAuser_Role.save()
        User.objects.create(User_ID=self.SUuser_ID, User_Role=self.SUuser_Role, User_Email="Super@uwm.edu", User_FName="John", User_LName="Johnson",
                            User_Phone_Number="1+(608)542-2343", User_Home_Address="123, Ridgeview Ct")
        User.objects.create(User_ID=self.INuser_ID, User_Role=self.INuser_Role, User_Email="Instrc@uwm.edu", User_FName="Jose", User_LName="Johnson",
                            User_Phone_Number="1+(608)532-2343", User_Home_Address="123, Ridgeview Ct")
        User.objects.create(User_ID=self.TAuser_ID, User_Role=self.TAuser_Role, User_Email="TA@uwm.edu", User_FName="Joann", User_LName="Johnson",
                            User_Phone_Number="1+(608)522-2343", User_Home_Address="123, Ridgeview Ct")
        self.abstractUserS = UserAbstractClass(Role(Role_Name="Supervisor"))
        self.abstractUserT = UserAbstractClass(Role(Role_Name="TA"))
        self.abstractUserI = UserAbstractClass(Role(Role_Name="Instructor"))
    def test_account_roleNone(self):
        self.assertFalse(self.abstractUserS.account_role(None))

    def test_account_roleTA(self):
        self.assertTrue(self.abstractUserT.account_role(self.INuser_ID))

    def test_account_roleSupervisor(self):
        self.assertFalse(self.abstractUserS.account_role(self.SUuser_ID))

    def test_account_roleInstructor(self):
        self.assertFalse(self.abstractUserI.account_role(self.SUuser_ID))

#Waiting for course ID
class TestViewAccount(TestCase):
    def setUp(self):
        self.SUuser_ID = 1234
        self.INuser_ID = 4567
        self.TAuser_ID = 7890
        self.SUuser_Role = Role(Role_Name='Supervisor')
        self.INuser_Role = Role(Role_Name='Instructor')
        self.TAuser_Role = Role(Role_Name='TA')
        self.SUuser_Role.save()
        self.INuser_Role.save()
        self.TAuser_Role.save()
        User.objects.create(User_ID=self.SUuser_ID, User_Role=self.SUuser_Role, User_Email="Super@uwm.edu",
                            User_FName="John", User_LName="Johnson",
                            User_Phone_Number="1+(608)542-2343", User_Home_Address="123, Ridgeview Ct")
        User.objects.create(User_ID=self.INuser_ID, User_Role=self.INuser_Role, User_Email="Instrc@uwm.edu",
                            User_FName="Jose", User_LName="Johnson",
                            User_Phone_Number="1+(608)532-2343", User_Home_Address="123, Ridgeview Ct")
        User.objects.create(User_ID=self.TAuser_ID, User_Role=self.TAuser_Role, User_Email="TA@uwm.edu",
                            User_FName="Joann", User_LName="Johnson",
                            User_Phone_Number="1+(608)522-2343", User_Home_Address="123, Ridgeview Ct")
        self.abstractSU = UserAbstractClass(Role(Role_Name="Supervisor"))
        self.abstractIN = UserAbstractClass(Role(Role_Name="Instructor"))
        self.abstractTA = UserAbstractClass(Role(Role_Name="TA"))

    def test_user_doesnt_exist(self):
        self.assertEqual("INVALID", self.abstractSU.view_account(1111))

    def test_view_account_SU_to_IN(self):
        self.assertEqual("Jose, Johnson: Instructor", self.abstractSU.view_account(self.INuser_ID))

    def test_view_account_SU_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", self.abstractSU.view_account(self.TAuser_ID))

    def test_view_account_SU_to_SU(self):
        self.assertEqual("John, Johnson: Supervisor", self.abstractSU.view_account(self.SUuser_ID))

    def test_view_account_IN_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", self.abstractIN.view_account(self.TAuser_ID))

    def test_view_account_IN_to_IN(self):
        self.assertEqual("Jose, Johnson: Instructor", self.abstractIN.view_account(self.INuser_ID))

    def test_view_account_TA_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", self.abstractTA.view_account(self.TAuser_ID))

    def test_view_account_TA_to_IN(self):
        self.assertEqual("INVALID", self.abstractTA.view_account(self.INuser_ID))

    def test_view_account_TA_to_SU(self):
        self.assertEqual("INVALID", self.abstractTA.view_account(self.SUuser_ID))

    def test_view_account_IN_to_SU(self):
        self.assertEqual("INVALID", self.abstractIN.view_account(self.SUuser_ID))


