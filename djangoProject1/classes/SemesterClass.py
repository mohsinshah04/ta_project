"""Currently Skeleton Class for Semesters"""
from ta_app.models import Course, Section, Semester, Assign_User_Junction, User
from datetime import datetime
class SemesterClass:
    def __init__(self, semester):
        pass


    @classmethod
    def createSemester(self, semesterTerm, semesterYear, user):
        if user == None:
            return False
        if semesterTerm == None:
            return False
        if(semesterYear == None):
            return False
        if(type(semesterYear) != int):
            return False
        if (type(user) != User):
            return False
        if not User.objects.filter(id=user.id).exists():
            return False
        if user.User_Role.Role_Name != 'Supervisor':
            return False

        validSemesterTerms = ["Spring", "Fall", "Winter", "Summer"]

        validCheck = False
        for term in validSemesterTerms:
            if term in semesterTerm:
                validCheck = True

        if(validCheck == False):
            return False

        curYear = datetime.now().year
        if ((semesterYear>curYear)):
            return False


        buildName = semesterTerm + " " + str(semesterYear)
        self.semester = Semester.objects.create(Semester_Name=buildName)
        if(self.semester == None):
            return False

        return True


    @classmethod
    def deleteSemester(self, semester, user):
        if user == None:
            return False
        if semester == None:
            return False
        if (type(user) != User):
            return False
        if not User.objects.filter(id=user.id).exists():
            return False
        if not Semester.objects.filter(id=semester).exists():
            return False
        if user.User_Role.Role_Name != 'Supervisor':
            return False

        Semester.objects.filter(id=semester).delete()

        return True
