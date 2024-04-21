from django.test import TestCase, Client
from ta_app.models import Role, User, Course, Semester, Assign_User_Junction
from django.urls import reverse
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


class TestCoursesCreate(TestCase):
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

        self.legalCode = "COMPSCI - 351"
        self.legalCourseName = "Data Structures and Algorithims"
        self.legalCourseDescription = "Blah blah blah"
        self.legalSemesterYear = 2024
        self.legalSemesterMonth = "Spring"

        self.user.save()
        self.userTA.save()
        self.userTA2.save()
        self.userProf.save()
        self.userProf1.save()


    def test_coursesCreateWithAssignedUsersExistingSemester(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName, "courseDescription": self.legalCourseDescription, "semester": self.semester.id})
        self.assertEqual(response.url, "/courses/")

    def test_coursesCreateWithAssignedUsersNewSemester(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear, "semesterMonth": self.legalSemesterMonth, "semester": "new"})
        self.assertEqual(response.url, "/courses/")

    def test_coursesCreateWithAssignedInvalidUserNewSemester(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": "new"})
        self.assertEqual(response.context['message'], "INVALID")

    def test_coursesCreateWithAssignedInvalidUserExistingSemester(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": self.semester.id})
        self.assertEqual(response.context['message'], "INVALID")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidCode(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": "33je9", "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": self.semester.id})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidYear(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": 2026,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": "new"})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidMonths(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": 2022,
                                                       "semesterMonth": "mmm", "semester": "new"})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidDescription(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": "d",
                                                       "semesterYear": 2022,
                                                       "semesterMonth": "mmm", "semester": self.semester.id})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateSemestersAppear(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.get("/courseCreate/", {"id": self.user.id})
        printout = [
            'Fall 2024'
        ]
        content = response.context['semesters']
        for name in printout:
            self.assertIn(name, content)

    def test_coursesCreateSemestersAppearInvalidUser(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password})
        response = self.client.get("/courseCreate/", {"id": self.userTA.id})
        self.assertEqual(response.url, "/courses/")

    def test_coursesCreateSemestersValidCreateWithStrings(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": "deeeeeeeee",
                                                       "semesterYear": "2022",
                                                       "semesterMonth": "Spring", "semester": "new"})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")


class TestCoursesEdit(TestCase):
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



        self.userProf = User.objects.create(User_FName="Himmithy", User_LName="Him", User_Email="prof@uwm.edu", User_Password="password", User_Role=self.RoleProf)
        self.userProf1 = User.objects.create(User_FName="New", User_LName="Test", User_Email="prof@uwm.edu", User_Password = "prof", User_Role = self.RoleProf)

        self.junctionUserProfToCourse = Assign_User_Junction.objects.create(User_ID=self.userProf, Course_ID = self.course2)

        self.legalCode = "COMPSCI - 351"
        self.legalCourseName = "Data Structures and Algorithims"
        self.legalCourseDescription = "Blah blah blah"
        self.legalSemesterYear = 2024
        self.legalSemesterMonth = "Spring"

        self.user.save()
        self.userTA.save()
        self.userTA2.save()
        self.userProf.save()
        self.userProf1.save()
    def test_EditCourseValid(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post('/courseEdit/', {
            'course_id': self.course.id,
            'courseCode': "MATH",
            'courseFullName': "201",
            'courseDescription': 'Calculus',
            'semester': self.semester.id,
            'assignedUsers': [self.userTA.id]
        })
        self.course.refresh_from_db()
        expected_name = "MATH - 201"
        self.assertEqual(self.course.Course_Name, expected_name)
        self.assertEqual(self.course.Course_Description, 'Calculus')
        self.assertTrue(Assign_User_Junction.objects.filter(User_ID=self.userTA, Course_ID = self.course).exists())

    def test_EditCourseInvalidUser(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password})
        response = self.client.post('/courseEdit/', {
            'course_id': self.course.id,
            'courseCode': "MATH",
            'courseFullName': "201",
            'courseDescription': 'Calculus',
            'semester': self.semester.id
        })
        self.assertEqual(response.url, "/courses/")

    def test_EditCourseRemoveAllUsers(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post('/courseEdit/', {
            'course_id': self.course.id,
            'courseCode': "MATH",
            'courseFullName': "201",
            'courseDescription': 'Calculus',
            'semester': self.semester.id,
            'assignedUsers': [self.userTA.id]
        })
        self.assertTrue(Assign_User_Junction.objects.filter(User_ID=self.userTA, Course_ID=self.course).exists())
        response = self.client.post('/courseEdit/', {
            'course_id': self.course.id,
            'courseCode': "MATH",
            'courseFullName': "201",
            'courseDescription': 'Calculus',
            'semester': self.semester.id,
            'assignedUsers': []
        })
        self.course.refresh_from_db()
        expected_name = "MATH - 201"
        self.assertEqual(self.course.Course_Name, expected_name)
        self.assertEqual(self.course.Course_Description, 'Calculus')
        self.assertFalse(Assign_User_Junction.objects.filter(User_ID=self.userTA, Course_ID = self.course).exists())






"""
    def test_post_edit_course(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post('/courseEdit/', {
            'course_id': self.course.id,
            'courseCode': 'CS - 352',
            'courseFullName': 'Advanced Data Structures',
            'courseDescription': 'A deeper look into data structures',
            'semester': self.semester.id
        })
        self.course.refresh_from_db()
        expected_name = "CS - 352 - Advanced Data Structures"
        self.assertEqual(self.course.Course_Name, expected_name)
        self.assertEqual(self.course.Course_Description, 'A deeper look into data structures')




    def test_coursesCreateWithAssignedUsersNewSemester(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear, "semesterMonth": self.legalSemesterMonth, "semester": "new"})
        self.assertEqual(response.url, "/courses/")

    def test_coursesCreateWithAssignedInvalidUserNewSemester(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": "new"})
        self.assertEqual(response.context['message'], "INVALID")

    def test_coursesCreateWithAssignedInvalidUserExistingSemester(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": self.semester.id})
        self.assertEqual(response.context['message'], "INVALID")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidCode(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": "33je9", "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": self.legalSemesterYear,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": self.semester.id})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidYear(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": 2026,
                                                       "semesterMonth": self.legalSemesterMonth, "semester": "new"})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidMonths(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": self.legalCourseDescription,
                                                       "semesterYear": 2022,
                                                       "semesterMonth": "mmm", "semester": "new"})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateWithAssignedUserExistingSemesterInvalidDescription(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": "d",
                                                       "semesterYear": 2022,
                                                       "semesterMonth": "mmm", "semester": self.semester.id})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")

    def test_coursesCreateSemestersAppear(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.get("/courseCreate/", {"id": self.user.id})
        printout = [
            'Fall 2024'
        ]
        content = response.context['semesters']
        for name in printout:
            self.assertIn(name, content)

    def test_coursesCreateSemestersAppearInvalidUser(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password})
        response = self.client.get("/courseCreate/", {"id": self.userTA.id})
        self.assertEqual(response.url, "/courses/")

    def test_coursesCreateSemestersValidCreateWithStrings(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password})
        response = self.client.post("/courseCreate/", {"courseCode": self.legalCode, "courseName": self.legalCourseName,
                                                       "courseDescription": "deeeeeeeee",
                                                       "semesterYear": "2022",
                                                       "semesterMonth": "Spring", "semester": "new"})
        self.assertEqual(response.context['error'], "Invalid Format: Try Again")
        
"""