from djangoProject1.ta_app.models import Role, User


class RoleClass:
    def __init__(self):
        pass

    @classmethod
    def create_role(self, roleName, user):
        if (roleName == None):
            return False
        if (Role.objects.filter(name=roleName).exists() != False):
            return False
        if (user.User_Role.Role_Name != 'Supervisor'):
            return False

        role = Role.objects.create(name=roleName)

        if(role == None):
            return False

        return True

    @classmethod
    def delete_role(self, roleName, user):
        if(roleName == None):
            return False
        if(Role.objects.filter(name=roleName).exists() == False):
            return False
        if(user.User_Role.Role_Name != 'Supervisor'):
            return False

        Role.objects.filter(id=roleName).delete()

        return True