"""
This class is an abstract class that is used to create all of the variations of a user that can be found on the app
"""
from djangoProject1.ta_app.models import User, Role

class UserAbstractClass:

    def __init__(self, role):
        if role.Role_Name == "Supervisor":
            self.role = role
        else:
            raise TypeError("The role given was not a supervisor")

    def create_user(self, email, password, role, phoneNumber, address, firstName, lastName):
        pass


    def delete_user(self, user_ID):
        pass


    def edit_user(self, user_ID, email, password, role, phoneNumber, address, firstName, lastName):
        pass


    def account_role(self, user_ID):
        pass


    def view_account(self, user_ID):
        pass

