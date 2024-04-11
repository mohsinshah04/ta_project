"""
This class is an abstract class that is used to create all of the variations of a user that can be found on the app
"""
from djangoProject1.ta_app.models import User, Role
class UserAbstractClass:

    def __init__(self, role):
        self.role = role

    def create_user(self, email, password, role, phoneNumber, address, firstName, lastName, Role):
        if self.role != "Supervisor":
            return False
        if email is None or password is None or role is None or phoneNumber is None or address is None or firstName is None or lastName is None or email is None:
            return False
        if len(password) < 7 or len(phoneNumber) < 15:
            return False
        ID = 1234
        User.objects.create(email=email, password=password, role=Role, phoneNumber=phoneNumber, address=address,
                            firstName=firstName, lastName=lastName, User_ID=ID)
        toReturn = User.object.filter(email=email).exists()
        return toReturn



    def delete_user(self, user_ID):
        pass


    def edit_user(self, user_ID, email, password, role, phoneNumber, address, firstName, lastName):
        pass


    def account_role(self, user_ID):
        pass


    def view_account(self, user_ID):
        pass