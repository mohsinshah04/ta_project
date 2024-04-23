from ta_app.models import Role, User


class RoleClass:
    def __init__(self):
        pass

    @classmethod
    def create_role(self, roleName, user):
        if roleName is None:
            return False
        if type(user) != User:
            return False
        if Role.objects.filter(name=roleName).exists():
            return False
        if user.User_Role.Role_Name != 'Supervisor':
            return False

        validRole = ["TA", "Supervisor", "Instructor"]

        validCheck = False
        for term in validRole:
            if term in roleName:
                validCheck = True

        if not validCheck:
            return False

        role = Role.objects.create(name=roleName)

        if role is None:
            return False

        return True

    @classmethod
    def delete_role(self, roleName, user):
        if roleName is None:
            return False
        if type(user) != User:
            return False
        if not Role.objects.filter(name=roleName).exists():
            return False
        if not User.objects.filter(id=user.id).exists():
            return False
        if user.User_Role.Role_Name != 'Supervisor':
            return False

        Role.objects.filter(id=roleName).delete()

        return True
