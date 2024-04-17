"""
This class is an abstract class that is used to create all of the variations of a user that can be found on the app
"""
from ta_app.models import User, Role, Assign_User_Junction


class UserObject:

    """
        def __init__(self, role):
        if not isinstance(role, Role):
            raise TypeError("Please specify a valid role")
        self.role = role
    """
    @classmethod
    def create_user(cls, email, password, role, phoneNumber, address, firstName, lastName, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor":
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


    @classmethod
    def delete_user(cls, user_id, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor":
            return False
        if user_id is None:
            return False
        if not User.objects.filter(id=user_id).exists():
            return False
        User.objects.filter(id=user_id).delete()
        toReturn = not User.objects.filter(id=user_id).exists()
        return toReturn


    @classmethod
    def edit_user(cls, user_id, email, password, phoneNumber, address, firstName, lastName, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor" and user_id != own_id:
            return False
        if (user_id is None or email is None or password is None or phoneNumber is None or address is None or firstName
            is None or lastName is None):
            return False
        if len(password) < 7 or len(phoneNumber) < 15:
            return False
        if not User.objects.filter(id=user_id).exists():
            return False
        user = User.objects.get(id=user_id)
        user.User_Email = email
        user.User_Password = password
        user.User_Phone_Number = phoneNumber
        user.User_Home_Address = address
        user.User_FName = firstName
        user.User_LName = lastName
        user.save()
        toReturn = User.objects.filter(User_Email=email).exists()
        return toReturn


    @classmethod
    def account_role(cls, user_ID, change_role, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        user = User.objects.get(id=own_id)
        if user.User_Role.Role_Name != "Supervisor":
            return False
        if not User.objects.filter(id=user_ID).exists():
            return False
        if change_role == None:
            return False
        change_role.save()
        user.User_Role = change_role
        toReturn = User.objects.filter(User_Role=change_role).exists()
        return toReturn

    #Waiting for course class to be complete and tested, then will add list of sections later
    @classmethod
    def view_account(cls, user_ID, own_id):
        if not User.objects.filter(id=own_id).exists():
            return False
        checked_user = User.objects.get(id=own_id)
        if not User.objects.filter(id=user_ID).exists():
            return "INVALID"
        user = User.objects.get(id=user_ID)
        if checked_user.User_Role.Role_Name == "Supervisor":
            return user.User_FName + ", " + user.User_LName + ": " + user.User_Role.Role_Name
        if checked_user.User_Role.Role_Name == "Instructor" and user.User_Role.Role_Name == "Supervisor":
            return "INVALID"
        if checked_user.User_Role.Role_Name == "TA" and (user.User_Role.Role_Name == "Instructor" or user.User_Role.Role_Name =="Supervisor"):
            return "INVALID"
        #sectionsList = list(Assign_User_Junction.objects.filter(User_ID=user_ID))
        return user.User_FName + ", " + user.User_LName + ": " + user.User_Role.Role_Name