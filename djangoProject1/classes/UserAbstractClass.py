"""
This class is an abstract class that is used to create all of the variations of a user that can be found on the app
"""
from djangoProject1.ta_app.models import User, Role
class UserAbstractClass:

    def __init__(self, role):
        self.role = role

    def create_user(self, email, password, role, phoneNumber, address, firstName, lastName):
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
        if self.role != "Supervisor":
            return False
        if user_ID is None:
            return False
        if User.objects.filter(User_ID=user_ID) is None:
            return False
        User.objects.delete(user_ID)
        toReturn = not(User.objects.filter(User_ID=user_ID).exists())
        return toReturn


    def edit_user(self, user_ID, email, password, phoneNumber, address, firstName, lastName):
        if self.role != "Supervisor":
            return False
        if user_ID is None or email is None or password is None or phoneNumber is None or address is None or firstName is None or lastName is None:
            return False
        if len(password) < 7 or len(phoneNumber) < 15:
            return False
        User.objects.filter(User_ID=user_ID, email=email, password=password, phoneNumber=phoneNumber, address=address,
                            firstName=firstName, lastName=lastName).update()
        toReturn = User.object.filter(User_ID=user_ID).exists()
        return toReturn

    def account_role(self, user_ID):
        if not (User.objects.filter(User_ID=user_ID).exists()):
            return False
        if self.role != "TA":
            return False

        toReturn = User.object.filter(User_ID=user_ID).exists()
        return toReturn

    def view_account(self, user_ID):
        if not (User.objects.filter(User_ID=user_ID).exists()):
            return "INVALID"
        user = User.objects.filter(User_ID=user_ID)
        if self.role == "Supervisor":
            return user.User_FName + ", " + user.User_LName + ": " + user.User_Role
        if (self.role == "Instructor" and user.User_Role == "Supervisor") or (self.role == "TA" and user.User_Role == "Instrctor"):
            return "INVALID"

        return user.User_FName + ", " + user.User_LName + ": " + user.User_Role