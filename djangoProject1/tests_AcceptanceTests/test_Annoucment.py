from django.test import TestCase, Client

from ta_app.models import User, Role


class AnnouncementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.role = Role(Role_Name="Supervisor")
        self.role.save()
        self.test_user = User.objects.create(User_Email="user@uwm.edu", User_Role=self.role, User_Password=
                                             "<PASSWORD>", User_Phone_Number="3333333333", User_Home_Address="123 Milwaukee St",
                                             User_FName="John", User_LName="User")
        self.test_user.save()
        self.client.post("/", {"Email": self.test_user.User_Email, "Password": self.test_user.User_Password}, follow=True)

    def test_redirect_to_announcement(self):
        response = self.client.post("/announcements/", {"User_List": self.test_user, "Message": "This is a test message"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_page_not_found(self):
        response = self.client.post("/announcements/", {"User_List": self.test_user, "Message": "This is a test message"}, follow=True)
        self.assertNotEqual(response.status_code, 404)

    def test_announcement_success(self):
        response = self.client.post("/announcements/", {"User_List": self.test_user, "Message": "This is a test message"}, follow=True)
        self.assertEqual(response.context['message'], "Announcement sent!")