from django.test import TestCase, Client

from ta_app.models import Role, User, Course, Semester, Assign_User_Junction, Section


class TestSectionsView(TestCase):
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


    def test_sectionsViewPageExists(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)
        response = self.client.get('/sections/',{"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_sectionsViewAsInstuctorValid(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.userProf.id]
        }
        response = self.client.post('/sectionCreate/', form_data)
        self.assertEqual(response.status_code, 302)

        self.client.post("/", {"Email": self.userProf.User_Email, "Password": self.userProf.User_Password}, follow=True)
        response = self.client.get('/sections/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '001')

    def test_sectionsViewAsTAValid(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.userTA.id]
        }
        response = self.client.post('/sectionCreate/', form_data)
        self.assertEqual(response.status_code, 302)

        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password}, follow=True)
        response = self.client.get('/sections/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '001')

    def test_sectionViewNoSections(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password}, follow=True)
        response = self.client.get('/sections/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No sections available')

    def test_sectionViewInvalidUser(self):
        response = self.client.get('/sections/')
        self.assertTrue(response.status_code, 302)

    def test_sectionViewNoAssignment(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password}, follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': []
        }
        response = self.client.post('/sectionCreate/', form_data)
        self.assertEqual(response.status_code, 302)

        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password}, follow=True)
        response = self.client.get('/sections/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')


class TestSectionCreate(TestCase):
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
        self.userProf1 = User.objects.create(User_FName="New", User_LName="Test", User_Email="pro@uwm.edu", User_Password = "profgfdfd", User_Role = self.RoleProf)

        self.junctionUserProfToCourse = Assign_User_Junction.objects.create(User_ID=self.userProf, Course_ID = self.course2)

        self.user.save()
        self.userTA.save()
        self.userTA2.save()
        self.userProf.save()
        self.userProf1.save()




    def test_sectionsCreatePageExists(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)
        response = self.client.get('/sectionCreate/', {"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_sectionsCreateValidAsSupervisor(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)
        response = self.client.get('/sectionCreate/', {"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.user.id]
        }
        response = self.client.post('/sectionCreate/', form_data)
        self.assertEqual(response.status_code, 302)
        section = Section.objects.first()
        self.assertIsNotNone(section)
        self.assertEqual(section.Section_Number, '001')
        self.assertEqual(section.Meets_Days, "['M', 'W', 'F']")
        self.assertEqual(section.Credits, 3)

    def test_sectionsCreateValidAsInstructor(self):
        self.client.post("/", {"Email": self.userProf.User_Email, "Password": self.userProf.User_Password}, follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.userProf.id]
        }
        response = self.client.post('/sectionCreate/', form_data)
        self.assertEqual(response.status_code, 302)

        section = Section.objects.first()
        self.assertIsNotNone(section)
        self.assertEqual(section.Section_Number, '001')
        self.assertEqual(section.Meets_Days, "['M', 'W', 'F']")
        self.assertEqual(section.Credits, 3)

    def test_sectionsCreateMissingData(self):
        self.client.post("/", {"Email": self.userProf.User_Email, "Password": self.userProf.User_Password}, follow=True)

        form_data = {
            'course': self.course.id,
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.userProf.id]
        }
        response = self.client.post('/sectionCreate/', form_data)
        self.assertEqual(response.status_code, 200)

        section = Section.objects.first()
        self.assertIsNone(section)

    def test_sectionsCreateInvalid(self):
        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password}, follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.userTA.id]
        }
        response = self.client.post('/sectionCreate/', form_data)
        self.assertEqual(response.status_code, 200)

        section = Section.objects.first()
        self.assertIsNone(section)

    def test_sectionsCreateValidAsSupervisorSimilar(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)
        response = self.client.get('/sectionCreate/', {"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.user.id]
        }

        response = self.client.post('/sectionCreate/', form_data)

        form_data = {
            'course': self.course.id,
            'section_num': '0012',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users[]': [self.user.id]
        }

        response2 = self.client.post('/sectionCreate/', form_data)


        self.assertEqual(response.status_code, 302)

        section = Section.objects.first()
        self.assertIsNotNone(section)
        self.assertEqual(section.Section_Number, '001')
        self.assertEqual(section.Meets_Days, "['M', 'W', 'F']")
        self.assertEqual(section.Credits, 3)


class TestSectionEdit(TestCase):
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

    def test_sectionsEditPageExists(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)
        response = self.client.get('/sectionCreate/', {"id": self.user.id}, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_sectionEditSupervisor(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users': [self.user.id]
        }
        self.client.post('/sectionCreate/', form_data)

        section_id = Section.objects.first().id

        edit_form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users': [self.user.id, self.userTA.id],
            'section_id' : section_id
        }
        response = self.client.post('/sectionEdit/', edit_form_data)
        self.assertEqual(response.status_code, 302)

        section = Section.objects.get(id=section_id)
        assigned_users = Assign_User_Junction.objects.filter(Section_ID=section)
        assigned_user_ids = [assignment.User_ID.id for assignment in assigned_users]
        self.assertIn(self.user.id, assigned_user_ids)
        self.assertIn(self.userTA.id, assigned_user_ids)
    def test_sectionsEditInstructor(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users': [self.user.id]
        }
        self.client.post('/sectionCreate/', form_data)

        section_id = Section.objects.first().id

        self.client.post("/", {"Email": self.userProf.User_Email, "Password": self.userProf.User_Password},
                         follow=True)
        edit_form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users': [self.user.id, self.userTA.id],
            'section_id' : section_id
        }
        response = self.client.post('/sectionEdit/', edit_form_data)
        self.assertEqual(response.status_code, 302)

        section = Section.objects.get(id=section_id)
        assigned_users = Assign_User_Junction.objects.filter(Section_ID=section)
        assigned_user_ids = [assignment.User_ID.id for assignment in assigned_users]
        self.assertIn(self.user.id, assigned_user_ids)
        self.assertIn(self.userTA.id, assigned_user_ids)

    def test_sectionEditInvalidUser(self):
        self.client.post("/", {"Email": self.user.User_Email, "Password": self.user.User_Password},
                         follow=True)

        form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users': [self.user.id]
        }
        self.client.post('/sectionCreate/', form_data)

        section_id = Section.objects.first().id

        self.client.post("/", {"Email": self.userTA.User_Email, "Password": self.userTA.User_Password},
                         follow=True)
        edit_form_data = {
            'course': self.course.id,
            'section_num': '001',
            'section_type': 'Lecture',
            'meets_days': ['M', 'W', 'F'],
            'campus': 'Main Campus',
            'start_date': '2023-09-01',
            'end_date': '2023-12-15',
            'credits': 3,
            'start_time': '09:00',
            'end_time': '10:15',
            'building_name': 'Tech Building',
            'room_number': '101',
            'assigned_users': [self.user.id, self.userTA.id],
            'section_id' : section_id
        }
        response = self.client.post('/sectionEdit/', edit_form_data)
        self.assertEqual(response.status_code, 302)

        section = Section.objects.get(id=section_id)
        assigned_users = Assign_User_Junction.objects.filter(Section_ID=section)
        assigned_user_ids = [assignment.User_ID.id for assignment in assigned_users]
        self.assertEqual([], assigned_user_ids)
