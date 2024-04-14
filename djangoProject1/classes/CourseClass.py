"""Currently Skeleton Class for Courses"""
from ta_app.models import Course, Section, Semester, Assign_User_Junction

class CourseClass:
    def __init__(self):
        pass

    def create_assignment(self, course_id, course_name, course_description):
        pass

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
