from abc import ABC, abstractmethod

class HandleAssignments(ABC):

    @abstractmethod
    def createAssignment(self, course, course_name, description):
        pass

    @abstractmethod
    def editAssignment(self, course_ID, description):
        pass

    @abstractmethod
    def userAssignment(self, user_ID, course_ID):
        pass

    @abstractmethod
    def deleteAssignment(self, course_ID):
        pass

    @abstractmethod
    def viewAllAssignments(self, course_ID):
        pass

    @abstractmethod
    def viewUserAssignments(self, course_ID, user_ID):
        pass