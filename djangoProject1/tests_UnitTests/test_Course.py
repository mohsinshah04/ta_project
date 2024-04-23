from django.test import TestCase
from classes.CourseClass import CourseClass
from .mocks import MockHandleAssignments
from ta_app.models import User, Role, Assign_User_Junction, Course, Semester

class CourseTestCase(TestCase):
    def setUp(self):
        self.semester = Semester.objects.create(Semester_Name="Fall 2024")
        self.RoleTA = Role.objects.create(Role_Name="TA")
        self.Role = Role.objects.create(Role_Name="Supervisor")
        self.RoleProf = Role.objects.create(Role_Name="Instructor")
        self.user = User.objects.create(User_FName="Supervisor", User_LName="User", User_Email="admin@uwm.edu",
                                        User_Password="admin", User_Role=self.Role)

        self.course = Course.objects.create(Course_Name="MATH - 201", Course_Description="Calculus",
                                            Course_Semester_ID_id=self.semester.id)
        self.course2 = Course.objects.create(Course_Name="CS - 351", Course_Description="Data Structures and Algos",
                                             Course_Semester_ID_id=self.semester.id)
        self.userTA = User.objects.create(User_FName="John", User_LName="Pork", User_Email="ta@uwm.edu",
                                          User_Password="ta", User_Role=self.RoleTA)
        self.userTA2 = User.objects.create(User_FName="Davis", User_LName="Clark", User_Email="ta@uwm.edu",
                                           User_Password="ta", User_Role=self.RoleTA)

        Assign_User_Junction.objects.create(Course_ID=self.course, User_ID=self.userTA)
        Assign_User_Junction.objects.create(Course_ID=self.course, User_ID=self.userTA2)
        Assign_User_Junction.objects.create(Course_ID=self.course2, User_ID=self.userTA)

        self.userProf = User.objects.create(User_FName="Himmithy", User_LName="Him", User_Email="prof@uwm.edu", User_Password="prof", User_Role=self.RoleProf)
        self.userProf1 = User.objects.create(User_FName="New", User_LName="Test", User_Email="prof@uwm.edu",
                                            User_Password="prof", User_Role=self.RoleProf)

        self.junctionUserProfToCourse = Assign_User_Junction.objects.create(User_ID=self.userProf,
                                                                            Course_ID=self.course2)


    def test_CreateAddCorrectAssignment(self):
        """assignmentMock = MockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", "Description stuff.", self.semester.id,self.user
        )"""
        createdCourse = CourseClass.createAssignment(
            "MATH - 240", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        self.assertTrue(createdCourse, "Valid Format Course Creation Must Be [COURSE CODE (COURSE - NUMBER), COURSE NAME, COURSE DESCRIPTION, SEMESTER_ID, user)")

    def test_CreateAddInvalidCodeAssignment(self):
        """assignmentMock1 = MockHandleAssignments.createAssignment(
            "240 - Math", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        assignmentMock2 = MockHandleAssignments.createAssignment(
            "MATH240", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        assignmentMock3 = MockHandleAssignments.createAssignment(
            "MATH - 240 - Math", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )"""
        createdCourse1 = CourseClass.createAssignment(
            "240 - Math", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        createdCourse2 = CourseClass.createAssignment(
            "MATH240", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        createdCourse3 = CourseClass.createAssignment(
            "MATH - 240 - Math", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )

        self.assertFalse(createdCourse1, "Invalid Course Code: Format [Course code (COURSE - NUMBER)")
        self.assertFalse(createdCourse2, "Invalid Course Code: Format [Course code (COURSE - NUMBER)")
        self.assertFalse(createdCourse3, "Invalid Course Code: Format [Course code (COURSE - NUMBER)")

    def test_CreateNullNameAssignment(self):
        """assignmentMock = MockHandleAssignments.createAssignment(
            None, "Statistical Math", "Description stuff.", self.semester.id, self.user
        )"""
        createdCourse = CourseClass.createAssignment(
            None, "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        self.assertFalse(createdCourse, "Must Input Valid Course Code")

    def test_CreateCourseDescriptionTooShort(self):
        """assignmentMock = MockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", "Descr.", self.semester.id, self.user
        )"""
        createdCourse = CourseClass.createAssignment(
            "MATH - 240", "Statistical Math", "Descr.", self.semester.id, self.user
        )
        self.assertFalse(createdCourse, "Description must be at least 10 characters.")

    def test_CreateNullCourseDescriptionAssignment(self):
        """assignmentMock = MockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", None, self.semester.id, self.user
        )"""
        createdCourse = CourseClass.createAssignment(
            "MATH - 240", "Statistical Math", None, self.semester.id, self.user
        )
        self.assertFalse(createdCourse, "Course Description must exist.")

    def test_CreateNullCourseNameAssignment(self):
        """assignmentMock = MockHandleAssignments.createAssignment(
            "MATH - 240", None, "Here is a descirption.", self.semester.id, self.user
        )"""
        createdCourse = CourseClass.createAssignment(
            "MATH - 240", None, "Here is a descirption.", self.semester.id, self.user
        )
        self.assertFalse(createdCourse, "Course Name must exist")

    def test_CreateIsNotASupervisor(self):
        """assignmentMock = MockHandleAssignments.createAssignment(
            "MATH - 240", None, "Here is a descirption.", self.semester.id, self.userTA
        )"""
        createdCourse = CourseClass.createAssignment(
            "MATH - 240", None, "Here is a descirption.", self.semester.id, self.userTA
        )
        self.assertFalse(createdCourse, "Must be a Supervisor/Admin to create a course.")

    def test_CreateUserCallNull(self):
        """assignmentMock = MockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", "Here is a descirption.",self.semester.id, None
        )"""
        createdCourse = CourseClass.createAssignment(
            "MATH - 240", "Statistical Math", "Here is a descirption.",self.semester.id, None
        )
        self.assertFalse(createdCourse, "Must be a valid and existing User to create a course.")

    def test_EditCourseValid(self):
        """editMock = MockHandleAssignments.editAssignment(
            self.course.id, "Here is a valid desciption change", self.user
        )"""
        editCourse = CourseClass.editAssignment(
            self.course.id, "Here is a valid desciption change", self.user
        )
        self.assertTrue(editCourse, "Valid Course Edit Successfull, with exsiting course id, course description, and user.")

    def test_EditCourseNonExistingCourse(self):
        """editMock = MockHandleAssignments.editAssignment(
            1111, "Here is a valid desciption change", self.user
        )"""
        editCourse = CourseClass.editAssignment(
            1111, "Here is a valid desciption change", self.user
        )
        self.assertFalse(editCourse, "Must be an existing course id to edit a course.")

    def test_EditCourseDescriptionTooSmallIfExists(self):
        """editMock = MockHandleAssignments.editAssignment(
            self.course.id, "Here is ", self.user
        )"""
        editCourse = CourseClass.editAssignment(
            1111, "Here is a valid desciption change", self.user
        )
        self.assertFalse(editCourse, "Must be a description of at least 10 characters during edit.")

    def test_EditCourseWithNoDescription(self):
        """editMock = MockHandleAssignments.editAssignment(
            self.course.id, None, self.user
        )"""
        editCourse = CourseClass.editAssignment(
            self.course.id, None, self.user
        )
        self.assertFalse(editCourse, "A description must exist to edit.")

    def test_EditCourseInvalidPermission(self):
        """editMock = MockHandleAssignments.editAssignment(
            self.course.id, "Here is a valid description", self.userTA
        )"""
        editCourse = CourseClass.editAssignment(
            self.course.id, "Here is a valid description", self.userTA
        )
        self.assertFalse(editCourse, "Must be a Supervisor/Admin to edit a course.")

    def test_EditCourseUserCallNull(self):
        """editMock = MockHandleAssignments.editAssignment(
            self.course.id, "Here is a valid description", None
        )"""
        editCourse = CourseClass.editAssignment(
            self.course.id, "Here is a valid description", None
        )
        self.assertFalse(editCourse, "Must be a valid and existing user to edit a course.")

    def test_EditCourseCourseNull(self):
        """editMock = MockHandleAssignments.editAssignment(
            None, "Here is a valid description", self.user
        )"""
        editCourse = CourseClass.editAssignment(
            None, "Here is a valid description", self.user
        )
        self.assertFalse(editCourse, "Must be a valid and existing Course to edit a course.")

    def test_UserAssignmentTAValid(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            self.course.id, self.userTA.id, self.user
        )"""
        userAssign = CourseClass.userAssignment(
            self.course.id, self.userTA.id, self.user
        )
        self.assertTrue(userAssign, "Valid assignment of existing Course to existing user of TA role, from a valid user.")

    def test_UserAssignmentProfessorValid(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            self.course.id, self.userProf.id, self.user
        )"""
        userAssign = CourseClass.userAssignment(
            self.course.id, self.userProf1.id, self.user
        )
        self.assertTrue(userAssign, "Valid assignment of existing Course to existing user of Professor role, from a valid user.")

    def test_UserAssignmentCourseNotExist(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            11111, self.userProf.id, self.user
        )"""
        userAssign = CourseClass.userAssignment(
            11111, self.userProf.id, self.user
        )
        self.assertFalse(userAssign, "Must be an existing Course to assign a user.")

    def test_UserAssignmentUserNotExist(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            self.course.id, 33333, self.user
        )"""
        userAssign = CourseClass.userAssignment(
            self.course.id, 33333, self.user
        )
        self.assertFalse(userAssign, "Must be an existing User to assign to a course.")

    def test_UserAssignmentUserIncorrectRole(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            self.course.id, self.user.id, self.user
        )"""
        userAssign = CourseClass.userAssignment(
            self.course.id, self.user.id, self.user
        )
        self.assertFalse(userAssign, "Must be of a TA or a Professor role to be assigned to a course.")

    def test_UserAssignmentUserIncorrectRole(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            self.course.id, self.userProf.id, self.userTA
        )"""
        userAssign = CourseClass.userAssignment(
            self.course.id, self.userProf.id, self.userTA
        )
        self.assertFalse(userAssign, "Must be of a Supervisor/Admin permission user to assign.")

    def test_UserAssignmentNullCourse(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            None, self.userProf.id, self.userTA
        )"""
        userAssign = CourseClass.userAssignment(
            None, self.userProf.id, self.userTA
        )
        self.assertFalse(userAssign, "Course must exist and not null")

    def test_UserAssignmentNullUserID(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            self.course.id, None, self.userTA
        )"""
        userAssign = CourseClass.userAssignment(
            self.course.id, None, self.userTA
        )
        self.assertFalse(userAssign, "User must exit and not null")

    def test_UserAssignmentNullUserCall(self):
        """userAssignMock = MockHandleAssignments.userAssignment(
            self.course.id, self.userProf.id, None
        )"""
        userAssign = CourseClass.userAssignment(
            self.course.id, self.userProf.id, None
        )
        self.assertFalse(userAssign, "User doing the assignment must exist.")

    def test_DeleteAssignmentValid(self):
        """courseDeleteMock = MockHandleAssignments.deleteAssignment(
            self.course.id, self.user
        )"""
        courseDelete = CourseClass.deleteAssignment(
            self.course.id, self.user.id
        )
        self.assertTrue(courseDelete, "Valid Delete Assignment, existing course and existing/correct permission user.")

    def test_DeleteAssignmentCourseNotExist(self):
        """courseDeleteMock = MockHandleAssignments.deleteAssignment(
            1234, self.user
        )"""
        courseDelete = CourseClass.deleteAssignment(
            1234, self.user.id
        )
        self.assertFalse(courseDelete, "Must be a existing course to delete")

    def test_DeleteAssignmentNotPermission(self):
        """courseDeleteMock = MockHandleAssignments.deleteAssignment(
            self.course.id, self.userTA
        )"""
        courseDelete = CourseClass.deleteAssignment(
            1234, self.user.id
        )
        self.assertFalse(courseDelete, "Must be of a Supervisor/Admin permission to delete")

    def test_DeleteAssignmentCourseNull(self):
        """courseDeleteMock = MockHandleAssignments.deleteAssignment(
            None, self.user
        )"""
        courseDelete = CourseClass.deleteAssignment(
            None, self.user
        )
        self.assertFalse(courseDelete, "Must be a non null course to delete.")

    def test_DeleteAssignmentUserCallNull(self):
        """courseDeleteMock = MockHandleAssignments.deleteAssignment(
            self.course.id, None
        )"""
        courseDelete = CourseClass.deleteAssignment(
            self.course.id, None
        )
        self.assertFalse(courseDelete, "Must be a user non null to delete")




    def test_viewAllAssignments(self):
        """result = MockHandleAssignments.viewAllAssignments(
            self.user
        )"""
        result = CourseClass.viewAllAssignments(self.user)

        self.assertIn("MATH - 201", result)
        self.assertIn("John Pork (TA), Davis Clark (TA)", result)
        self.assertIn("CS - 351", result)
        self.assertIn("John Pork (TA)", result)
        self.assertIn("Instructor", result)


    def test_viewAllAssignmentsPermissionTA(self):
        """result = MockHandleAssignments.viewAllAssignments(
            self.userTA
        )"""
        result = CourseClass.viewAllAssignments(self.userTA2)
        self.assertIn("MATH - 201", result)
        self.assertIn("John Pork (TA), Davis Clark (TA)", result)
        self.assertIn("CS - 351", result)
        self.assertIn("John Pork (TA)", result)
        self.assertNotIn("Instructor", result)


    def test_viewAllAssignmentsPermissionProfessor(self):
        """result = MockHandleAssignments.viewAllAssignments(
            self.userProf
        )"""
        result = CourseClass.viewAllAssignments(self.userProf)
        self.assertIn("MATH - 201", result)
        self.assertIn("John Pork (TA), Davis Clark (TA)", result)
        self.assertIn("CS - 351", result)
        self.assertIn("John Pork (TA)", result)
        self.assertIn("Instructor", result)


    def test_viewAllAssignmentsUserNotExist(self):
        result = MockHandleAssignments.viewAllAssignments(
            44444
        )
        result = CourseClass.viewAllAssignments(44444)
        self.assertEqual(result, "INVALID", "Must be existing user to view assignments.")

    def test_viewAllAssignmentsUserNull(self):
        """result = MockHandleAssignments.viewAllAssignments(
            None
        )"""
        result = CourseClass.viewAllAssignments(None)
        self.assertEqual(result, "INVALID", "Must be a non null user to view assignments")




    def test_viewUserAssignmentAsAdminOnTA(self):
        """result = MockHandleAssignments.viewUserAssignments(
                    self.userTA, self.user
        )"""

        result = CourseClass.viewUserAssignments(
            self.userTA, self.user
        )
        self.assertIn("Assigned Users:", result)
        self.assertIn("Instructor", result)
        self.assertIn("MATH - 201", result)
        self.assertIn("CS - 351", result)
        self.assertIn("John Pork (TA)", result)

    def test_viewUserAssignmentAsAdminOnProf(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userProf, self.user
        )"""
        result = CourseClass.viewUserAssignments(
            self.userProf, self.user
        )

        self.assertIn("Assigned Users:", result)
        self.assertIn("CS - 351", result)
        self.assertIn("Himmithy Him (Instructor)", result)

    def test_viewUserAssignmentAsTAOnSelf(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userTA, self.userTA
        )"""
        result = CourseClass.viewUserAssignments(
            self.userTA, self.userTA
        )
        self.assertIn("Assigned Users:", result)
        self.assertIn("Instructor", result)
        self.assertIn("MATH - 201", result)
        self.assertIn("CS - 351", result)
        self.assertIn("John Pork (TA)", result)

    def test_viewUserAssignmentAsTAOnDifferentTA(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userTA2, self.userTA
        )"""
        result = CourseClass.viewUserAssignments(
            self.userTA2, self.userTA
        )
        self.assertIn("Assigned Users:", result)
        self.assertIn("MATH - 201", result)
        self.assertIn("Davis Clark (TA)", result)

    def test_viewUserAssignmentAsTAOnProfessorInSameCourse(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userProf, self.userTA
        )"""
        result = CourseClass.viewUserAssignments(
            self.userProf, self.userTA
        )
        self.assertIn("Assigned Users:", result)
        self.assertIn("CS - 351", result)
        self.assertIn("John Pork (TA)", result)

    def test_viewUserAssignmentAsProfOnProfessorInNotCourse(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userProf, self.userTA2
        )"""
        result = CourseClass.viewUserAssignments(
            self.userProf, self.userTA2
        )
        self.assertIn("INVALID", result)

    def test_viewUserAssignmentAsProfOnSelf(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userProf, self.userProf
        )"""
        result = CourseClass.viewUserAssignments(
            self.userProf, self.userProf
        )
        self.assertIn("Assigned Users:", result)
        self.assertIn("Instructor", result)
        self.assertNotIn("MATH - 201", result)
        self.assertIn("CS - 351", result)
        self.assertIn("Himmithy Him (Instructor)", result)

    def test_viewUserAssignmentAsProfOnTA(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userTA, self.userProf
        )"""
        result = CourseClass.viewUserAssignments(
            self.userTA, self.userProf
        )
        self.assertIn("Assigned Users:", result)
        self.assertIn("Instructor", result)
        self.assertIn("MATH - 201", result)
        self.assertIn("CS - 351", result)
        self.assertIn("Himmithy Him (Instructor)", result)
        self.assertIn("John Pork (TA)", result)

    def test_viewUserAssignmentAsProfOnProf(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userTA, self.userProf
        )"""
        result = CourseClass.viewUserAssignments(
            self.userTA, self.userProf
        )
        self.assertIn("Assigned Users:", result)
        self.assertIn("Instructor", result)
        self.assertIn("MATH - 201", result)
        self.assertIn("CS - 351", result)
        self.assertIn("Himmithy Him (Instructor)", result)
        self.assertIn("John Pork (TA)", result)


    def test_viewUserAssignmentUserNotExist(self):
        """result = MockHandleAssignments.viewUserAssignments(
            3333, self.user
        )"""
        result = CourseClass.viewUserAssignments(
            3333, self.user
        )
        self.assertIn(result, "INVALID", "Must be a valid existing userID")

    def test_viewUserAssignmentCallingUserNotExist(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userTA, 33333
        )"""
        result = CourseClass.viewUserAssignments(
            self.userTA, 33333
        )
        self.assertIn(result, "INVALID", "Must be a valid existing userID")


    def test_viewUserAssignmentNullCallingUser(self):
        """result = MockHandleAssignments.viewUserAssignments(
            self.userTA, None
        )"""
        viewUserAll = CourseClass.viewUserAssignments(
            self.userTA, None
        )
        self.assertEqual(viewUserAll, "INVALID", "Must be a non null userID")



