from django.test import TestCase, Client
from ta_app.models import Role, User, Course, Semester, Assign_User_Junction

class TestCoursesView(TestCase):
    def setUp(self):

        self.client = Client()
        self.semester = Semester.objects.create(Semester_Name="Fall 2024")
        self.RoleTA = Role.objects.create(Role_Name="TA")
        self.Role = Role.objects.create(Role_Name="Supervisor")
        self.RoleProf = Role.objects.create(Role_Name="Instructor")
        self.user = User.objects.create(User_FName="Supervisor", User_LName="User", User_Email="admin@uwm.edu", User_Password = "admin", User_Role = self.Role)

        self.course = Course.objects.create(Course_Name="MATH - 201", Course_Description="Calculus", Course_Semester_ID_id = self.semester.id)
        self.course2 = Course.objects.create(Course_Name="CS - 351", Course_Description="Data Structures and Algos", Course_Semester_ID_id = self.semester.id)
        self.userTA = User.objects.create(User_FName="John", User_LName="Pork", User_Email="ta@uwm.edu", User_Password = "tapassword", User_Role = self.RoleTA)
        self.userTA2 = User.objects.create(User_FName="Davis", User_LName="Clark", User_Email="ta@uwm.edu", User_Password = "tapassword", User_Role = self.RoleTA)

        Assign_User_Junction.objects.create(Course_ID=self.course, User_ID=self.userTA)
        Assign_User_Junction.objects.create(Course_ID=self.course, User_ID=self.userTA2)
        Assign_User_Junction.objects.create(Course_ID=self.course2, User_ID=self.userTA)

        self.userProf = User.objects.create(User_FName="Himmithy", User_LName="Him", User_Email="prof@uwm.edu", User_Password="password", User_Role=self.RoleProf)
        self.userProf1 = User.objects.create(User_FName="New", User_LName="Test", User_Email="prof@uwm.edu", User_Password = "prof", User_Role = self.RoleProf)

        self.junctionUserProfToCourse = Assign_User_Junction.objects.create(User_ID=self.userProf, Course_ID = self.course2)
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)

    def test_courses_list_with_assigned_users(self):
        self.client.login(username='Supervisor', password='admin')
        response = self.client.get('/courses/')

        printout = [
            "MATH - 201 - Calculus",
            "Assigned Users: John Pork (TA), Davis Clark (TA)",
            "CS - 351 - Data Structures and Algos",
            "Assigned Users: John Pork (TA), Himmithy Him (Instructor)"
        ]

        for content in printout:
            self.assertContains(response, content)

    def test_no_courses_available(self):
        Course.objects.all().delete()
        response = self.client.get('/courses/')
        self.assertIn("INVALID", response.content.decode())

    def test_instructor_sees_assigned_courses(self):
        self.client.logout()
        self.client.login(username='Himmithy', password='password')
        response = self.client.get('/courses/')
        self.assertContains(response, "CS - 351 - Data Structures and Algos")
        self.assertContains(response, "Himmithy Him (Instructor)")
        self.assertNotContains(response, "Calculus")

    def test_ta_sees_assigned_courses(self):
        self.client.logout()
        self.client.login(username='John', password='tapassword')
        response = self.client.get('/courses/')
        self.assertContains(response, "MATH - 201 - Calculus")
        self.assertContains(response, "John Pork (TA)")
        self.assertContains(response, "CS - 351 - Data Structures and Algos")
        self.assertNotContains(response, "PHYS - 101 - Physics")

    def test_unauthenticated_user_access(self):
        self.client.logout()
        response = self.client.get('/courses/')
        self.assertRedirects(response, '/login/')