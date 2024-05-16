from django.test import TestCase
from classes.UserClass import UserObject
from ta_app.models import User, Role


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
        # toReturn = MockUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
        #                                                       self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        self.assertTrue(UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                      self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id))

    def test_create_existing_user(self):
        # toReturn = MockUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
        #                                       self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                      self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        self.assertFalse(UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id))


    def test_create_empty_user(self):
        # toReturn = MockUser.create_user(None, None, None, None,
        #                                                        None, None, None, self.test_user.id)
        self.assertFalse(UserObject.create_user(None, None, None, None,
                                                       None, None, None, self.test_user.id))



    def test_password_verification(self):
        # toReturn = MockUser.create_user(self.user_Email, bad_Password, self.user_Role, self.user_Phone_Number,
        #                                                        self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        bad_Password = "HEAVEN"
        self.assertFalse(UserObject.create_user(self.user_Email, bad_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id))

    def test_user_in_database(self):
        # toReturn = MockUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
        #                                       self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                      self.user_Home_Address, self.user_FName, self.user_LName, self.test_user.id)
        self.assertTrue(User.objects.filter(User_Email=self.user_Email).exists())

    def test_create_with_instructor(self):
        # toReturn = MockUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
        #                                                 self.user_Home_Address, self.user_FName, self.user_LName, self.test_user_in.id)
        self.assertFalse(UserObject.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                self.user_Home_Address, self.user_FName, self.user_LName, self.test_user_in.id))

    def test_create_with_TA(self):
        # toReturn = MockUser.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
        #                                                 self.user_Home_Address, self.user_FName, self.user_LName, self.test_user_ta.id)
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
        # toReturn = MockUser.delete_user(self.test_user.id, self.test_sUser.id)
        self.assertTrue(UserObject.delete_user(self.test_user.id, self.test_sUser.id))

    def test_user_does_not_exist(self):
        # toReturn = MockUser.delete_user(1111, self.test_sUser.id)
        self.assertFalse(UserObject.delete_user(1111, self.test_sUser.id))

    def test_user_in_database(self):
        # toReturn = MockUser.delete_user(self.test_user.id, self.test_sUser.id)
        UserObject.delete_user(self.test_user.id, self.test_sUser.id)
        self.assertFalse(User.objects.filter(id=self.test_user.id).exists())

    def test_delete_user_instructor(self):
        # toReturn = MockUser.delete_user(self.test_sUser.id, self.test_user_in.id)
        self.assertFalse(UserObject.delete_user(self.test_sUser.id, self.test_user_in.id))

    def test_delete_user_TA(self):
        # toReturn = MockUser.delete_user(self.test_sUser.id, self.test_user_ta.id)
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
        self.updateSkillSUorIN = ""
        self.updateTAGrader = "Grader"
        self.updateTANA = "N/A"

    def test_edit_user(self):
        # toReturn = MockUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_su.id, self.updateSkillSUorIN)
        self.assertTrue(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user_su.id))
        self.assertTrue(User.objects.filter(id=self.test_user.id, User_Email=self.updateEmail).exists())

    def test_edit_user_does_not_exist(self):
        # toReturn = MockUser.edit_user(1234, self.updateEmail, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id, self.updateSkillSUorIN)
        self.assertFalse(UserObject.edit_user(1234, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user.id))

    def test_edit_user_bad_password(self):
        # toReturn = MockUser.edit_user(self.test_user.id, self.updateEmail, "HEAVEN", self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id, self.updateSkillSUorIN)
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, "HEAVEN",
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user.id))

    def test_edit_user_bad_email(self):
        # toReturn = MockUser.edit_user(self.test_user.id, None, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id, self.updateSkillSUorIN)
        self.assertFalse(UserObject.edit_user(self.test_user.id, None, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user.id))

    def test_edit_user_bad_phoneNumber(self):
        # toReturn = MockUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword, "123+(312)-123211", self.updateAddress, self.updateFName, self.updateLName, self.test_user.id, self.updateSkillSUorIN)
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                                     "123+(312)-123211", self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user.id))

    def test_edit_user_bad_fName_lName(self):
        # toReturn = MockUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword, self.updatePassword, self.updateAddress, None, None, self.test_user.id, self.updateSkillSUorIN)
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                        self.updatePassword, self.updateAddress, None, None, self.updateSkillSUorIN, self.test_user.id))

    def test_edit_user_instructor(self):
        # toReturn = MockUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_in.id, self.updateSkillSUorIN)
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                     self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user_in.id))

    def test_edit_user_TA(self):
        # toReturn = MockUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_ta.id, self.updateSkillSUorIN)
        self.assertFalse(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user_ta.id))

    def test_edit_self_TA(self):
        # toReturn = MockUser.edit_user(self.test_user_ta.id, self.updateEmail, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_ta.id, self.updateTAGrader)
        self.assertTrue(UserObject.edit_user(self.test_user_ta.id, self.updateEmail, self.updatePassword,
                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateTAGrader, self.test_user_ta.id))

    def test_edit_self_IN(self):
        # toReturn = MockUser.edit_user(self.test_user_in.id, self.updateEmail, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user_in.id, self.updateSkillSUorIN)
        self.assertTrue(UserObject.edit_user(self.test_user_in.id, self.updateEmail, self.updatePassword,
                                             self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user_in.id))

    def test_edit_self_SU(self):
        # toReturn = MockUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword, self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.test_user.id, updateSkillSUorIN)
        self.assertTrue(UserObject.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                             self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName, self.updateSkillSUorIN, self.test_user.id))


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
        # toReturn = MockUser.account_role(self.test_user_ta.id, None, self.test_user_su.id)
        self.assertFalse(UserObject.account_role(self.test_user_ta.id, None, self.test_user_su.id))

    def test_account_role_user_does_not_exist(self):
        # toReturn = MockUser.account_role(1111, self.TAuser_Role, self.test_user_su.id)
        self.assertFalse(UserObject.account_role(1111, self.TAuser_Role, self.test_user_su.id))

    def test_account_roleTA(self):
        # toReturn = MockUser.account_role(self.test_user_in.id, self.TAuser_Role, self.test_user_ta.id)
        self.assertFalse(UserObject.account_role(self.test_user_in.id, self.TAuser_Role, self.test_user_ta.id))

    def test_account_roleSupervisor(self):
        # toReturn = MockUser.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_su.id)
        self.assertTrue(UserObject.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_su.id))

    def test_account_roleInstructor(self):
        # toReturn = MockUser.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_in.id)
        self.assertFalse(UserObject.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_in.id))

    def test_changeRoleSup_InstructorToTA(self):
        # toReturn = MockUser.account_role(self.test_user_in.id, self.TAuser_Role, self.test_user_su.id)
        self.assertTrue(UserObject.account_role(self.test_user_in.id, self.TAuser_Role, self.test_user_su.id))

    def test_changeRoleSup_instructorToSupervisor(self):
        # toReturn = MockUser.account_role(self.test_user_in.id, self.SUuser_Role, self.test_user_su.id)
        self.assertTrue(UserObject.account_role(self.test_user_in.id, self.SUuser_Role, self.test_user_su.id))

    def test_changeRoleSup_TAToInstructor(self):
        # toReturn = MockUser.account_role(self.test_user_ta.id, self.INuser_Role, self.test_user_su.id)
        self.assertTrue(UserObject.account_role(self.test_user_ta.id, self.INuser_Role, self.test_user_su.id))

    def test_changeRoleSup_TAToSupervisor(self):
        # toReturn = MockUser.account_role(self.test_user_ta.id, self.SUuser_Role, self.test_user_su.id)
        self.assertTrue(UserObject.account_role(self.test_user_ta.id, self.SUuser_Role, self.test_user_su.id))

    def test_changeRole_SupervisorToSupervisor(self):
        # toReturn = MockUser.account_role(self.test_user_su.id, self.SUuser_Role, self.test_user_su.id)
        self.assertTrue(UserObject.account_role(self.test_user_su.id, self.SUuser_Role, self.test_user_su.id))

    def test_changeRole_InstructorToInstructor(self):
        # toReturn = MockUser.account_role(self.test_user_su.id, self.INuser_Role, self.test_user_in.id)
        self.assertFalse(UserObject.account_role(self.test_user_su.id, self.INuser_Role, self.test_user_in.id))

    def test_changeRole_TAToTA(self):
        # toReturn = MockUser.account_role(self.test_user_su.id, self.TAuser_Role, self.test_user_ta.id)
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
                            User_Phone_Number="1+(608)522-2343", User_Home_Address="123, Ridgeview Ct", User_Skill="Grader")


    def test_user_doesnt_exist(self):
        # toReturn = MockUser.view_account(1111, self.test_user_su.id)
        self.assertEqual("INVALID", UserObject.view_account(1111, self.test_user_su.id))

    def test_view_account_SU_to_IN(self):
        # toReturn = MockUser.view_account(1111, self.test_user_su.id)
        self.assertEqual("Jose Johnson: Instrc@uwm.edu: 1+(608)532-2343: 123, Ridgeview Ct: Instructor: ", UserObject.view_account(self.test_user_in.id, self.test_user_su.id))

    def test_view_account_SU_to_TA(self):
        # toReturn = MockUser.view_account(self.test_user_ta.id, self.test_user_su.id)
        self.assertEqual("Joann Johnson: TA@uwm.edu: 1+(608)522-2343: 123, Ridgeview Ct: TA: Grader", UserObject.view_account(self.test_user_ta.id, self.test_user_su.id))

    def test_view_account_SU_to_SU(self):
        # toReturn = MockUser.view_account(self.test_user_su.id, self.test_user_su.id)
        self.assertEqual("John Johnson: Super@uwm.edu: 1+(608)542-2343: 123, Ridgeview Ct: Supervisor: ", UserObject.view_account(self.test_user_su.id, self.test_user_su.id))

    def test_view_account_IN_to_TA(self):
        # toReturn = MockUser.view_account(self.test_user_ta.id, self.test_user_in.id)
        self.assertEqual("Joann Johnson: TA@uwm.edu: 1+(608)522-2343: 123, Ridgeview Ct: TA: Grader", UserObject.view_account(self.test_user_ta.id, self.test_user_in.id))

    def test_view_account_IN_to_IN(self):
        # toReturn = MockUser.view_account(self.test_user_in.id, self.test_user_su.id)
        self.assertEqual("Jose Johnson: Instrc@uwm.edu: 1+(608)532-2343: 123, Ridgeview Ct: Instructor: ", UserObject.view_account(self.test_user_in.id, self.test_user_su.id))

    def test_view_account_TA_to_TA(self):
        # toReturn = MockUser.view_account(self.test_user_ta.id, self.test_user_ta.id)
        self.assertEqual("Joann Johnson: TA@uwm.edu: 1+(608)522-2343: 123, Ridgeview Ct: TA: Grader", UserObject.view_account(self.test_user_ta.id, self.test_user_ta.id))

    def test_view_account_TA_to_IN(self):
        # toReturn = MockUser.view_account(self.test_user_in.id, self.test_user_ta.id)
        self.assertEqual("Jose Johnson: Instrc@uwm.edu: 1+(608)532-2343: 123, Ridgeview Ct: Instructor: ", UserObject.view_account(self.test_user_in.id, self.test_user_ta.id))

    def test_view_account_TA_to_SU(self):
        # toReturn = MockUser.view_account(self.test_user_su.id, self.test_user_ta.id)
        self.assertEqual("John Johnson: Super@uwm.edu: 1+(608)542-2343: 123, Ridgeview Ct: Supervisor: ", UserObject.view_account(self.test_user_su.id, self.test_user_ta.id))

    def test_view_account_IN_to_SU(self):
        # toReturn = MockUser.view_account(self.test_user_su.id, self.test_user_ta.id)
        self.assertEqual("John Johnson: Super@uwm.edu: 1+(608)542-2343: 123, Ridgeview Ct: Supervisor: ", UserObject.view_account(self.test_user_su.id, self.test_user_ta.id))

