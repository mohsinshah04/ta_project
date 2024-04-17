from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from datetime import datetime
from .models import Role, User
# Create your views here.


class LoginPage(View):
    def get(self,request):
        return render(request,"loginPage.html",{})
    def post(self, request):
        user_doesnt_exist = False
        bad_password = False
        try:
            m = User.objects.get(User_Email=request.POST['Email'])
            bad_password = (m.User_Password != request.POST['Password'])
        except:
            user_doesnt_exist = True
        if user_doesnt_exist:
            return render(request, "loginPage.html", {"message": "email and password do not exists. Please contact supervisor to get shit this done"})
        elif bad_password:
            return render(request, "loginPage.html", {"message": "bad password"})
        else:
            request.session["email"] = m.User_Email
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
class announcements(View):
    def get(self, request):
        return render(request, 'announcements.html', {})

    def post(self, request):
        return render(request, 'announcements.html', {})
class accounts(View):
    def get(self, request):
        return render(request, 'acctsView.html', {})

    def post(self, request):
        return render(request, 'acctsView.html', {})
class accountCreate(View):
    def get(self, request):
        return render(request, 'acctsCreate.html', {})

    def post(self, request):
        return render(request, 'acctsCreate.html', {})
class accountEdit(View):
    def get(self, request):
        return render(request, 'acctsEdit.html', {})

    def post(self, request):
        return render(request, 'acctsEdit.html', {})
class accountEditOther(View):
    def get(self, request):
        return render(request, 'acctsOtherEdit.html', {})

    def post(self, request):
        return render(request, 'acctsOtherEdit.html', {})
class courses(View):
    def get(self, request):
        return render(request, 'courseView.html', {})

    def post(self, request):
        return render(request, 'courseView.html', {})
class courseCreate(View):
    def get(self, request):
        return render(request, 'courseCreate.html', {})

    def post(self, request):
        return render(request, 'courseCreate.html', {})
class courseEdit(View):
    def get(self, request):
        return render(request, 'courseEdit.html', {})

    def post(self, request):
        return render(request, 'courseEdit.html', {})
class sections(View):
    def get(self, request):
        return render(request, 'sectionView.html', {})

    def post(self, request):
        return render(request, 'sectionView.html', {})
class sectionCreate(View):
    def get(self, request):
        return render(request, 'sectionCreate.html', {})

    def post(self, request):
        return render(request, 'sectionCreate.html', {})
class sectionEdit(View):
    def get(self, request):
        return render(request, 'sectionEdit.html', {})

    def post(self, request):
        return render(request, 'sectionEdit.html', {})

