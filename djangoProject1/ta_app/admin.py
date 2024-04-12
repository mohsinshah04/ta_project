from django.contrib import admin

from .models import User, Role, Semester, Assign_User_Junction, Course, Section

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Semester)
admin.site.register(Assign_User_Junction)
admin.site.register(Course)
admin.site.register(Section)