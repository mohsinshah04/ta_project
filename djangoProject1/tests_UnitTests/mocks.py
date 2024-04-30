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
    def createAssignment(self, classID, sectionNum, sectionType, sectionMeetsDays, sectionCampus, sectionStartDate, sectionEndDate, sectionCredits, sectionStartTimes, sectionEndTimes, buldingName, roomNum, userID):
        if (userID == None):
            return False
        user = User.objects.get(id=userID)
        if (user.User_Role.Role_Name == "TA"):
            return False

        if (classID == None) or (sectionNum == None) or (sectionType == None) or (sectionMeetsDays == None) or (sectionCampus == None) or (sectionStartDate == None) or (sectionEndDate == None) or (sectionCredits == None) or (sectionStartTimes == None) or (sectionEndTimes == None) or (userID == None):
            return False

        if(type(sectionNum) ==int):
            return False
        if (type(sectionType) == int):
            return False
        if(type(sectionMeetsDays) != list ):
            return False

        if(type(sectionCampus) == int):
            return False
        if(type(sectionCredits) != int):
            return False
        if (sectionCredits <0):
            return False
        if(type(sectionStartTimes) ==int):
            return False
        if (type(sectionEndTimes) == int):
            return False
        if (type(buldingName) == int):
            return False
        if (type(roomNum) == int):
            return False
        try:
            return True
        except Exception as e:
            return False, str(e)

    @classmethod
    def createAssignment(self, classID, sectionNum, sectionType, sectionMeetsDays, sectionCampus, sectionStartDate, sectionEndDate, sectionCredits, sectionStartTimes, sectionEndTimes, userID):
        # based on the internet, you got to use re for format checking
        if(classID == None):
            return False
        if (User.objects.filter(id=userID).exists() == False):
            return "INVALID"


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


class MockUser:

    @classmethod
    def create_user(cls, email, password, role, phoneNumber, address, firstName, lastName, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor":
            return False
        if email is None or password is None or role is None or phoneNumber is None or address is None or firstName is None or lastName is None or email is None:
            return False
        if email == "" or password == "" or role == "" or phoneNumber == "" or address == "" or firstName == "" or lastName == "" or email == "":
            return False
        if role.Role_Name != "Supervisor" and role.Role_Name != "Instructor" and role.Role_Name != "TA":
            return False
        if len(password) < 7 or len(phoneNumber) > 15:
            return False
        if User.objects.filter(User_Email=email).exists():
            return False
        return True

    @classmethod
    def delete_user(cls, user_id, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor":
            return False
        if user_id is None:
            return False
        if not User.objects.filter(id=user_id).exists():
            return False
        return True

    @classmethod
    def edit_user(cls, user_id, email, password, phoneNumber, address, firstName, lastName, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor" and user_id != own_id:
            return False
        if user_id is None or email is None or password is None or phoneNumber is None or address is None or firstName is None or lastName is None:
            return False
        if email == "" or password == "" or phoneNumber == "" or address == "" or firstName == "" or lastName == "":
            return False
        if len(password) < 7 or len(phoneNumber) > 15:
            return False
        if not User.objects.filter(id=user_id).exists():
            return False
        return True

    @classmethod
    def account_role(cls, user_ID, change_role, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor":
            return False
        if not User.objects.filter(id=user_ID).exists():
            return False
        if change_role == None:
            return False
        change_role.save()
        user.User_Role = change_role
        toReturn = User.objects.filter(User_Role=change_role).exists()
        return toReturn

    @classmethod
    def view_account(cls, user_ID, own_id):
        if not User.objects.filter(id=own_id).exists():
            return "INVALID"
        checked_user = User.objects.get(id=own_id)
        if not User.objects.filter(id=user_ID).exists():
            return "INVALID"
        user = User.objects.get(id=user_ID)
        if checked_user.User_Role.Role_Name == "Instructor" and user.User_Role.Role_Name == "Supervisor":
            return "INVALID"
        if checked_user.User_Role.Role_Name == "TA" and (user.User_Role.Role_Name == "Instructor" or user.User_Role.Role_Name == "Supervisor"):
            return "INVALID"

        if checked_user.User_Role.Role_Name == "Supervisor" and user.User_Role.Role_Name == "Instructor":
            return "Jose Johnson: Instrc@uwm.edu: 1+(608)532-2343: 123, Ridgeview Ct: Instructor"

        if checked_user.User_Role.Role_Name == "Supervisor" and user.User_Role.Role_Name == "TA":
            return "Joann Johnson: TA@uwm.edu 1+(608)522-2343: 123, Ridgeview Ct: TA"

        if checked_user.User_Role.Role_Name == "Supervisor" and user.User_Role.Role_Name == "Supervisor":
            return "John Johnson: Super@uwm.edu: 1+(608)542-2343: 123, Ridgeview Ct: Supervisor"

        if checked_user.User_Role.Role_Name == "Instructor" and user.User_Role.Role_Name == "TA":
            return "Joann Johnson: TA@uwm.edu 1+(608)522-2343: 123, Ridgeview Ct: TA"

        if checked_user.User_Role.Role_Name == "Instructor" and checked_user.User_Role.Role_Name == "Instructor":
            return "Jose Johnson: Instrc@uwm.edu: 1+(608)532-2343: 123, Ridgeview Ct: Instructor"

        if checked_user.User_Role.Role_Name == "TA" and user.User_Role.Role_Name == "TA":
            return "Joann Johnson: TA@uwm.edu 1+(608)522-2343: 123, Ridgeview Ct: TA"



