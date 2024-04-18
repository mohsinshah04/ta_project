import re
from ta_app.models import User, Role, Assign_User_Junction, Course, Semester
class MockHandleAssignments:

    @classmethod
    def createAssignment(self, courseCode, courseName, courseDescription, semester, user):
        # based on the internet, you got to use re for format checking
        if (semester == None):
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
        return True

    @classmethod
    def editAssignment(self, courseID, courseDescription, user):
        if (courseID == None):
            return False
        if (user == None):
            return False
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if (courseDescription == None):
            return False
        if len(courseDescription) < 10:
            return False
        if(Course.objects.filter(id=courseID).exists() == False):
            return False
        if user.User_Role.Role_Name != 'Admin':
            return False
        return True

    @classmethod
    def userAssignment(self, courseID, userID, user):
        if (courseID == None):
            return False
        if (userID == None):
            return False
        if (user == None):
            return False
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if (Course.objects.filter(id=courseID).exists() == False):
            return False
        if (User.objects.filter(id=userID).exists() == False):
            return False
        if ((User.objects.get(id=userID).User_Role.Role_Name != 'TA')
                and (User.objects.get(id=userID).User_Role.Role_Name != 'Professor')):
            return False
        if user.User_Role.Role_Name != 'Admin':
            return False
        return True

    @classmethod
    def deleteAssignment(self, courseID, user):
        if (courseID == None):
            return False
        if(user == None):
            return False
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if (Course.objects.filter(id=courseID).exists() == False):
            return False
        if user.User_Role.Role_Name != 'Admin':
            return False
        return True

    @classmethod
    def viewAllAssignments(self, user):
        if (user == None):
            return "INVALID"
        if(type(user) != User):
            return "INVALID"
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"

        return "Course: MATH - 201, Description: Calculus, Users: John Pork, Davis Clark\nCourse: CS - 351, Description: Data Strutures and Algos, Users: John Pork"

    @classmethod
    def viewUserAssignments(self, tuser, user):
        if (user == None):
            return "INVALID"
        if (tuser == None):
            return "INVALID"
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if (User.objects.filter(id=tuser.id).exists() == False):
            return "INVALID"

        if user.User_Role.Role_Name == 'Admin' or user.User_Role.Role_Name == 'Instructor':
            # Admin or Instructor can see all details
            return "MATH - 201 - Calculus Assigned Users: John Pork (TA), Davis Clark (TA) CS - 351 - Data Structures and Algos Assigned Users: John Pork (TA), Himmithy Him (Instructor)"
        elif user.User_Role.Role_Name == 'Instructor':
            if tuser.User_FName == 'John':
                return "MATH - 201 - Calculus Assigned Users: John Pork (TA), Davis Clark (TA) CS - 351 - Data Structures and Algos Assigned Users: John Pork (TA), Himmithy Him (Instructor)"
            elif user.User_FName == 'Davis':
                return "MATH - 201 - Calculus Assigned Users: John Pork (TA), Davis Clark (TA)"
        elif user.User_FName == 'John' or user.User_FName == 'Davis':
            # TA can only see their own or other TA's details, but not instructors' unless shared
            if tuser.User_FName == 'John':
                return "MATH - 201 - Calculus Assigned Users: John Pork (TA), Davis Clark (TA) CS - 351 - Data Structures and Algos Assigned Users: John Pork (TA), Himmithy Him (Instructor)"
            elif tuser.User_FName == 'Davis':
                return "MATH - 201 - Calculus Assigned Users: John Pork (TA), Davis Clark (TA) CS - 351 - Data Structures and Algos"
            else:
                return "INVALID"
        else:
            return "INVALID"

        return "No courses found for user"


