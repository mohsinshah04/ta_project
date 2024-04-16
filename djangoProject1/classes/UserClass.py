"""
This class is an abstract class that is used to create all of the variations of a user that can be found on the app
"""
from ta_app.models import User, Role, Assign_User_Junction


class UserObject:

    def __init__(self, role):
        if not isinstance(role, Role):
            raise TypeError("Please specify a valid role")
        self.role = role

    def create_user(self, email, password, role, phoneNumber, address, firstName, lastName):
        if self.role.Role_Name != "Supervisor":
            return False
        if email is None or password is None or role is None or phoneNumber is None or address is None or firstName is None or lastName is None or email is None:
            return False
        if len(password) < 7 or len(phoneNumber) < 15:
            return False
        if User.objects.filter(User_Email=email).exists():
            return False
        role.save()
        User.objects.create(User_Email=email, User_Password=password, User_Role=role, User_Phone_Number=phoneNumber, User_Home_Address=address,
                            User_FName=firstName, User_LName=lastName).save()
        toReturn = User.objects.filter(User_Email=email).exists()
        return toReturn


    def delete_user(self, user_id):
        if self.role.Role_Name != "Supervisor":
            return False
        if user_id is None:
            return False
        if not User.objects.filter(id=user_id).exists():
            return False
        User.objects.filter(id=user_id).delete()
        toReturn = not User.objects.filter(id=user_id).exists()
        return toReturn


    def edit_user(self, user_ID, email, password, phoneNumber, address, firstName, lastName):
        if self.role.Role_Name != "Supervisor":
            return False
        if (user_ID is None or email is None or password is None or phoneNumber is None or address is None or firstName
            is None or lastName is None):
            return False
        if len(password) < 7 or len(phoneNumber) < 15:
            return False
        if not User.objects.filter(id=user_ID).exists():
            return False
        user = User.objects.get(id=user_ID)
        user.User_Email = email
        user.User_Password = password
        user.User_Phone_Number = phoneNumber
        user.User_Home_Address = address
        user.User_FName = firstName
        user.User_LName = lastName
        user.save()
        toReturn = User.objects.filter(User_Email=email).exists()
        return toReturn

    def account_role(self, user_ID, changed_role):
        if not User.objects.filter(id=user_ID).exists():
            return False
        if self.role.Role_Name != "TA":
            return False
        toReturn = User.objects.filter(id=user_ID).exists()
        return toReturn

    #Waiting for course class to be complete and tested, then will add list of sections later
    def view_account(self, user_ID):
        if not User.objects.filter(id=user_ID).exists():
            return "INVALID"
        user = User.objects.get(id=user_ID)
        if self.role.Role_Name == "Supervisor":
            return user.User_FName + ", " + user.User_LName + ": " + user.User_Role.Role_Name
        if self.role.Role_Name == "Instructor" and user.User_Role.Role_Name == "Supervisor":
            return "INVALID"
        if self.role.Role_Name == "TA" and (user.User_Role.Role_Name == "Instructor" or user.User_Role.Role_Name =="Supervisor"):
            return "INVALID"
        #sectionsList = list(Assign_User_Junction.objects.filter(User_ID=user_ID))
        return user.User_FName + ", " + user.User_LName + ": " + user.User_Role.Role_Name