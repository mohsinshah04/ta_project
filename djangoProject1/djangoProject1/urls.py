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
from ta_app.views import (Home, LoginPage, LogOutPage, Announcements,
                          Accounts, AccountCreate, AccountEdit, AccountEditOther,
                          Courses, CourseCreate, CourseEdit,
                          Sections, SectionCreate, SectionEdit, AccountDelete)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPage.as_view()),
    path('home/', Home.as_view(), name='login'),
    path('logout/', LogOutPage.as_view(), name='logout'),
    path('announcements/', Announcements.as_view(), name='announcements'),
    path('accounts/', Accounts.as_view(), name='accounts'),
    path('accountCreate/', AccountCreate.as_view(), name='accountCreate'),
    path('accountEdit/', AccountEdit.as_view(), name='accountEdit'),
    path('accountEditOther/', AccountEditOther.as_view(), name='accountEditOther'),
    path('deleteAccount', AccountDelete.as_view(), name='deleteAccount'),
    path('courses/', Courses.as_view(), name='courses'),
    path('courseCreate/', CourseCreate.as_view(), name='courseCreate'),
    path('courseEdit/', CourseEdit.as_view(), name='courseEdit'),
    path('sections/', Sections.as_view(), name='sections'),
    path('sectionCreate/', SectionCreate.as_view(), name='sectionCreate'),
    path('sectionEdit/', SectionEdit.as_view(), name='sectionEdit'),

]
