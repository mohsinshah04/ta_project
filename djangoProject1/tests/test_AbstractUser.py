from django.test import TestCase
from classes.UserClass import UserObject
from ta_app.models import User, Role, Assign_User_Junction

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



class TestCreateUser(TestCase):
    def setUp(self):
        self.role = Role(Role_Name='Supervisor')
        self.abstractUser = UserObject(self.role)
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
        a = UserObject(Role(Role_Name="Instructor"))
        self.assertFalse(a.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                                       self.user_Home_Address, self.user_FName, self.user_LName))

    def test_create_with_TA(self):
        a = UserObject(Role(Role_Name="TA"))
        self.assertFalse(a.create_user(self.user_Email, self.user_Password, self.user_Role, self.user_Phone_Number,
                                       self.user_Home_Address, self.user_FName, self.user_LName))


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.SUuser_Role = Role(Role_Name="Supervisor")
        self.SUuser_Role.save()
        self.test_user = User.objects.create(User_Role=self.SUuser_Role, User_Email= "Super@uwm.edu", User_FName = "John", User_LName = "Johnson",User_Phone_Number = "1+(608)542-2343",User_Home_Address = "123, Ridgeview Ct")
        self.user = UserObject(self.SUuser_Role)

    def test_delete_user(self):
        result = self.user.delete_user(self.test_user.id)
        self.assertTrue(result, "User in database should have been deleted from table.")
        #self.assertTrue(self.abstractUser.delete_user(self.SUuser_ID))

    def test_user_does_not_exist(self):
        self.assertFalse(self.user.delete_user(1111))

    def test_user_in_database(self):
        self.user.delete_user(self.test_user.id)
        self.assertFalse(User.objects.filter(id=self.test_user.id).exists())

    def test_delete_user_instructor(self):
        a = UserObject(Role(Role_Name='Instructor'))
        self.assertFalse(a.delete_user(self.test_user.id))

    def test_delete_user_TA(self):
        a = UserObject(Role(Role_Name='TA'))
        self.assertFalse(a.delete_user(self.test_user.id))


class TestEditUser(TestCase):
    def setUp(self):
        self.role = Role(Role_Name='Supervisor')
        self.abstractUser = UserObject(self.role)
        self.role.save()
        self.test_user = User.objects.create(User_Email="genericUser@uwm.edu", User_Password="<PASSWORD", User_Role=self.role, User_Home_Address="123, Ridgeview Ct, Portage WI",
                            User_FName="Generic", User_LName="User", User_Phone_Number="1+(608)654-2321")
        self.updateEmail = "joseJoe@uwm.edu"
        self.updateRole = Role(Role_Name='Supervisor')
        self.updateRole.save()
        self.updateFName = "Jose"
        self.updateLName = "Joe"
        self.updatePassword = "<PASS124>"
        self.updateAddress = "456, Ridgeview Ct, Portage WI"
        self.updatePhoneNumber = "1+(608)554-2321"

    def test_edit_user(self):
        self.assertTrue(self.abstractUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))
        self.assertTrue(User.objects.filter(id=self.test_user.id, User_Email=self.updateEmail).exists())

    def test_edit_user_does_not_exist(self):
        self.assertFalse(self.abstractUser.edit_user(1234, self.updateEmail, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_password(self):
        self.assertFalse(self.abstractUser.edit_user(self.test_user.id, self.updateEmail, "HEAVEN",
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_email(self):
        self.assertFalse(self.abstractUser.edit_user(self.test_user.id, None, self.updatePassword,
                                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_phoneNumber(self):
        self.assertFalse(self.abstractUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                                     "123+(312)-1232", self.updateAddress, self.updateFName, self.updateLName))

    def test_edit_user_bad_fName_lName(self):
        self.assertFalse(self.abstractUser.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                        self.updatePassword, self.updateAddress, None, None))

    def test_delete_user_instructor(self):
        a = UserObject(Role(Role_Name='Instructor'))
        self.assertFalse(a.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                     self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))

    def test_delete_user_TA(self):
        a = UserObject(Role(Role_Name='TA'))
        self.assertFalse(a.edit_user(self.test_user.id, self.updateEmail, self.updatePassword,
                                    self.updatePhoneNumber, self.updateAddress, self.updateFName, self.updateLName))


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
        self.userS = UserObject(Role(Role_Name="Supervisor"))
        self.userT = UserObject(Role(Role_Name="TA"))
        self.userI = UserObject(Role(Role_Name="Instructor"))
    def test_account_roleNone(self):
        self.assertFalse(self.userS.account_role(None))

    def test_account_roleTA(self):
        self.assertTrue(self.userT.account_role(self.test_user_in.id))

    def test_account_roleSupervisor(self):
        self.assertFalse(self.userS.account_role(self.test_user_su.id))

    def test_account_roleInstructor(self):
        self.assertFalse(self.userI.account_role(self.test_user_su.id))

    def test_changeRoleSup_supervisorToInstructor(self):
        self.assertTrue(self.userS.account_role(self, self.userS, self.userI))

    def test_changeRoleSup_supervisorToTA(self):
        self.assertTrue(self.userS.account_role(self, self.userS, self.userT))

    def test_changeRoleSup_InstructorToTA(self):
        self.assertTrue(self.userS.account_role(self, self.userI, self.userT))

    def test_changeRoleSup_instructorToSupervisor(self):
        self.assertTrue(self.userS.account_role(self, self.userI, self.userS))

    def test_changeRoleSup_TAToInstructor(self):
        self.assertTrue(self.userS.account_role(self, self.userT, self.userI))

    def test_changeRoleSup_TAToSupervisor(self):
        self.assertTrue(self.userS.account_role(self, self.userT, self.userS))

    def test_changeRoleIns_TAToInstructor(self):
        self.assertTrue(self.userI.account_role(self, self.userT, self.userI))

    def test_changeRoleIns_InstructorToTA(self):
        self.assertFalse(self.userI.account_role(self, self.userI, self.userT))

    def test_changeRoleIns_TAToSupervisor(self):
        self.assertFalse(self.userI.account_role(self, self.userT, self.userS))

    def test_changeRoleIns_InstructorToSupervisor(self):
        self.assertFalse(self.userI.account_role(self, self.userI, self.userS))

    def test_changeRoleIns_SupervisorToInstructor(self):
        self.assertFalse(self.userI.account_role(self, self.userS, self.userI))

    def test_changeRoleIns_SupervisorToTA(self):
        self.assertFalse(self.userI.account_role(self, self.userS, self.userT))

    def test_changeRoleTA_TAToInstructor(self):
        self.assertFalse(self.userT.account_role(self, self.userT, self.userI))

    def test_changeRoleTA_InstructorToTA(self):
        self.assertFalse(self.userT.account_role(self, self.userI, self.userT))

    def test_changeRoleTA_TAToSupervisor(self):
        self.assertFalse(self.userT.account_role(self, self.userT, self.userS))

    def test_changeRoleTA_InstructorToSupervisor(self):
        self.assertFalse(self.userT.account_role(self, self.userI, self.userS))

    def test_changeRoleTA_SupervisorToInstructor(self):
        self.assertFalse(self.userT.account_role(self, self.userS, self.userI))

    def test_changeRoleTA_SupervisorToTA(self):
        self.assertFalse(self.userT.account_role(self, self.userS, self.userT))

    def test_changeRole_unexistantAccount(self):
        self.assertTrue(self.userE.account_role(self, self.userI, self.userT))
    def test_changeRole_unexistantAccount2(self):
        self.assertTrue(self.userI.account_role(self, self.userE, self.userT))
    def test_changeRole_unexistantAccount3(self):
        self.assertTrue(self.userI.account_role(self, self.userT, self.userE))



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
        self.userSU = UserObject(Role(Role_Name="Supervisor"))
        self.userIN = UserObject(Role(Role_Name="Instructor"))
        self.userTA = UserObject(Role(Role_Name="TA"))


    def test_user_doesnt_exist(self):
        self.assertEqual("INVALID", self.userSU.view_account(1111))

    def test_view_account_SU_to_IN(self):
        self.assertEqual("Jose, Johnson: Instructor", self.userSU.view_account(self.test_user_in.id))

    def test_view_account_SU_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", self.userSU.view_account(self.test_user_ta.id))

    def test_view_account_SU_to_SU(self):
        self.assertEqual("John, Johnson: Supervisor", self.userSU.view_account(self.test_user_su.id))

    def test_view_account_IN_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", self.userIN.view_account(self.test_user_ta.id))

    def test_view_account_IN_to_IN(self):
        self.assertEqual("Jose, Johnson: Instructor", self.userIN.view_account(self.test_user_in.id))

    def test_view_account_TA_to_TA(self):
        self.assertEqual("Joann, Johnson: TA", self.userTA.view_account(self.test_user_ta.id))

    def test_view_account_TA_to_IN(self):
        self.assertEqual("INVALID", self.userTA.view_account(self.test_user_in.id))

    def test_view_account_TA_to_SU(self):
        self.assertEqual("INVALID", self.userTA.view_account(self.test_user_su.id))

    def test_view_account_IN_to_SU(self):
        self.assertEqual("INVALID", self.userIN.view_account(self.test_user_su.id))


