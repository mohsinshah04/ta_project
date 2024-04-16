"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ta_app.views import (Home, LoginPage, LogOutPage, announcements,
                          accounts, accountCreate, accountEdit, accountEditOther,
                          courses, courseCreate, courseEdit,
                          sections, sectionCreate, sectionEdit)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogOutPage.as_view(), name='logout'),
    path('announcements/', announcements.as_view(), name='announcements'),
    path('accounts/', accounts.as_view(), name='accounts'),
    path('accountCreate/', accountCreate.as_view(), name='accountCreate'),
    path('accountEdit/', accountEdit.as_view(), name='accountEdit'),
    path('accountEditOther/', accountEditOther.as_view(), name='accountEditOther'),
    path('courses/', courses.as_view(), name='courses'),
    path('courseCreate/', courseCreate.as_view(), name='courseCreate'),
    path('courseEdit/', courseEdit.as_view(), name='courseEdit'),
    path('sections/', sections.as_view(), name='sections'),
    path('sectionCreate/', sectionCreate.as_view(), name='sectionCreate'),
    path('sectionEdit/', sectionEdit.as_view(), name='sectionEdit'),

]
