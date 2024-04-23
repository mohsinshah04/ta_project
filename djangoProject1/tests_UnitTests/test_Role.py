from django.test import TestCase
from classes.RoleClass import RoleClass
from .mocks import MockHandleAssignments
from ta_app.models import User, Role, Assign_User_Junction

class RoleTest(TestCase):
    def setUp(self):
        self.Role = Role.objects.create(Role_Name="Supervisor")
        self.user = User.objects.create(User_FName="Supervisor", User_LName="User", User_Email="admin@uwm.edu",
                                        User_Password="admin", User_Role=self.Role)

    # create role tests
    def test_createTA(self):
        output = RoleClass.create_role("TA", self.user)
        self.assertTrue(output)

    def test_createSupervisor(self):
        Role.objects.filter(id=self.Role.id).delete()
        output = RoleClass.create_role("Supervisor", self.user)
        self.assertTrue(output)

    def test_createInstructor(self):
        output = RoleClass.create_role("Instructor", self.user)
        self.assertTrue(output)

    def test_createUnexisting(self):
        output = RoleClass.create_role("No", self.user)
        self.assertFalse(output)


    # delete role tests
    def test_deleteTA(self):
        self.Role = Role.objects.create(Role_Name="TA")
        output = RoleClass.delete_role(self.Role, self.user)
        self.assertTrue(output)

    def test_deleteSupervisor(self):
        output = RoleClass.delete_role(self.Role, self.user)
        self.assertTrue(output)

    def test_deleteInstructor(self):
        self.Role = Role.objects.create(Role_Name="Supervisor")
        output = RoleClass.delete_role(self.Role, self.user)
        self.assertTrue(output)

    def test_deleteUnexisting(self):
        output = RoleClass.delete_role("ff", self.user)
        self.assertFalse(output)
