from django.test import TestCase
from djangoProject1.classes.UserAbstractClass import UserAbstractClass
from djangoProject1.ta_app.models import User, Role

class UserAbstractClassTest(TestCase):
    def setUp(self):
        self.testSRole = Role(name='Supervisor')
        self.testIRole = Role(name='Supervisor')
        self.testTRole = Role(name='Supervisor')

    def test_no_parameteters(self):
        with self.assertRaises(TypeError, msg="The role given was not a supervisor"):
            a = UserAbstractClass(None)

    def test_no_role(self):
        with self.assertRaises(TypeError, msg="Please specify a role"):
            a = UserAbstractClass("Teach")
    def test_role_supervisor(self):
        a = UserAbstractClass(self.testSRole)
        self.assertEqual(Role(name='Supervisor'), a.role)

    def test_role_instructor(self):
        a = UserAbstractClass(self.testIRole)
        self.assertEqual(Role(name='Instructor'), a.role)

    def test_role_TA(self):
        a = UserAbstractClass(self.testTRole)
        self.assertEqual(Role(name='TA'), a.role)



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
        self.user_Phone_Number = "1+(608)654-2321"


    def test_create_user(self):
        self.assertTrue(self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                      self.user_Home_Address, self.user_FName, self.user_LName))

    def test_create_existing_user(self):
        self.assertFalse(self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
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
        self.assertFalse(self.abstractUser.create_user(self.user_Email, bad_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))

    def test_user_in_database(self):
        self.abstractUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                      self.user_Home_Address, self.user_FName, self.user_LName)
        self.assertTrue(User.objects.filter(email=self.user_Email).exists())

    def test_create_with_instructor(self):
        a = UserAbstractClass(Role(name="Instructor"))
        self.assertFalse(a.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))

    def test_create_with_TA(self):
        a = UserAbstractClass(Role(name="TA"))
        self.assertFalse(a.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                       self.user_Home_Address, self.user_FName, self.user_LName))


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.role = Role(name='Supervisor')
        self.abstractUser = UserAbstractClass(self.role)
        self.user = User(User_ID=12321)


    def test_delete_user(self):
        self.assertTrue(self.abstractUser.delete_user(self.user.User_ID))

    def test_user_does_not_exist(self):
        user = User
        self.assertFalse(self.abstractUser.delete_user(user))

    def test_user_in_database(self):
        self.abstractUser.delete_user(self.user)
        self.assertFalse(User.objects.filter(user_ID=self.user).exists())

    def test_delete_user_instructor(self):
        a = UserAbstractClass(Role(name='Instructor'))
        self.assertFalse(a.delete_user(self.user.User_ID))

    def test_delete_user_TA(self):
        a = UserAbstractClass(Role(name='TA'))
        self.assertFalse(a.delete_user(self.user.User_ID))


class TestEditUser(TestCase):
    def setUp(self):
        self.role = Role(name='Supervisor')
        self.abstractUser = UserAbstractClass(self.role)
        self.user = User.objects.create("genericUser@uwm.edu", "<PASSWORD", self.role,
                                      "123, Ridgeview Ct, Portage WI", "Generic", "User", "1+(608)654-2321", User_ID=12321)
        self.updateEmail = "joseJoe@uwm.edu"
        self.updateRole = Role(name='Supervisor')
        self.updateFName = "Jose"
        self.updateLName = "Joe"
        self.updatePassword = "<PASS124>"
        self.updateAddress = "456, Ridgeview Ct, Portage WI"
        self.updatePhoneNumber = "1+(608)554-2321"

    def test_edit_user(self):
        self.assertTrue(self.abstractUser.edit_user(self.user.User_ID, self.updateEmail, self.updatePassword, self.updateRole,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))
        self.assertTrue(User.objects.filter(User_ID=self.user.User_ID, email=self.updateEmail).exists())

    def test_edit_user_does_not_exist(self):
        self.assertFalse(self.abstractUser.edit_user(1234, self.updateEmail, self.updatePassword, self.updateRole,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_password(self):
        self.assertFalse(self.abstractUser.edit_user(self.user.User_ID, self.updateEmail, "<Password1232>", self.updateRole,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_email(self):
        self.assertFalse(self.abstractUser.edit_user(self.user.User_ID, "nothing", self.updatePassword, self.updateRole,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_phoneNumber(self):
        self.assertFalse(self.abstractUser.edit_user(self.user.User_ID, self.updateEmail, self.updatePassword, self.updateRole,
                                                     "123+(312)-1232", self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_fName_lName(self):
        self.assertFalse( self.abstractUser.edit_user(self.user.User_ID, self.updateEmail, self.updatePassword, self.updateRole,
                                        self.updatePassword, self.updateAddress, "", ""))

    def test_delete_user_instructor(self):
        a = UserAbstractClass(Role(name='Instructor'))
        self.assertFalse(a.edit_user(self.user.User_ID, self.updateEmail, self.updatePassword, self.updateRole,
                                     self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_delete_user_TA(self):
        a = UserAbstractClass(Role(name='TA'))
        self.assertFalse(a.edit_user(self.user.User_ID, self.updateEmail, self.updatePassword, self.updateRole,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))
class TestAccountRole(TestCase):
    def setUp(self):
        self.TARole = Role(name="TA")
        self.InstRole = Role(name="Instructor")
        self.SuperRole = Role(name="Supervisor")
        self.TAuser = User(User_ID=1234)
        self.INuser = User(User_ID=4567)
        self.SUPERuser = User(User_ID=7890)
        self.TAuser.User_Role = self.TARole
        self.InstRole.User_Role = self.InstRole
        self.SuperRole.User_Role = self.SuperRole
        self.abstractUserS = UserAbstractClass(Role(name="Supervisor"))
        self.abstractUserT = UserAbstractClass(Role(name="TA"))
        self.abstractUserI = UserAbstractClass(Role(name="Instructor"))
    def test_account_roleNone(self):
        self.assertFalse(self.abstractUserS.account_role(None))

    def test_account_roleTA(self):
        self.assertTrue(self.abstractUserT.account_role(self.INuser.User_ID))

    def test_account_roleSupervisor(self):
        self.assertFalse(self.abstractUserS.account_role(self.SUPERuser.User_ID))

    def test_account_roleInstructor(self):
        self.assertFalse(self.abstractUserT.account_role(self.SUPERuser.User_ID))

class TestViewAccount(TestCase):
    def setUp(self):
        self.TARole = Role(name="TA")
        self.InstRole = Role(name="Instructor")
        self.SuperRole = Role(name="Supervisor")
        self.TAuser = User(User_ID=1234)
        self.INuser = User(User_ID=4567)
        self.SUPERuser = User(User_ID=7890)
        self.TAuser.User_Role = self.TARole
        self.InstRole.User_Role = self.InstRole
        self.SuperRole.User_Role = self.SuperRole
        self.abstractUser = UserAbstractClass(Role(name="Supervisor"))



