from models import User, Role

class UserAbstractClass():

    def create_user(self, email, password, role, phoneNumber, address, firstName, lastName):
        pass

    def delete_user(self, user_ID):
        pass

    def edit_account(self, user_ID, email, password, role, phoneNumber, address, firstName, lastName):
        pass

    def account_role(self, user_ID):
        pass

    def view_account(self, user_ID):
        pass

