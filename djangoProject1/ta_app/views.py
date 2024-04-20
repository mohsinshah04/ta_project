from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from datetime import datetime
from .models import Role, User
from classes.UserClass import UserObject
# Create your views here.


class LoginPage(View):
    def get(self,request):
        return render(request,"loginPage.html",{})
    def post(self, request):
        #if request.session.get('id') is not None:
            #return render(request,"loginPage.html",{"message": "User already logged in"})
        user_doesnt_exist = False
        bad_password = False
        try:
            m = User.objects.get(User_Email=request.POST['Email'])
            bad_password = (m.User_Password != request.POST['Password'])
        except:
            user_doesnt_exist = True
        if user_doesnt_exist:
            return render(request, "loginPage.html", {"message": "Email and password do not exists. Please contact your supervisor to get your account created"})
        elif bad_password:
            return render(request, "loginPage.html", {"message": "Incorrect Password, please try again."})
        else:
            request.session["id"] = m.id
            return redirect("/home/")


class LogOutPage(View):
    def get(self, request):
        request.session.clear()
        return render(request, 'logOutPage.html', {})

    def post(self, request):
        request.session.clear()
        return render(request, 'logOutPage.html', {})


class Home(View):
    def get(self, request):
        return render(request, 'home.html', {})

    def post(self, request):
        return render(request, 'home.html', {})


class Announcements(View):
    def get(self, request):
        return render(request, 'announcements.html', {})

    def post(self, request):
        return render(request, 'announcements.html', {})


class AccountViewSelf(View):
    def get(self, request):
        own_id = request.session.get('id')
        user = User.objects.get(id=own_id)
        name = user.User_FName + " " + user.User_LName
        email = user.User_Email
        phone = user.User_Phone_Number
        address = user.User_Home_Address
        return render(request, 'acctsViewSelf.html', {"name": name, "email": email, "phone":phone, "address": address})

    def post(self, request):
        return render(request, 'acctsViewSelf.html', {})


class AccountSearch(View):
    def get(self, request):
        return render(request, 'acctsSearch.html', {})
    def post(self, request):
        own_id = request.session.get("id")
        user_fname = request.POST.get('First Name')
        user_lname = request.POST.get('Last Name')
        if not User.objects.filter(User_FName=user_fname, User_LName=user_lname).exists():
            return render(request, 'acctsSearch.html', {"message": "Invalid account: " + user_fname + " " + user_lname})
        own_user = User.objects.get(id=own_id)
        user = User.objects.get(User_FName=user_fname, User_LName=user_lname)
        if own_user.User_Role.Role_Name == 'Instructor' and user.User_Role.Role_Name == 'Supervisor':
            return render(request, 'acctsSearch.html', {"message": "You cannot view this account because of your role"})

        if own_user.User_Role.Role_Name == 'TA' and (
                user.User_Role.Role_Name == 'Supervisor' or user.User_Role.Role_Name == 'Instructor'):
            return render(request, 'acctsSearch.html', {"message": "You cannot view this account because of your role"})

        account_string = UserObject.view_account(user.id, own_id)
        if account_string == "INVALID":
            return render(request, "acctsSearch.html", {"message": "Invalid account id: " + user.id})
        name = account_string.split(":")
        return render(request, 'acctsSearch.html', {"name": name[0], "role": name[1]})

class AccountCreate(View):
    def get(self, request):
        return render(request, 'acctsCreate.html', {})

    def post(self, request):
        get_all_info = False
        try:
            own_id = request.session.get("id")
            own_user = User.objects.get(id=own_id)
            if own_user.User_Role.Role_Name != "Supervisor":
                return render(request, "acctsCreate.html", {"message": "You do not have permission to create users"})

            f_name = request.POST.get('First Name')
            l_name = request.POST.get('Last Name')
            email = request.POST.get('Email')
            password = request.POST.get('Password')
            role_name = request.POST.get('Role')
            if role_name != "Supervisor" and role_name != "Instructor" and role_name != "TA":
                return render(request, "acctsCreate.html", {"message": "Please enter a valid role"})
            role = Role(Role_Name=role_name)
            address = request.POST.get('Address')
            phone = request.POST.get('Phone Number')
        except:
            get_all_info = True

        if get_all_info:
            return render(request, "acctsCreate.html", {"message": "Please enter in all information"})

        toReturn = UserObject.create_user(email, password, role, phone, address, f_name, l_name, own_id)
        if not toReturn:
            return render(request, "acctsCreate.html", {"message": "User was not created successfully"})

        return render(request, 'acctsCreate.html', {"message": "User was created successfully"})


class AccountEditSelf(View):
    def get(self, request):
        return render(request, 'acctsEditSelf.html', {})

    def post(self, request):
        get_all_info = False
        try:
            own_id = request.session.get('id')
            user_password = request.POST.get('Old Password')
            own_user = User.objects.get(id=own_id)
            if own_user.User_Password != user_password:
                return render(request, 'acctsEditSelf.html', {"message": "Account passwords do not match"})
            user_id = User.objects.get(User_Password=user_password).id
            f_name = request.POST.get('First Name')
            l_name = request.POST.get('Last Name')
            email = request.POST.get('Email')
            password = request.POST.get('Password')
            address = request.POST.get('Address')
            phone = request.POST.get('Phone Number')
            if f_name == "":
                f_name = own_user.User_FName
            if l_name == "":
                l_name = own_user.User_LName
            if email == "":
                email = own_user.User_Email
            if password == "":
                password = own_user.User_Password
            if address == "":
                address = own_user.User_Home_Address
            if phone == "":
                phone = own_user.User_Phone_Number

        except:
            get_all_info = True

        if get_all_info:
            return render(request, 'acctsEditSelf.html', {"message": "Please enter all information correctly"})

        toReturn = UserObject.edit_user(user_id, email, password, phone, address, f_name, l_name, own_id)

        if not toReturn:
            return render(request, 'acctsEditSelf.html', {"message": "Account was not updated successfully"})

        return render(request, 'acctsEditSelf.html', {"message": "Account was updated successfully"})


class AccountEditOther(View):
    def get(self, request):
        return render(request, 'acctsOtherEdit.html', {})

    def post(self, request):
        get_all_info = False
        try:
            own_id = request.session.get('id')
            user_email = request.POST['User Email']
            if not User.objects.filter(User_Email=user_email).exists():
                return render(request, 'acctsOtherEdit.html', {"message": "Invalid account email: " + user_email})
            own_user = User.objects.get(id=own_id)
            user = User.objects.get(User_Email=user_email)
            user_id = user.id
            if own_user.User_Role.Role_Name != "Supervisor":
                return render(request, "acctsOtherEdit.html", {"message": "You do not have permission to create users"})
            f_name = request.POST.get('First Name')
            l_name = request.POST.get('Last Name')
            email = request.POST.get('Email')
            password = request.POST.get('Password')
            address = request.POST.get('Address')
            phone = request.POST.get('Phone Number')
            if f_name == "":
                f_name = user.User_FName
            if l_name == "":
                l_name = user.User_LName
            if email == "":
                email = user.User_Email
            if password == "":
                password = user.User_Password
            if address == "":
                address = user.User_Home_Address
            if phone == "":
                phone = user.User_Phone_Number
        except:
            get_all_info = True

        if get_all_info:
            return render(request, 'acctsOtherEdit.html', {"message": "Please enter all information correctly"})

        toReturn = UserObject.edit_user(user_id, email, password, phone, address, f_name, l_name, own_id)

        if not toReturn:
            return render(request, 'acctsOtherEdit.html', {"message": "Account was not updated successfully"})

        return render(request, 'acctsOtherEdit.html', {"message": "Account was updated successfully"})

class AccountDelete(View):
    def get(self, request):
        return render(request, 'deleteAccounts.html', {})

    def post(self, request):
        own_id = request.session.get('id')
        user_email = request.POST.get('User Email')
        if not User.objects.filter(User_Email=user_email).exists():
            return render(request, 'deleteAccounts.html', {"message": "Invalid account id: " + user_email})
        own_user = User.objects.get(id=own_id)
        user_id = User.objects.get(User_Email=user_email).id
        if own_user.User_Role.Role_Name != "Supervisor":
            return render(request, 'deleteAccounts.html', {"message": "You do not have permission to delete accounts"})

        toReturn = UserObject.delete_user(user_id, own_id)

        if not toReturn:
            return render(request, 'deleteAccounts.html', {"message": "Account was not deleted successfully"})

        return render(request, 'deleteAccounts.html', {"message": "You have successfully deleted account: " + user_email})


class Courses(View):
    def get(self, request):
        return render(request, 'courseView.html', {})

    def post(self, request):
        return render(request, 'courseView.html', {})


class CourseCreate(View):
    def get(self, request):
        return render(request, 'courseCreate.html', {})

    def post(self, request):
        return render(request, 'courseCreate.html', {})


class CourseEdit(View):
    def get(self, request):
        return render(request, 'courseEdit.html', {})

    def post(self, request):
        return render(request, 'courseEdit.html', {})


class Sections(View):
    def get(self, request):
        return render(request, 'sectionView.html', {})

    def post(self, request):
        return render(request, 'sectionView.html', {})


class SectionCreate(View):
    def get(self, request):
        return render(request, 'sectionCreate.html', {})

    def post(self, request):
        return render(request, 'sectionCreate.html', {})


class SectionEdit(View):
    def get(self, request):
        return render(request, 'sectionEdit.html', {})

    def post(self, request):
        return render(request, 'sectionEdit.html', {})

