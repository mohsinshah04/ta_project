from django.test import TestCase
from classes.CourseClass import CourseClass
from classes.SectionClass import SectionClass
from .mocks import MockHandleAssignments
from ta_app.models import User, Role, Assign_User_Junction, Course, Semester, Section
from datetime import datetime
class SectionTestCase(TestCase):
    def setUp(self):
        self.semester = Semester.objects.create(Semester_Name="Fall 2024")
        self.RoleTA = Role.objects.create(Role_Name="TA")
        self.Role = Role.objects.create(Role_Name="Supervisor")
        self.RoleProf = Role.objects.create(Role_Name="Instructor")
        self.user = User.objects.create(User_FName="Supervisor", User_LName="User", User_Email="admin@uwm.edu",
                                        User_Password="admin", User_Role=self.Role)
        self.course = Course.objects.create(Course_Name="COMPSCI - 251 - Data Structures", Course_Description="Introduction to data structures.", Course_Semester_ID=self.semester)


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


        # Valid data for section creation
        self.sectionNumValid = '001'
        self.sectionTypeValid = 'Lecture'
        self.sectionMeetsDaysValid = ['M', 'W', 'F']
        self.sectionCampusValid = "Main Campus"
        self.sectionStartDate = '2023-09-01'
        self.sectionEndDate = '2023-12-15'
        self.sectionCreditsValid = 3
        self.sectionStartTimeValid = '09:00'
        self.sectionEndTimeValid = '10:15'
        self.sectionBuildingName = 'Tech Building'
        self.sectionRoomNumberValid = '101'
        self.sectionAssignedUsersValid = [self.user.id]

    def test_CreateSectionAssignmentValidSupervisor(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertTrue(createdSection, "Section should be create with valid data")

    def test_CreateSectionAssignmentInvalidCourse(self):
        """createdSection = MockHandleAssignments.createAssignment(
            1111, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            1111, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection[0], "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionNum(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, 222, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, 222, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionType(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, 222, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, 222, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")


    def test_CreateSectionAssignmentInvalidSectionMeetDays(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, 333,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, 333,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionCampus(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            3333,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            3333,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")
    def test_CreateSectionAssignmentInvalidSectionStartDate(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            '43', self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                '43', self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection[0], "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionEndDate(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, '33', self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, '33', self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection[0], "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionCredits(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, '4', self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, '4', self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionCreditsNegative(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, -4, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, -4, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionStartTime(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, 4,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, 4,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionEndTime(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            4, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        4, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionBuildingName(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, 334, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, 334, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionRoomNum(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, 443,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, 443,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")


    def test_CreateSectionAssignmentValidInstructor(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.userProf.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.userProf.id
        )
        self.assertTrue(createdSection, "Section should be create with valid data")

    def test_CreateSectionAssignmentValidTA(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid, self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.userTA2.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.userTA2.id
        )
        self.assertFalse(createdSection, "Section should be create with valid data")

    def test_CreateSectionAssignmentInvalidCourseNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            1111, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            None, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionNumNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, 222, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, None, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionTypeNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, 222, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, None, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")


    def test_CreateSectionAssignmentInvalidSectionMeetDaysNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, 333,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, None,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionCampusNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            3333,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            None,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid, self.sectionEndTimeValid, self.sectionBuildingName, self. sectionRoomNumberValid,
            self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")
    def test_CreateSectionAssignmentInvalidSectionStartDateNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            '43', self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                None, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionEndDateNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, '33', self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, None, self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionCreditsNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, '4', self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, None, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionCreditsNegativeNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, -4, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, None, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionStartTimeNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, 4,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, None,
        self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionEndTimeNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            4, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        None, self.sectionBuildingName, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionBuildingNameNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, 334, self.sectionRoomNumberValid,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, None, self.sectionRoomNumberValid,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")

    def test_CreateSectionAssignmentInvalidSectionRoomNumNone(self):
        """createdSection = MockHandleAssignments.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, 443,
            self.user.id
        )"""
        createdSection = SectionClass.createAssignment(
        self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
        self.sectionCampusValid,
                self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
        self.sectionEndTimeValid, self.sectionBuildingName, None,
        self.user.id
        )
        self.assertFalse(createdSection, "section should not be create with invalid data.")








    def test_viewUserAssignmentsValidSupervisor(self):
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.user.id
        )
        viewedSection = SectionClass.viewUserAssignments(
            self.user.id, self.course.id
        )
        sections = viewedSection.get('sections', [])
        s = sections[0].get('building')
        self.assertEqual(s, "Tech Building")

    def test_viewUserAssignmentsValidInstructor(self):
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.userProf.id
        )
        viewedSection = SectionClass.viewUserAssignments(
            self.userProf.id, self.course.id
        )
        sections = viewedSection.get('sections', [])
        s = sections[0].get('building')
        self.assertEqual(s, "Tech Building")

    def test_viewUserAssignmentsValidTA(self):
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.userProf.id
        )
        viewedSection = SectionClass.viewUserAssignments(
            self.userTA.id, self.course.id
        )
        self.assertTrue(viewedSection, "Tech Building")

    def test_viewUserAssignmentsInvalidUser(self):
        createdSection = SectionClass.createAssignment(
            self.course.id, self.sectionNumValid, self.sectionTypeValid, self.sectionMeetsDaysValid,
            self.sectionCampusValid,
            self.sectionStartDate, self.sectionEndDate, self.sectionCreditsValid, self.sectionStartTimeValid,
            self.sectionEndTimeValid, self.sectionBuildingName, self.sectionRoomNumberValid,
            self.userProf.id
        )
        viewedSection = SectionClass.viewUserAssignments(
            434, self.course.id
        )
        self.assertFalse(viewedSection, "Tech Building")
