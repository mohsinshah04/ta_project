import re
class MockHandleAssignments:
    def create_assignment(self, courseCode, courseName, courseDescription, user):
        #based on the internet, you got to use re for format checking
        if not re.match(r"^[A-Z]+ - \d+$", courseCode):
            return False
        if not courseName or not courseDescription or len(courseDescription) < 10:
            return False
        if user.User_Role.Role_Name != 'Admin':
            return False
        return True