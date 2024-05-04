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
                          AccountViewSelf, AccountCreate, AccountEditSelf, AccountEditOther,
                          Courses, CourseCreate, CourseEdit, AccountsViewTA_IN,
                          Sections, SectionCreate, SectionEdit, AccountDelete, AccountsView, AccountsViewSelfTA_IN,
                          CoursesTA_IN)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginPage.as_view()),
    path('login/', LoginPage.as_view(), name='login'),
    path('home/', Home.as_view(), name='home'),
    path('logout/', LogOutPage.as_view(), name='logout'),
    path('announcements/', Announcements.as_view(), name='announcements'),
    path('accountsViewSelf/', AccountViewSelf.as_view(), name='account'),
    path('accountsViewSelfTA_IN', AccountsViewSelfTA_IN.as_view(), name='accountsViewSelfTA_IN'),
    path('accountCreate/', AccountCreate.as_view(), name='accountCreate'),
    path('accountEditSelf/', AccountEditSelf.as_view(), name='accountEditSelf'),
    path('accountEditOther/', AccountEditOther.as_view(), name='accountEditOther'),
    path('accountsView/', AccountsView.as_view(), name='accountsView'),
    path('accountsViewTA_IN', AccountsViewTA_IN.as_view(), name='accountsViewTA_In'),
    path('deleteAccounts/', AccountDelete.as_view(), name='deleteAccounts'),
    path('courses/', Courses.as_view(), name='courses'),
    path('coursesTA_IN/', CoursesTA_IN.as_view(), name='courses'),
    path('courseCreate/', CourseCreate.as_view(), name='courseCreate'),
    path('courseEdit/', CourseEdit.as_view(), name='courseEdit'),
    path('sections/', Sections.as_view(), name='sections'),
    path('sectionCreate/', SectionCreate.as_view(), name='sectionCreate'),
    path('sectionEdit/', SectionEdit.as_view(), name='sectionEdit'),

]
