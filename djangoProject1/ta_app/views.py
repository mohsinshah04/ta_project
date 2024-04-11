from django.shortcuts import render
from django.views import View
from datetime import datetime
from .models import Role
# Create your views here.

class Home(View):
    def post(self, request):
        print("Hello World!")

