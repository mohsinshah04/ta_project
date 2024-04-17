import re
from ta_app.models import User, Role, Assign_User_Junction, Course, Semester
class MockHandleAssignments:
    def createAssignment(self, courseCode, courseName, courseDescription, user):
        #based on the internet, you got to use re for format checking
        if (courseCode == None):
            return False
        if (courseName == None):
            return False
        if (user == None):
            return False
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if (courseDescription == None):
            return False
        if not re.match(r"^[A-Z]+ - \d+$", courseCode):
            return False
        if not courseName or not courseDescription or len(courseDescription) < 10:
            return False
        if user.User_Role.Role_Name != 'Admin':
            return False
        return True

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

    def viewAllAssignments(self, courseID, userID, user):
        if (courseID == None):
            return "INVALID"
        if (userID == None):
            return "INVALID"
        if (user == None):
            return "INVALID"
        if (Course.objects.filter(id=courseID).exists() == False):
            return "INVALID"
        if (User.objects.filter(id=userID).exists() == False):
            return "INVALID"
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if Assign_User_Junction.objects.filter(Course_ID=courseID, User_ID=userID).exists() == False:
            return "INVALID"
        if user.User_Role.Role_Name != 'Admin':
            return "INVALID"
        cDes = Course.objects.get(id=courseID).Course_Description
        cName = Course.objects.get(id=courseID).Course_Name

        return cName + " - " + cDes

    def viewUserAssignments(self, courseID, userID, user):
        if (user == None):
            return "INVALID"
        if (courseID == None):
            return "INVALID"
        if (userID == None):
            return "INVALID"
        if (Course.objects.filter(id=courseID).exists() == False):
            return "INVALID"
        if (User.objects.filter(id=userID).exists() == False):
            return "INVALID"
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if Assign_User_Junction.objects.filter(Course_ID=courseID, User_ID=userID).exists() == False:
            return "INVALID"
        if user.User_Role.Role_Name != 'Admin':
            if user.User_Role.Role_Name == 'Professor':
                if(Assign_User_Junction.objects.filter(Course_ID=courseID, User_ID=user.id).exists() == False):
                    return "INVALID1"
            elif(userID != user.id):
                return "INVALID"
        cDes = Course.objects.get(id=courseID).Course_Description
        cName = Course.objects.get(id=courseID).Course_Name
        FName = User.objects.get(id=userID).User_FName
        LName = User.objects.get(id=userID).User_LName

        return FName + ", " + LName + ", " + cName



