"""Currently Skeleton Class for Semesters"""
from ta_app.models import Semester


class SemesterClass:
    def __init__(self, semester):
        self.semester = semester

    @classmethod
    def createSemester(self, semesterTerm, semesterYear, user):
        pass

    def deleteSemester(self, semester, user):
        pass
