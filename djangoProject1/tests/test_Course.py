from django.test import TestCase
from classes.CourseClass import CourseClass
from .mocks import MockHandleAssignments
from ta_app.models import User, Role, Assign_User_Junction, Course, Semester

class CourseTestCase(TestCase):
    def setUp(self):
        self.semester = Semester.objects.create(Semester_Name="Fall 2024")
        self.Role = Role.objects.create(Role_Name="Admin")
        self.RoleTA = Role.objects.create(Role_Name="TA")
        self.RoleProf = Role.objects.create(Role_Name="Professor")
        self.course2 = Course.objects.create(Course_Name="CS 444", Course_Description="Course Test.", Course_Semester_ID_id=self.semester.id)
        self.course = Course.objects.create(Course_Name="CS 351", Course_Description="Course Test.", Course_Semester_ID_id=self.semester.id)
        self.user = User.objects.create(User_FName="Admin", User_Email="admin@uwm.edu", User_Password="admin", User_Role=self.Role)
        self.userTA = User.objects.create(User_FName="TA", User_Email="ta@uwm.edu", User_Password="ta", User_Role=self.RoleTA)
        self.userTA2 = User.objects.create(User_FName="TA2", User_Email="ta2@uwm.edu", User_Password="ta2",User_Role=self.RoleTA)
        self.userProf = User.objects.create(User_FName="TA", User_Email="ta@uwm.edu", User_Password="ta", User_Role=self.RoleProf)
        self.junctionUserTAToCourse = Assign_User_Junction.objects.create(User_ID=self.userTA, Course_ID=self.course)
        self.junctionUserTAToCourse2 = Assign_User_Junction.objects.create(User_ID=self.userTA2, Course_ID=self.course2)
        self.junctionUserProfToCourse = Assign_User_Junction.objects.create(User_ID=self.userProf, Course_ID=self.course)
        self.mockHandleAssignments = MockHandleAssignments()
        """self.course = CourseClass()"""

    def test_CreateAddCorrectAssignment(self):
        assignmentMock = self.mockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", "Description stuff.", self.semester.id,self.user
        )
        """createdCourse = CourseClass.createAssignment("MATH - 240", "Statistical Math", "Description stuff.", self.semester.id, self.user)
        """
        self.assertTrue(assignmentMock, "Valid Format Course Creation Must Be [COURSE CODE (COURSE - NUMBER), COURSE NAME, COURSE DESCRIPTION, SEMESTER_ID, user)")

    def test_CreateAddInvalidCodeAssignment(self):
        assignmentMock1 = self.mockHandleAssignments.createAssignment(
            "240 - Math", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        assignmentMock2 = self.mockHandleAssignments.createAssignment(
            "MATH240", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        assignmentMock3 = self.mockHandleAssignments.createAssignment(
            "MATH - 240 - Math", "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        self.assertFalse(assignmentMock1, "Invalid Course Code: Format [Course code (COURSE - NUMBER)")
        self.assertFalse(assignmentMock2, "Invalid Course Code: Format [Course code (COURSE - NUMBER)")
        self.assertFalse(assignmentMock3, "Invalid Course Code: Format [Course code (COURSE - NUMBER)")

    def test_CreateNullNameAssignment(self):
        assignmentMock1 = self.mockHandleAssignments.createAssignment(
            None, "Statistical Math", "Description stuff.", self.semester.id, self.user
        )
        self.assertFalse(assignmentMock1, "Must Input Valid Course Code")

    def test_CreateCourseDescriptionTooShort(self):
        assignmentMock1 = self.mockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", "Descr.", self.semester.id, self.user
        )
        self.assertFalse(assignmentMock1, "Description must be at least 10 characters.")

    def test_CreateNullCourseDescriptionAssignment(self):
        assignmentMock1 = self.mockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", None, self.semester.id, self.user
        )
        self.assertFalse(assignmentMock1, "Course Description must exist.")

    def test_CreateNullCourseNameAssignment(self):
        assignmentMock1 = self.mockHandleAssignments.createAssignment(
            "MATH - 240", None, "Here is a descirption.", self.semester.id, self.user
        )
        self.assertFalse(assignmentMock1, "Course Name must exist")

    def test_CreateIsNotASupervisor(self):
        assignmentMock1 = self.mockHandleAssignments.createAssignment(
            "MATH - 240", None, "Here is a descirption.", self.semester.id, self.userTA
        )
        self.assertFalse(assignmentMock1, "Must be a Supervisor/Admin to create a course.")

    def test_CreateUserCallNull(self):
        assignmentMock1 = self.mockHandleAssignments.createAssignment(
            "MATH - 240", "Statistical Math", "Here is a descirption.",self.semester.id, None
        )
        self.assertFalse(assignmentMock1, "Must be a valid and existing User to create a course.")

    def test_EditCourseValid(self):
        editMock1 = self.mockHandleAssignments.editAssignment(
            self.course.id, "Here is a valid desciption change", self.user
        )
        self.assertTrue(editMock1, "Valid Course Edit Successfull, with exsiting course id, course description, and user.")

    def test_EditCourseNonExistingCourse(self):
        editMock1 = self.mockHandleAssignments.editAssignment(
            1111, "Here is a valid desciption change", self.user
        )
        self.assertFalse(editMock1, "Must be an existing course id to edit a course.")

    def test_EditCourseDescriptionTooSmallIfExists(self):
        editMock1 = self.mockHandleAssignments.editAssignment(
            self.course.id, "Here is ", self.user
        )
        self.assertFalse(editMock1, "Must be a description of at least 10 characters during edit.")

    def test_EditCourseWithNoDescription(self):
        editMock1 = self.mockHandleAssignments.editAssignment(
            self.course.id, None, self.user
        )
        self.assertFalse(editMock1, "A description must exist to edit.")

    def test_EditCourseInvalidPermission(self):
        editMock1 = self.mockHandleAssignments.editAssignment(
            self.course.id, "Here is a valid description", self.userTA
        )
        self.assertFalse(editMock1, "Must be a Supervisor/Admin to edit a course.")

    def test_EditCourseUserCallNull(self):
        editMock1 = self.mockHandleAssignments.editAssignment(
            self.course.id, "Here is a valid description", None
        )
        self.assertFalse(editMock1, "Must be a valid and existing user to edit a course.")

    def test_EditCourseCourseNull(self):
        editMock1 = self.mockHandleAssignments.editAssignment(
            None, "Here is a valid description", self.user
        )
        self.assertFalse(editMock1, "Must be a valid and existing Course to edit a course.")

    def test_UserAssignmentTAValid(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            self.course.id, self.userTA.id, self.user
        )
        self.assertTrue(userAssignMock1, "Valid assignment of existing Course to existing user of TA role, from a valid user.")

    def test_UserAssignmentProfessorValid(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            self.course.id, self.userProf.id, self.user
        )
        self.assertTrue(userAssignMock1, "Valid assignment of existing Course to existing user of Professor role, from a valid user.")

    def test_UserAssignmentCourseNotExist(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            11111, self.userProf.id, self.user
        )
        self.assertFalse(userAssignMock1, "Must be an existing Course to assign a user.")

    def test_UserAssignmentUserNotExist(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            self.course.id, 33333, self.user
        )
        self.assertFalse(userAssignMock1, "Must be an existing User to assign to a course.")

    def test_UserAssignmentUserIncorrectRole(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            self.course.id, self.user.id, self.user
        )
        self.assertFalse(userAssignMock1, "Must be of a TA or a Professor role to be assigned to a course.")

    def test_UserAssignmentUserIncorrectRole(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            self.course.id, self.userProf.id, self.userTA
        )
        self.assertFalse(userAssignMock1, "Must be of a Supervisor/Admin permission user to assign.")

    def test_UserAssignmentNullCourse(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            None, self.userProf.id, self.userTA
        )
        self.assertFalse(userAssignMock1, "Course must exist and not null")

    def test_UserAssignmentNullUserID(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            self.course.id, None, self.userTA
        )
        self.assertFalse(userAssignMock1, "User must exit and not null")

    def test_UserAssignmentNullUserCall(self):
        userAssignMock1 = self.mockHandleAssignments.userAssignment(
            self.course.id, self.userProf.id, None
        )
        self.assertFalse(userAssignMock1, "User doing the assignment must exist.")

    def test_DeleteAssignmentValid(self):
        courseDeleteMock1 = self.mockHandleAssignments.deleteAssignment(
            self.course.id, self.user
        )
        self.assertTrue(courseDeleteMock1, "Valid Delete Assignment, existing course and existing/correct permission user.")

    def test_DeleteAssignmentCourseNotExist(self):
        courseDeleteMock1 = self.mockHandleAssignments.deleteAssignment(
            1234, self.user
        )
        self.assertFalse(courseDeleteMock1, "Must be a existing course to delete")

    def test_DeleteAssignmentNotPermission(self):
        courseDeleteMock1 = self.mockHandleAssignments.deleteAssignment(
            self.course.id, self.userTA
        )
        self.assertFalse(courseDeleteMock1, "Must be of a Supervisor/Admin permission to delete")

    def test_DeleteAssignmentCourseNull(self):
        courseDeleteMock1 = self.mockHandleAssignments.deleteAssignment(
            None, self.user
        )
        self.assertFalse(courseDeleteMock1, "Must be a non null course to delete.")

    def test_DeleteAssignmentUserCallNull(self):
        courseDeleteMock1 = self.mockHandleAssignments.deleteAssignment(
            self.course.id, None
        )
        self.assertFalse(courseDeleteMock1, "Must be a user non null to delete")

    def test_viewAllAssignments(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            self.course.id, self.userTA.id, self.user
        )
        self.assertEqual(viewAllMock1, "CS 351 - Course Test.",
                         "Valid View All Assignments, requires valid courses, users, and correct user call permission level. "
                         "Output COURSE CODE - COURSE NAME")

    def test_viewAllAssignmentsNotPermissionTA(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            self.course.id, self.userTA.id, self.userTA
        )
        self.assertEqual(viewAllMock1, "INVALID", "Must be of Supervisor/Admin permission to view all assignments.")

    def test_viewAllAssignmentsNotPermissionProfessor(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            self.course.id, self.userTA.id, self.userProf
        )
        self.assertEqual(viewAllMock1, "INVALID", "Must be of Supervisor/Admin permission to view all assignments.")

    def test_viewAllAssignmentsCourseNotExist(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            1234, self.userTA.id, self.user
        )
        self.assertEqual(viewAllMock1, "INVALID", "Must be an existing courses to view assignments.")

    def test_viewAllAssignmentsUserNotExist(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            self.course.id, 4313, self.user
        )
        self.assertEqual(viewAllMock1, "INVALID", "Must be existing user to view assignments.")

    def test_viewAllAssignmentsUserNull(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            self.course.id, None, self.user
        )
        self.assertEqual(viewAllMock1, "INVALID", "Must be a non null user to view assignments")

    def test_viewAllAssignmentsCourseNull(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            None, self.userTA.id, self.user
        )
        self.assertEqual(viewAllMock1, "INVALID", "Must be a non null course to view assignments")

    def test_viewAllAssignmentsUserCallNull(self):
        viewAllMock1 = self.mockHandleAssignments.viewAllAssignments(
            self.course.id, self.userTA.id, None
        )
        self.assertEqual(viewAllMock1, "INVALID", "Mustbe a none null user calling to view assignments")

    def test_viewUserAssignmentAsSamePermission(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, self.userTA.id, self.userTA
        )
        self.assertEqual(viewUserAllMock1, "TA, null, CS 351",
                         "Valid User Viewing Assignments, valid course, valid user (of any permission), "
                         "calling user TA can view themselves, Supervisor/TA can view more")

    def test_viewUserAssignmentAsSupervisor(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, self.userTA.id, self.user
        )
        self.assertEqual(viewUserAllMock1, "TA, null, CS 351", "Valid Supervisor viewing TA assignments.")

    def test_viewUserAssignmentAsWrongPermission(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, self.userTA.id, self.userTA2
        )
        self.assertEqual(viewUserAllMock1, "INVALID", "TA cannot view other TA course assignments.")

    def test_viewUserAssignmentAsProfessor(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, self.userProf.id, self.userProf
        )
        self.assertEqual(viewUserAllMock1, "TA, null, CS 351", "Professor can view themeselves assignments")

    def test_viewUserAssignmentAsProfessorAssignedTAs(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, self.userTA.id, self.userProf
        )
        self.assertEqual(viewUserAllMock1, "TA, null, CS 351", "Professor can view TA assignments to course")

    def test_viewUserAssignmentAsProfessorNotAssignedTAs(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, self.userTA2.id, self.userProf
        )
        self.assertEqual(viewUserAllMock1, "INVALID", "Professor cannot view not assigned course TA")

    def test_viewUserAssignmentUserIDNotExist(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, 33333, self.userProf
        )
        self.assertEqual(viewUserAllMock1, "INVALID", "Must be a valid existing userID")

    def test_viewUserAssignmentCourseIDNotExist(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            3333, self.userProf.id, self.userProf
        )
        self.assertEqual(viewUserAllMock1, "INVALID", "Must be a valid existing courseID")

    def test_viewUserAssignmentNullCourse(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            None, self.userProf.id, self.userProf
        )
        self.assertEqual(viewUserAllMock1, "INVALID", "Must be a non null courseID")

    def test_viewUserAssignmentNullUserID(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, None, self.userProf
        )
        self.assertEqual(viewUserAllMock1, "INVALID", "Must be a non null userID")

    def test_viewUserAssignmentNullUser(self):
        viewUserAllMock1 = self.mockHandleAssignments.viewUserAssignments(
            self.course.id, self.userProf.id, None
        )
        self.assertEqual(viewUserAllMock1, "INVALID", "Must be a non null call user")

