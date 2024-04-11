from models import User, Role

class UserAbstractClass:

    @classmethod
    def create_user(self, email, password, role, phoneNumber, address, firstName, lastName):
        pass

    @classmethod
    def delete_user(self, user_ID):
        pass

    @classmethod
    def edit_account(self, user_ID, email, password, role, phoneNumber, address, firstName, lastName):
        pass

    @classmethod
    def account_role(self, user_ID):
        pass

    @classmethod
    def view_account(self, user_ID):
        pass

