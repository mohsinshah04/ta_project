"""Currently Skeleton Class for Courses"""
from ta_app.models import Course, Section, Semester, Assign_User_Junction, User
import re
class CourseClass:
    def __init__(self):
        pass

    @classmethod
    def createAssignment(self, courseCode, courseName, courseDescription, semester, user):
        # based on the internet, you got to use re for format checking
        if(semester == None):
            return False
        if (courseCode == None):
            return False
        if (courseName == None):
            return False
        if (user == None):
            return False
        if (User.objects.filter(id=user.id).exists() == False):
            return False
        if (Semester.objects.filter(id=semester).exists() == False):
            return False
        if (courseDescription == None):
            return False
        if not re.match(r"^[A-Z]+ - \d+$", courseCode):
            return False
        if not courseName or not courseDescription or len(courseDescription) < 10:
            return False
        if user.User_Role.Role_Name != 'Admin':
            return False
        course = Course.objects.create(Course_Name="CS 351", Course_Description="Course Test.",Course_Semester_ID_id=semester)

        if(course == None):
            return False

        return True


    def edit_assignment(self, course_id, course_description):
        pass

    def user_assignment(self, course_id, user_id):
        pass

    def delete_course(self, course_id):
        pass

    def view_all_assignments(self, course_id):
        pass

    def view_user_assignments(self, course_id, user_id):
        pass
