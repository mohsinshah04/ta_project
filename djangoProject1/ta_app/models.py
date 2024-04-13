from django.db import models

# Create your models here.

class Role(models.Model):
    Role_Name = models.CharField(max_length=50)
    def __str__(self):
        return "Role: " + self.Role_Name
class User(models.Model):
    User_Password = models.CharField(max_length=50, default="null")
    User_Email = models.CharField(max_length=50, default="null")
    User_FName = models.CharField(max_length=50, default="null")
    User_LName = models.CharField(max_length=50, default="null")
    User_Home_Address = models.CharField(max_length=50, default="null")
    User_Phone_Number = models.CharField(max_length=15, default="null")
    User_Role = models.ForeignKey(Role,on_delete=models.CASCADE)
    User_ID = models.IntegerField(default=0)

    def __str__(self):
        return ("User FName: " + self.User_FName +
                "\n LName: " + self.User_LName +
                "\n Home Address: " + self.User_Home_Address +
                "\n Email: " + self.User_Email +
                "\n Phone Number: " + self.User_Phone_Number +
                "\n Password: " + self.User_Password)


class Semester(models.Model):
    Semester_Name = models.CharField(max_length=50)
    def __str__(self):
        return ("Semester Name: " + self.Semester_Name)
class Course(models.Model):
    Course_Name = models.CharField(max_length=50)
    Course_Description = models.CharField(max_length=200)
    Course_Semester_ID = models.ForeignKey(Semester, on_delete=models.CASCADE)
    def __str__(self):
        return ("Course Name: " + self.Course_Name +
                " \n Description: " + self.Course_Description)
class Section(models.Model):
    Is_Lab = models.BooleanField()
    Section_Meet = models.DateTimeField()
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return ("Is Lab: " + self.Is_Lab +
                "\nSection Meet: " + self.Section_Meet +
                "\n Course ID: " + self.Course_ID)

class Assign_User_Junction(models.Model):
    User_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    Course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    Section_ID = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ('User_ID', 'Course_ID')

    def __str__(self):
        return("User Email: " + str(self.User_ID.User_Email) + " ---> To Course Name: " + str(self.Course_ID.Course_Name) + " ---> For Semester: " + str(self.Section_ID))

