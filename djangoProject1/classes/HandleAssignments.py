from abc import ABC, abstractmethod

class HandleAssignments(ABC):

    @abstractmethod
    def create_assignment(self, course, course_name, description):
        pass

    @abstractmethod
    def edit_assignment(self, course_ID, description):
        pass

    @abstractmethod
    def user_assignment(self, user_ID, course_ID):
        pass

    @abstractmethod
    def delete_assignment(self, course_ID):
        pass

    @abstractmethod
    def view_all_assignments(self, course_ID):
        pass

    @abstractmethod
    def view_user_assignments(self, course_ID, user_ID):
        pass