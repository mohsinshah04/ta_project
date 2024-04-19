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
        self.userTA2 = User.objects.create(User_FName="Davis", User_LName="Clark", User_Email="ta2@uwm.edu", User_Password = "ta2password", User_Role = self.RoleTA)

        Assign_User_Junction.objects.create(Course_ID=self.course, User_ID=self.userTA)
        Assign_User_Junction.objects.create(Course_ID=self.course, User_ID=self.userTA2)
        Assign_User_Junction.objects.create(Course_ID=self.course2, User_ID=self.userTA)

        self.userProf = User.objects.create(User_FName="Himmithy", User_LName="Him", User_Email="prof@uwm.edu", User_Password="password", User_Role=self.RoleProf)
        self.userProf1 = User.objects.create(User_FName="New", User_LName="Test", User_Email="prof@uwm.edu", User_Password = "prof", User_Role = self.RoleProf)

        self.junctionUserProfToCourse = Assign_User_Junction.objects.create(User_ID=self.userProf, Course_ID = self.course2)

        self.user.save()
        self.userTA.save()
        self.userTA2.save()
        self.userProf.save()
        self.userProf1.save()


    def test_coursesListWithAssignedUsers(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)
        response = self.client.get('/courses/',{"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        printout = [
            "MATH - 201 - Calculus",
            "Assigned Users: John Pork (TA), Davis Clark (TA)",
            "CS - 351 - Data Structures and Algos",
            "Assigned Users: John Pork (TA), Himmithy Him (Instructor)"
        ]

        for content in printout:
            self.assertContains(response, content)

    def test_coursesListWithAssignedUsersAsFirstTA(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password}, follow=True)
        response = self.client.get('/courses/',{"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        printout = [
            "MATH - 201 - Calculus",
            "Assigned Users: John Pork (TA), Davis Clark (TA)",
            "CS - 351 - Data Structures and Algos",
            "Assigned Users: John Pork (TA), Himmithy Him (Instructor)"
        ]

        for content in printout:
            self.assertContains(response, content)

    def test_coursesListWithAssignedUsersAsSecondTA(self):
        self.client.post("/", {"Email": self.userTA2.User_Email, "Password": self.userTA2.User_Password}, follow=True)
        response = self.client.get('/courses/', {"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        printout = [
            "MATH - 201 - Calculus",
            "Assigned Users: John Pork (TA), Davis Clark (TA)"
        ]

        for content in printout:
            self.assertContains(response, content)


    def test_noCoursesAvailable(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)
        Course.objects.all().delete()
        response = self.client.get('/courses/', {"id": self.user.id}, follow=True)
        printout = [
            "No courses found"
        ]

        for content in printout:
            self.assertContains(response, content)

    def test_NotLoggedIn(self):
        response = self.client.get('/courses/', {"id": self.user.id}, follow=True)
        self.assertContains(response, "Please log in to view this page.")
