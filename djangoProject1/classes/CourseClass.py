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
        if user.User_Role.Role_Name != 'Supervisor':
            return False

        buildString = courseCode + " - " + courseName
        course = Course.objects.create(Course_Name=buildString, Course_Description=courseDescription,Course_Semester_ID_id=semester)

        if(course == None):
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
        if (Course.objects.filter(id=courseID).exists() == False):
            return False
        if user.User_Role.Role_Name != 'Supervisor':
            return False
        course = Course.objects.get(id=courseID)
        course.Course_Description = courseDescription

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
                and (User.objects.get(id=userID).User_Role.Role_Name != 'Instructor')):
            return False
        if user.User_Role.Role_Name != 'Supervisor':
            return False

        if(Assign_User_Junction.objects.filter(Course_ID=Course.objects.get(id=courseID), User_ID=User.objects.get(id=userID)).exists()):
            return True

        assigned = Assign_User_Junction.objects.create(Course_ID=Course.objects.get(id=courseID), User_ID=User.objects.get(id=userID))

        if(assigned == None):
            return False

        return True

    @classmethod
    def deleteAssignment(self, courseID, user):
        if (courseID == None):
            return False
        if (user == None):
            return False
        userobj = User.objects.get(id=user)
        if (User.objects.filter(id=user).exists() == False):
            return "INVALID"
        if (Course.objects.filter(id=courseID).exists() == False):
            return False
        if userobj.User_Role.Role_Name != 'Supervisor':
            Assign_User_Junction.objects.filter(Course_ID=courseID, User_ID_id=user).delete()
        else:
            Course.objects.filter(id=courseID).delete()

        return True

    @classmethod
    def viewAllAssignments(self, user):
        if (user == None):
            return "INVALID"
        if(type(user) != User):
            return "INVALID"
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"

        courses = Course.objects.all()
        results = ""

        for course in courses:
            courseDetails = course.Course_Name + " - " + course.Course_Description + "\nAssigned Users: "
            junctions = Assign_User_Junction.objects.filter(Course_ID=course).select_related('User_ID', 'User_ID__User_Role')
            userDetails = ""
            first_user = True
            checkExists = []

            for junction in junctions:
                i = 0
                if user.User_Role.Role_Name == 'TA' and junction.User_ID.User_Role.Role_Name == 'Instructor':
                    if not Assign_User_Junction.objects.filter(Course_ID=course, User_ID=user).exists():
                        continue

                if junction.User_ID.id in checkExists:
                    continue
                checkExists.insert(i, junction.User_ID.id)
                i = i+1

                indDetail = junction.User_ID.User_FName + " " + junction.User_ID.User_LName + " (" + junction.User_ID.User_Role.Role_Name + ")"
                if not first_user:
                    userDetails += ", "


                userDetails += indDetail
                first_user = False

            if userDetails:
                courseDetails += userDetails
            else:
                courseDetails += "No assigned users"
            if results:
                results += "\n\n"
            results += courseDetails
        return results if results else "No courses found"

    @classmethod
    def viewUserAssignments(self, tuser, user):
        if tuser == None:
            return "INVALID"
        if user == None:
            return "INVALID"
        if (type(user) != User):
            return "INVALID"
        if (type(tuser) != User):
            return "INVALID"
        if not User.objects.filter(id=user.id).exists() or not User.objects.filter(id=tuser.id).exists():
            return "INVALID"

        # this check btw is for if a ta is calling a professor that they are never assigned to
        if ((user.User_Role.Role_Name != 'Supervisor') and (user.User_Role.Role_Name != 'Instructor')) and (user.User_Role.Role_Name == 'TA' and tuser.User_Role.Role_Name == 'Instructor'):
            #if you do __ you can move through tables attributes, cool!
            if not Assign_User_Junction.objects.filter(User_ID=tuser, Course_ID__assign_user_junction__User_ID=user).exists():
                return "INVALID"

        courses = Course.objects.filter(assign_user_junction__User_ID=tuser)
        results = ""
        checkCourses = []
        z = 0
        for course in courses:
            if results:
                results += "\n\n"
            if(course.id in checkCourses):
                continue
            checkCourses.insert(z, course.id)
            z = z + 1

            courseDetails = course.Course_Name + " - " + course.Course_Description + "\nAssigned Users: "


            userDetails = ""
            junctions = Assign_User_Junction.objects.filter(Course_ID=course).select_related('User_ID', 'User_ID__User_Role')
            first_user = True
            checkExists = []
            for junction in junctions:
                i = 0
                if junction.User_ID.id in checkExists:
                    continue
                checkExists.insert(i, junction.User_ID.id)
                i = i+1
                userDetail = junction.User_ID.User_FName + " " + junction.User_ID.User_LName + " (" + junction.User_ID.User_Role.Role_Name + ")"
                if not first_user:
                    userDetails += ", "
                userDetails += userDetail
                first_user = False

            courseDetails += userDetails if userDetails else "No assigned users"
            results += courseDetails

        return results if results else "No courses found for user"

