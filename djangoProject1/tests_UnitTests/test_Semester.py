from django.test import TestCase
from classes.SemesterClass import SemesterClass
from .mocks import MockHandleAssignments
from ta_app.models import User, Role, Assign_User_Junction, Course, Semester

class SemesterTestCase(TestCase):
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
        self.semester = Semester.objects.create(Semester_Name="Fall 2024")

        self.validTermSpring = "Spring"
        self.validTermFall = "Fall"
        self.validTermWinter = "Winter"
        self.validTermSummer = "Summer"
        self.validYear = 2024
        self.invalidTerm = "March"
        self.invalidYear = 31330


    #create tests
    def test_CreateSemesterValid(self):
        createdSemester = SemesterClass.createSemester(
            self.validTermSpring, self.validYear, self.user
        )
        self.assertTrue(createdSemester, "Valid Semester Created [Spring, Fall, Winter, Summer] "
                                         "and valid year within -100 and +1 current year, only admin call")

    def test_CreateSemesterInvalidUser(self):
        createdSemester = SemesterClass.createSemester(
            self.validTermSpring, self.validYear, self.userTA
        )
        self.assertFalse(createdSemester, "Must be Supervisor to create semester.")

    def test_CreateSemesterNullUser(self):
        createdSemester = SemesterClass.createSemester(
            self.validTermSpring, self.validYear, None
        )
        self.assertFalse(createdSemester, "Must has a existing user.")

    def test_CreateSemesterInvalidTerm(self):
        createdSemester = SemesterClass.createSemester(
            self.invalidTerm, self.validYear, self.user
        )
        self.assertFalse(createdSemester, "Must be term of these types [Spring, Fall, Winter, Summer]")

    def test_CreateSemesterNullTerm(self):
        createdSemester = SemesterClass.createSemester(
            None, self.validYear, self.user
        )
        self.assertFalse(createdSemester, "Must exist term of these types [Spring, Fall, Winter, Summer]")

    def test_CreateSemesterInvalidYear(self):
        createdSemester = SemesterClass.createSemester(
            self.validTermSpring, self.invalidYear, self.user
        )
        self.assertFalse(createdSemester, "valid year within -100 and +1 current year")

    def test_CreateSemesterNullYear(self):
        createdSemester = SemesterClass.createSemester(
            self.validTermSpring, None, self.user
        )
        self.assertFalse(createdSemester, "valid year within -100 and +1 current year must exist")

    def test_CreateSemesterInvalidNegativeYear(self):
        createdSemester = SemesterClass.createSemester(
            self.validTermSpring, 1923, self.user
        )
        self.assertFalse(createdSemester, "valid year within -100 of current year")

    def test_CreateSemesterInvalidPositiveYear(self):
        createdSemester = SemesterClass.createSemester(
            self.validTermSpring, 2026, self.user
        )
        self.assertFalse(createdSemester, "valid year within +1 of current year")




    #delete tests
    def test_DeleteSemesterValid(self):
        deleteSemester = SemesterClass.createSemester(
            self.semester.ID, self.user
        )
        self.assertFalse(deleteSemester, "Valid Deletion Of semester requires exisitng Semester and Supervisor level")

    def test_DeleteSemesterInvalidUser(self):
        deleteSemester = SemesterClass.createSemester(
            self.semester.ID, self.userTA
        )
        self.assertFalse(deleteSemester, "Must be Supervisor level")

    def test_DeleteSemesterNonExistentSemester(self):
        deleteSemester = SemesterClass.createSemester(
            43934, self.user
        )
        self.assertFalse(deleteSemester, "Must be existing Semester")

    def test_DeleteSemesterNullSemester(self):
        deleteSemester = SemesterClass.createSemester(
            None, self.user
        )
        self.assertFalse(deleteSemester, "Must be non null exisiting Semester")

    def test_DeleteSemesterNullUser(self):
        deleteSemester = SemesterClass.createSemester(
            self.semester.ID, None
        )
        self.assertFalse(deleteSemester, "Must be Supervisor level and non-null")
