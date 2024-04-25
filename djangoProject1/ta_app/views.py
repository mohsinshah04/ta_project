from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from datetime import datetime
from .models import Role, User, Course, Semester, Assign_User_Junction
from classes.UserClass import UserObject
from classes.CourseClass import CourseClass
from classes.SemesterClass import SemesterClass
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
            return render(request, "loginPage.html", {"message": "Incorrect Email or Password, please try again."})
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


class AccountsView(View):
    def get(self, request):
        own_id = request.session.get("id")
        own_user = User.objects.get(id=own_id)
        # if own_user.User_Role.Role_Name == 'Instructor' and user.User_Role.Role_Name == 'Supervisor':
        # return render(request, 'acctsView.html', {"message": "You cannot view this account because of your role"})

        # if own_user.User_Role.Role_Name == 'TA' and (
        # ser.User_Role.Role_Name == 'Supervisor' or user.User_Role.Role_Name == 'Instructor'):
        # return render(request, 'acctsView.html', {"message": "You cannot view this account because of your role"})
        if own_user.User_Role.Role_Name != "Supervisor":
            return render(request, 'acctsView.html', {"message": "You do not have permission to view other users"})
        names = []
        emails = []
        addresses = []
        phones = []
        roles = []
        for i in User.objects.iterator():
            if i.id == own_id:
                continue
            account_string = UserObject.view_account(i.id, own_id)
            if account_string == "INVALID":
                return render(request, "acctsView.html", {"message": "Invalid account id: " + i.id})
            string = account_string.split(": ")
            names.append(string[0])
            emails.append(string[1])
            phones.append(string[2])
            addresses.append(string[3])
            roles.append(string[4])

        accounts_list = zip(names, emails, phones, addresses, roles)

        return render(request, 'acctsView.html', {"Accounts": accounts_list})
    def post(self, request):
        return render(request, 'acctsView.html', {})

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
        if User.objects.filter(User_Email=email).exists():
            return render(request, "acctsCreate.html", {"message": "This user already exists, please go to the update page if you would like to edit this user instead"})

        toReturn = UserObject.create_user(email, password, role, phone, address, f_name, l_name, own_id)
        if not toReturn:
            if len(password) < 7:
                return render(request, "acctsCreate.html", {"message": "Password is too short"})
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
            if len(password) < 7:
                return render(request, "acctsEditSelf.html", {"message": "Password is too short"})
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
            if len(password) < 7:
                return render(request, "acctsOtherEdit.html", {"message": "Password is too short"})
            return render(request, 'acctsOtherEdit.html', {"message": "Account was not updated successfully"})

        return render(request, 'acctsOtherEdit.html', {"message": "Account was updated successfully"})

class AccountDelete(View):
    def get(self, request):
        return render(request, 'deleteAccounts.html', {})

    def post(self, request):
        own_id = request.session.get('id')
        user_email = request.POST.get('User Email')
        if not User.objects.filter(User_Email=user_email).exists():
            return render(request, 'deleteAccounts.html', {"message": "Invalid email: " + user_email})
        own_user = User.objects.get(id=own_id)
        user_id = User.objects.get(User_Email=user_email).id
        if own_user.User_Role.Role_Name != "Supervisor":
            return render(request, 'deleteAccounts.html', {"message": "You do not have permission to delete accounts"})

        toReturn = UserObject.delete_user(user_id, own_id)

        if not toReturn:
            return render(request, 'deleteAccounts.html', {"message": "Account was not deleted successfully"})
        """
            send_mail(
            "Account Deletion",
            "Your account has been deleted. Please contact you supervisor for any further questions.",
            "emmettbenck@gmail.com",
            ["oliviajczarnecki@gmail.com"],
        )
        """

        return render(request, 'deleteAccounts.html', {"message": "You have successfully deleted account: " + user_email})


class Courses(View):
    def get(self, request):
        user_id = request.session.get('id')
        if not User.objects.filter(id=user_id).exists():
            return render(request, 'loginPage.html', {"message": "Please log in to view this page."})

        user = User.objects.get(id=user_id)

        if (user.User_Role.Role_Name == 'Supervisor'):
            course_details = CourseClass.viewAllAssignments(user)
        else:
            course_details = CourseClass.viewUserAssignments(user, user)

        if course_details == "INVALID":
            return render(request, 'courseView.html', {'message': 'No Courses To See Here'})

        context = {
            'courseInformation': course_details
        }

        return render(request, 'courseView.html', context)

    def post(self, request):
        return self.get(request)


class CourseCreate(View):
    def get(self, request):
        user_id = request.session.get('id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            return render(request, 'loginPage.html', {"message": "Please log in to view this page."})

        if user.User_Role.Role_Name != 'Supervisor':
            return redirect('courses')

        semesters = Semester.objects.all()
        users = User.objects.filter()
        context = {
            'semesters': semesters,
            'users': users
        }
        return render(request, 'courseCreate.html', context)

    def post(self, request):
        user_id = request.session.get('id')
        user = User.objects.get(id=user_id)
        course_code = request.POST.get('courseCode')
        course_name = request.POST.get('courseName')
        course_description = request.POST.get('courseDescription')
        semester_id = request.POST.get('semester')

        semesters = Semester.objects.all()

        if semester_id == 'new':
            semester_name = request.POST.get('semesterMonth')
            semester_year = request.POST.get('semesterYear')
            if semester_name and semester_year:
                semester = SemesterClass.createSemester(semesterTerm=semester_name, semesterYear=int(semester_year),
                                                        user=user)
                if semester:
                    sem = Semester.objects.get(Semester_Name=semester_name + " " + semester_year)
                    semester_id = sem.id
                else:
                    context = {
                        'semesters': semesters,
                        'error': 'Failed to create new semester.'
                    }
                    return render(request, 'courseCreate.html', context)

        if course_code and course_name and course_description and semester_id:
            created = CourseClass.createAssignment(course_code, course_name, course_description, semester_id, user)
            if created:
                assigned_user_ids = request.POST.getlist('assignedUsers')
                course_instance = None
                if created:
                    course_instance = Course.objects.last()
                    for user_id in assigned_user_ids:
                        user1 = User.objects.get(id=user_id)
                        CourseClass.userAssignment(course_instance.id, user1.id, user)
            else:
                context = {
                    'semesters': semesters,
                    'error': 'Invalid format or missing information. Please try again.'
                }
                return render(request, 'courseCreate.html', context)
            return redirect('courses')

        context = {
            'semesters': semesters,
            'error': 'Invalid format or missing information. Please try again.'
        }
        return render(request, 'courseCreate.html', context)


class CourseEdit(View):
    def get(self, request):
        user_id = request.session.get('id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            return render(request, 'loginPage.html', {"message": "Please log in to view this page."})

        if user.User_Role.Role_Name != 'Supervisor':
            return redirect('courses')

        courses = Course.objects.all()
        semesters = Semester.objects.all()
        users = User.objects.all()

        selected_course_id = request.GET.get('course_id')
        selected_course = Course.objects.filter(id=selected_course_id).first()

        course_code, course_full_name = "", ""
        if selected_course:
            parts = selected_course.Course_Name.split(" - ", 2)
            if len(parts) >= 3:
                course_code = parts[0] + " - " + parts[1]
                course_full_name = parts[2]
            elif len(parts) == 2:
                course_code = parts[0]
                course_full_name = parts[1]

        assigned_users_ids = []
        if selected_course:
            junctions = Assign_User_Junction.objects.filter(Course_ID=selected_course)
            assigned_users_ids = [j.User_ID.id for j in junctions]

        context = {
            'courses': courses,
            'selected_course': selected_course,
            'course_code': course_code,
            'course_full_name': course_full_name,
            'semesters': semesters,
            'users': users,
            'assigned_users_ids': assigned_users_ids,
        }
        return render(request, 'courseEdit.html', context)

    def post(self, request):
        user_id = request.session.get('id')
        user = User.objects.get(id=user_id)
        course_id = request.POST.get('course_id')
        print(course_id)
        print(user_id)
        selected_course = Course.objects.get(id=course_id)

        if user.User_Role.Role_Name != 'Supervisor':
            return redirect('courses')

        selected_course.Course_Name = request.POST.get('courseCode') + " - " + request.POST.get('courseFullName')
        selected_course.Course_Description = request.POST.get('courseDescription')
        selected_course.semester_id = request.POST.get('semester')
        selected_course.save()

        current_assigned_users = Assign_User_Junction.objects.filter(Course_ID=selected_course)
        current_assigned_user_ids = [user.User_ID_id for user in current_assigned_users]
        new_assigned_user_ids = [int(uid) for uid in request.POST.getlist('assignedUsers')]

        for user_id in new_assigned_user_ids:
            if user_id not in current_assigned_user_ids:
                CourseClass.userAssignment(selected_course.id, user_id, user)

        for user_id in current_assigned_user_ids:
            if user_id not in new_assigned_user_ids:
                CourseClass.deleteAssignment(selected_course.id, user_id)
        return redirect('courses')


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

