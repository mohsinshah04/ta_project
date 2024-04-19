from django.test import TestCase
from classes.Role import Role
from .mocks import MockHandleAssignments
from ta_app.models import User, Role, Assign_User_Junction

class RoleTest(TestCase):
    def setUp(self):
        self.RoleTA = Role.objects.create(Role_Name="TA")
        self.Role = Role.objects.create(Role_Name="Supervisor")
        self.RoleProf = Role.objects.create(Role_Name="Instructor")

        self.user = User.objects.create(User_FName="Supervisor", User_LName="User", User_Email="admin@uwm.edu",
                                        User_Password="admin", User_Role=self.Role)
        self.userTA = User.objects.create(User_FName="John", User_LName="Pork", User_Email="ta@uwm.edu",
                                          User_Password="ta", User_Role=self.RoleTA)
        self.userProf = User.objects.create(User_FName="Himmithy", User_LName="Him", User_Email="prof@uwm.edu",
                                            User_Password="prof", User_Role=self.RoleProf)

    # create role tests
    def test_createTA(self):
        role = Role(self.RoleTA)
        self.assertEqual(Role.create_role(self.RoleTA))

    def test_createSupervisor(self):
        role = Role(self.Role)
        self.assertEqual(Role.create_role(self.Role))

    def test_createInstructor(self):
        role = Role(self.RoleProf)
        self.assertEqual(Role.create_role(self.RoleProf))

    def test_createUnexisting(self):
        role = Role(self.FAKE)
        self.assertFalse(Role.create_role(self.FAKE))

    def test_CreateRoleName(self):
        role = Role(self.Role)
        self.assertFalse(Role.RoleName(None))

    # delete role tests

    def test_deleteTA(self):
        role = Role(self.RoleTA)
        self.assertEqual(Role.delete_role(self.RoleTA))

    def test_deleteSupervisor(self):
        role = Role(self.Role)
        self.assertEqual(Role.delete_role(self.Role))

    def test_deleteInstructor(self):
        role = Role(self.RoleProf)
        self.assertEqual(Role.delete_role(self.RoleProf))

    def test_deleteUnexisting(self):
        role = Role(self.FAKE)
        self.assertFalse(Role.delete_role(self.FAKE))

    def test_RoleName(self):
        role = Role(self.Role)
        self.assertFalse(Role.RoleName(None))