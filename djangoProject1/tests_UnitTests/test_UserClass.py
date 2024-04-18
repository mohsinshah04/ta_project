from django.test import TestCase
from classes.UserClass import UserObject
from ta_app.models import User, Role, Assign_User_Junction

"""
class UserAbstractClassTest(TestCase):
    def setUp(self):
        self.testSRole = Role(Role_Name='Supervisor')
        self.testIRole = Role(Role_Name='Instructor')
        self.testTRole = Role(Role_Name='TA')

    def test_no_parameters(self):
        with self.assertRaises(TypeError, msg="Please specify a valid role"):
            a = UserObject(None)

    def test_no_role(self):
        with self.assertRaises(TypeError, msg="Please specify a valid role"):
            a = UserObject("Teach")
    def test_role_supervisor(self):
        a = UserObject(Role(Role_Name='Supervisor'))
        self.assertEqual('Supervisor', a.role.Role_Name)

    def test_role_instructor(self):
        a = UserObject(Role(Role_Name='Instructor'))
        self.assertEqual('Instructor', a.role.Role_Name)

    def test_role_TA(self):
        a = UserObject(Role(Role_Name='TA'))
        self.assertEqual('TA', a.role.Role_Name)
"""



class TestCreateUser(TestCase):
    def setUp(self):
        self.role = Role(Role_Name='Supervisor')
        self.INuser_Role = Role(Role_Name='Instructor')
        self.TAuser_Role = Role(Role_Name='TA')
        self.role.save()
        self.INuser_Role.save()
        self.TAuser_Role.save()
        self.user_Email = "genericUser@uwm.edu"
        self.user_Role = self.role
        self.user_FName = "Generic"
        self.user_LName = "User"
        self.user_Password = "<PASSWORD>"
        self.user_Home_Address = "123, Ridgeview Ct, Portage WI"
        self.user_Phone_Number = "1+(608)654-2321"
        self.test_user = User.objects.create(User_Role=self.role, User_Email="Super@uwm.edu", User_FName="John", User_LName="Johnson",
                                             User_Phone_Number="1+(608)542-2343",User_Home_Address="123, Ridgeview Ct")

        self.test_user_in = User.objects.create(User_Role=self.INuser_Role, User_Email="Instrc@uwm.edu", User_FName="Jose", User_LName="Johnson",
                                                User_Phone_Number="1+(608)532-2343", User_Home_Address="123, Ridgeview Ct")

        self.test_user_ta = User.objects.create(User_Role=self.TAuser_Role, User_Email="TA@uwm.edu", User_FName="Joann", User_LName="Johnson",
                                                User_Phone_Number="1+(608)522-2343", User_Home_Address="123, Ridgeview Ct")


    def test_create_user(self):
        self.assertTrue(UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                      self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id))

    def test_create_existing_user(self):
        UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                      self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        self.assertFalse(UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id))
    """
    def test_create_bad_user(self):
        a = User
        a.User_FName = "John"
        a.User_LName = "Doe"
        a.User_Password = "<PASSWORD>"
        with self.assertRaises("TypeError" ):
            UserObject.create_user(a.User_FName, a.User_LName, a.User_Password)
    """


    def test_create_empty_user(self):
        self.assertFalse(UserObject.create_user(None, None, None, None,
                                                       None, None, None, self.test_user.id))



    def test_password_verification(self):
        bad_Password = "HEAVEN"
        self.assertFalse(UserObject.create_user(self.user_Email, bad_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id))

    def test_user_in_database(self):
        UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                      self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        self.assertTrue(User.objects.filter(User_Email=self.user_Email).exists())

    def test_create_with_instructor(self):
        self.assertFalse(UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                self.user_Home_Address, self.user_FName, self.user_LName, self.test_user_in.id))

    def test_create_with_TA(self):
        self.assertFalse(UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                self.user_Home_Address, self.user_FName, self.user_LName, self.test_user_ta.id))


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.SUuser_Role = Role(Role_Name="Supervisor")
        self.INuser_Role = Role(Role_Name='Instructor')
        self.TAuser_Role = Role(Role_Name='TA')
        self.SUuser_Role.save()
        self.INuser_Role.save()
        self.TAuser_Role.save()
        self.test_user = User.objects.create(User_Role=self.SUuser_Role, User_Email= "Super@uwm.edu", User_FName = "John", User_LName = "Johnson",User_Phone_Number = "1+(608)542-2343",User_Home_Address = "123, Ridgeview Ct")
        self.test_sUser = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD", User_Role=self.SUuser_Role, User_Home_Address="123, Ridgeview Ct, Portage WI",
                            User_FName="Generic", User_LName="User", User_Phone_Number="1+(608)654-2321")

        self.test_user_in = User.objects.create(User_Role=self.INuser_Role, User_Email="Instrc@uwm.edu", User_FName="Jose", User_LName="Johnson",
                                                User_Phone_Number="1+(608)532-2343", User_Home_Address="123, Ridgeview Ct")

        self.test_user_ta = User.objects.create(User_Role=self.TAuser_Role, User_Email="TA@uwm.edu", User_FName="Joann", User_LName="Johnson",
                                                User_Phone_Number="1+(608)522-2343", User_Home_Address="123, Ridgeview Ct")

    def test_delete_user(self):
        result = UserObject.delete_user(self.test_user.id, self.test_sUser.id)
        self.assertTrue(result, "User in database should have been deleted from table.")

    def test_user_does_not_exist(self):
        self.assertFalse(UserObject.delete_user(1111, self.test_sUser.id))

    def test_user_in_database(self):
        UserObject.delete_user(self.test_user.id, self.test_sUser.id)
        self.assertFalse(User.objects.filter(id=self.test_user.id).exists())

    def test_delete_user_instructor(self):
        self.assertFalse(UserObject.delete_user(self.test_sUser.id, self.test_user_in.id))

    def test_delete_user_TA(self):
        self.test_sUser.user_Role = Role(Role_Name="TA")
        self.assertFalse(UserObject.delete_user(self.test_sUser.id, self.test_user_ta.id))


class TestEditUser(TestCase):
    def setUp(self):
        self.SUuser_Role = Role(Role_Name='Supervisor')
        self.INuser_Role = Role(Role_Name='Instructor')
        self.TAuser_Role = Role(Role_Name='TA')
        self.SUuser_Role.save()
        self.INuser_Role.save()
        self.TAuser_Role.save()
        self.test_user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD", User_Role=self.SUuser_Role, User_Home_Address="123, Ridgeview Ct, Portage WI",
                            User_FName="Generic", User_LName="User", User_Phone_Number="1+(608)654-2321")

        self.test_user_su = User.objects.create(User_Role=self.SUuser_Role, User_Email="Super@uwm.edu",User_FName="John", User_LName="Johnson",User_Phone_Number="1+(608)542-2343",
                                                User_Home_Address="123, Ridgeview Ct")

        self.test_user_in = User.objects.create(User_Role=self.INuser_Role, User_Email="Instrc@uwm.edu", User_FName="Jose", User_LName="Johnson", User_Phone_Number="1+(608)532-2343",
                                                User_Home_Address="123, Ridgeview Ct")

        self.test_user_ta = User.objects.create(User_Role=self.TAuser_Role, User_Email="TA@uwm.edu", User_FName="Joann", User_LName="Johnson", User_Phone_Number="1+(608)522-2343",
                                                User_Home_Address="123, Ridgeview Ct")

        self.updateEmail = "joseJoe@uwm.edu"
        self.updateFName = "Jose"
        self.updateLName = "Joe"
        self.updatePassword = "<PASS124>"
        self.updateAddress = "456, Ridgeview Ct, Portage WI"
        self.updatePhoneNumber = "1+(608)554-2321"

    def test_edit_user(self):
        self.assertTrue(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_su.id))
        self.assertTrue(User.objects.filter(id=self.test_user.id, User_Email=self.updateEmail).exists())

    def test_edit_user_does_not_exist(self):
        self.assertFalse(UserObject.edit_user(1234, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id))

    def test_edit_user_bad_password(self):
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, "HEAVEN",
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id))

    def test_edit_user_bad_email(self):
        self.assertFalse(UserObject.edit_user(self.test_user.id, None, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id))

    def test_edit_user_bad_phoneNumber(self):
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                                     "123+(312)-1232", self.updateAddress, self.updateFName, self.updateLName, self.test_user.id))

    def test_edit_user_bad_fName_lName(self):
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                        self.updatePassword, self.updateAddress, None, None, self.test_user.id))

    def test_edit_user_instructor(self):
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                     self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_in.id))

    def test_edit_user_TA(self):
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_ta.id))

    def test_edit_self_TA(self):
        self.assertTrue(UserObject.edit_user(self.test_user_ta.id, self.updateEmail, self.updatePassword,
                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_ta.id))

    def test_edit_self_IN(self):
        self.assertTrue(UserObject.edit_user(self.test_user_in.id, self.updateEmail, self.updatePassword,
                                             self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_in.id))

    def test_edit_self_SU(self):
        self.assertTrue(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                             self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id))


class TestAccountRole(TestCase):

    def setUp(self):
        self.SUuser_Role = Role(Role_Name='Supervisor')
        self.INuser_Role = Role(Role_Name='Instructor')
        self.TAuser_Role = Role(Role_Name='TA')
        self.SUuser_Role.save()
        self.INuser_Role.save()
        self.TAuser_Role.save()
        self.test_user_su = User.objects.create(User_Role=self.SUuser_Role, User_Email="Super@uwm.edu", User_FName="John", User_LName="Johnson",
                            User_Phone_Number="1+(608)542-2343", User_Home_Address="123, Ridgeview Ct")
        self.test_user_in = User.objects.create(User_Role=self.INuser_Role, User_Email="Instrc@uwm.edu", User_FName="Jose", User_LName="Johnson",
                            User_Phone_Number="1+(608)532-2343", User_Home_Address="123, Ridgeview Ct")
        self.test_user_ta = User.objects.create(User_Role=self.TAuser_Role, User_Email="TA@uwm.edu", User_FName="Joann", User_LName="Johnson",
                            User_Phone_Number="1+(608)522-2343", User_Home_Address="123, Ridgeview Ct")

    def test_account_roleNone(self):
        self.assertFalse(UserObject.account_role(self.test_user_ta.id, None, self.test_user_su.id))

    def test_account_role_user_does_not_exist(self):
        self.assertFalse(UserObject.account_role(1111, self.TAuser_Role, self.test_user_su.id))

    def test_account_roleTA(self):
        self.assertFalse(UserObject.account_role(self.test_user_in.id, self.TAuser_Role, self.test_user_ta.id))

    def test_account_roleSupervisor(self):
        self.assertTrue(UserObject.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_su.id))

    def test_account_roleInstructor(self):
        self.assertFalse(UserObject.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_in.id))

    def test_changeRoleSup_InstructorToTA(self):
        self.assertTrue(UserObject.account_role(self.test_user_in.id, self.TAuser_Role, self.test_user_su.id))

    def test_changeRoleSup_instructorToSupervisor(self):
        self.assertTrue(UserObject.account_role(self.test_user_in.id, self.SUuser_Role, self.test_user_su.id))

    def test_changeRoleSup_TAToInstructor(self):
        self.assertTrue(UserObject.account_role(self.test_user_ta.id, self.INuser_Role, self.test_user_su.id))

    def test_changeRoleSup_TAToSupervisor(self):
        self.assertTrue(UserObject.account_role(self.test_user_ta.id, self.SUuser_Role, self.test_user_su.id))

    def test_changeRole_SupervisorToSupervisor(self):
        self.assertTrue(UserObject.account_role(self.test_user_su.id, self.SUuser_Role, self.test_user_su.id))

    def test_changeRole_InstructorToInstructor(self):
        self.assertFalse(UserObject.account_role(self.test_user_su.id, self.INuser_Role, self.test_user_in.id))

    def test_changeRole_TAToTA(self):
        self.assertFalse(UserObject.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_ta.id))


#Waiting for course ID
class TestViewAccount(TestCase):
    def setUp(self):
        self.SUuser_Role = Role(Role_Name='Supervisor')
        self.INuser_Role = Role(Role_Name='Instructor')
        self.TAuser_Role = Role(Role_Name='TA')
        self.SUuser_Role.save()
        self.INuser_Role.save()
        self.TAuser_Role.save()
        self.test_user_su = User.objects.create(User_Role=self.SUuser_Role, User_Email="Super@uwm.edu",
                            User_FName="John", User_LName="Johnson",
                            User_Phone_Number="1+(608)542-2343", User_Home_Address="123, Ridgeview Ct")
        self.test_user_in = User.objects.create(User_Role=self.INuser_Role, User_Email="Instrc@uwm.edu",
                            User_FName="Jose", User_LName="Johnson",
                            User_Phone_Number="1+(608)532-2343", User_Home_Address="123, Ridgeview Ct")
        self.test_user_ta = User.objects.create(User_Role=self.TAuser_Role, User_Email="TA@uwm.edu",
                            User_FName="Joann", User_LName="Johnson",
                            User_Phone_Number="1+(608)522-2343", User_Home_Address="123, Ridgeview Ct")


    def test_user_doesnt_exist(self):
        self.assertEqual("INVALID", UserObject.view_account(1111, self.test_user_su.id))

    def test_view_account_SU_to_IN(self):
        self.assertEqual("Jose, Johnson: Instructor", UserObject.view_account(self.test_user_in.id, self.test_user_su.id))

    def test_view_account_SU_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", UserObject.view_account(self.test_user_ta.id, self.test_user_su.id))

    def test_view_account_SU_to_SU(self):
        self.assertEqual("John, Johnson: Supervisor", UserObject.view_account(self.test_user_su.id, self.test_user_su.id))

    def test_view_account_IN_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", UserObject.view_account(self.test_user_ta.id, self.test_user_in.id))

    def test_view_account_IN_to_IN(self):
        self.assertEqual("Jose, Johnson: Instructor", UserObject.view_account(self.test_user_in.id, self.test_user_su.id))

    def test_view_account_TA_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", UserObject.view_account(self.test_user_ta.id, self.test_user_ta.id))

    def test_view_account_TA_to_IN(self):
        self.assertEqual("INVALID", UserObject.view_account(self.test_user_in.id, self.test_user_ta.id))

    def test_view_account_TA_to_SU(self):
        self.assertEqual("INVALID", UserObject.view_account(self.test_user_su.id, self.test_user_ta.id))

    def test_view_account_IN_to_SU(self):
        self.assertEqual("INVALID", UserObject.view_account(self.test_user_su.id, self.test_user_ta.id))

