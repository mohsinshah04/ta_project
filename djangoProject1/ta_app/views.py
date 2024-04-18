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
            return render(request, "loginPage.html", {"message": "bad password"})
        else:
            request.session["id"] = m.id
            return redirect("/home/")


class LogOutPage(View):
    def get(self, request):
        return render(request, 'logOutPage.html', {})

    def post(self, request):
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


class Accounts(View):
    def get(self, request):
        return render(request, 'acctsView.html', {})

    def post(self, request):
        own_id = request.session.get("id")
        user_id = request.POST.get('id')
        if not User.objects.filter(id=user_id).exists():
            return render(request, 'acctsView.html', {"message": "Invalid account id: " + user_id})
        own_user = User.objects.get(id=own_id)
        user = User.objects.get(id=user_id)
        if own_user.User_Role.Role_Name == 'Instructor' and user.User_Role.Role_Name == 'Supervisor':
            return render(request, 'acctsView.html', {"message": "You cannot view this account because of your role"})

        if own_user.User_Role.Role_Name == 'TA' and (user.User_Role.Role_Name == 'Supervisor' or user.User_Role.Role_Name == 'Instructor'):
            return render(request, 'acctsView.html', {"message": "You cannot view this account because of your role"})

        account_string = UserObject.view_account(user_id, own_id)
        if account_string == "INVALID":
            return render(request, "acctsView.html", {"message": "Invalid account id: " + user_id})
        name = account_string.split(":")
        return render(request, 'acctsView.html', {"name": name[0], "role": name[1]})


class AccountCreate(View):
    def get(self, request):
        return render(request, 'acctsCreate.html', {})

    def post(self, request):
        get_all_info = False
        try:
            own_id = request.session.get("id")
            own_user = User.objects.get(id=own_id)
            if own_user.User_Role.Role_Name != "Supervisor":
                return render(request, "acctsView.html", {"message": "You do not have permission to create users"})

            f_name = request.POST.get('First Name')
            l_name = request.POST.get('Last Name')
            email = request.POST.get('Email')
            password = request.POST.get('Password')
            role_name = request.POST.get('Role')
            name = role_name.split(": ")
            role = Role(Role_Name=name[1])
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


class AccountEdit(View):
    def get(self, request):
        return render(request, 'acctsEdit.html', {})

    def post(self, request):
        get_all_info = False
        try:
            own_id = request.session.get('id')
            user_id = int(request.POST.get('id'))
            if own_id is not user_id:
                return render(request, 'acctsEdit.html', {"message": "Account ids do not match"})
            f_name = request.POST.get('First Name')
            l_name = request.POST.get('Last Name')
            email = request.POST.get('Email')
            password = request.POST.get('Password')
            address = request.POST.get('Address')
            phone = request.POST.get('Phone Number')
        except:
            get_all_info = True

        if get_all_info:
            return render(request, 'acctsEdit.html', {"message": "Please enter all information correctly"})

        toReturn = UserObject.edit_user(user_id, email, password, phone, address, f_name, l_name, own_id)

        if not toReturn:
            return render(request, 'acctsEdit.html', {"message": "Account was not updated successfully"})

        return render(request, 'acctsEdit.html', {"message": "Account was updated successfully"})


class AccountEditOther(View):
    def get(self, request):
        return render(request, 'acctsOtherEdit.html', {})

    def post(self, request):
        return render(request, 'acctsOtherEdit.html', {})


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

