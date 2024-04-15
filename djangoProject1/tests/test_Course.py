from django.test import TestCase
from classes.CourseClass import CourseClass
from .mocks import MockHandleAssignments
from ta_app.models import User, Role, Assign_User_Junction, Course, Semester

class CourseTestCase(TestCase):
    def setUp(self):
        #self.semester = Semester.objects.create(Semester_Name="Fall 2024")
        self.Role = Role.objects.create(Role_Name="Admin")
        #self.course = Course.objects.create(Course_Name="CS 351", Course_Description="Course Test.", Course_Semester_ID_id=self.semester.id)
        self.user = User.objects.create(User_FName="Admin", User_Email="admin@uwm.edu", User_Password="admin", User_Role=self.Role)
        self.mockHandleAssignments = MockHandleAssignments()

    def test_AddCorrectAssignment(self):
        assignmentMock = self.mockHandleAssignments.create_assignment(
            "MATH - 240", "Statistical Math", "Description stuff.", self.user
        )
        self.assertTrue(assignmentMock)
