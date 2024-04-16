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
            m = User.objects.get(User_Email=request.POST['email'])
            bad_password = (m.password != request.POST['password'])
        except:
            user_doesnt_exist = True
        if user_doesnt_exist:
            return render(request, "loginPage.html", {"message": "email and password do not exists. Please contact supervisor to get shit this done"})
        elif bad_password:
            return render(request, "loginPage.html", {"message": "bad password"})
        else:
            request.session["email"] = m.User_Email
            return redirect("/home.html/")
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
class courses(View):
    def get(self, request):
        return render(request, 'courseView.html', {})

    def post(self, request):
        return render(request, 'courseView.html', {})
class LogOutPage(View):
    def get(self, request):
        return render(request, 'logOutPage.html', {})

    def post(self, request):
        return render(request, 'logOutPage.html', {})