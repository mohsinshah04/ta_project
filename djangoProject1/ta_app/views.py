from django.shortcuts import render
from django.views import View
from datetime import datetime
from .models import Role
# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, 'home.html', {})
    def post(self, request):
        print("Hello World!")
        return render(request, 'home.html', {})

