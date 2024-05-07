"""Currently Skeleton Class for Section"""
from ta_app.models import Course, Section, Semester, Assign_User_Junction, User
import re
import datetime
class SectionClass:
    def __init__(self):
        pass

    @classmethod
    def createAssignment(self, classID, sectionNum, sectionType, sectionMeetsDays, sectionCampus, sectionStartDate, sectionEndDate, sectionCredits, sectionStartTimes, sectionEndTimes, buldingName, roomNum, userID):
        if (userID == None):
            return False
        user = User.objects.get(id=userID)
        if (user.User_Role.Role_Name == "TA"):
            return False

        if (classID == None) or (sectionNum == None) or (sectionType == None) or (sectionMeetsDays == None) or (sectionCampus == None) or (sectionStartDate == None) or (sectionEndDate == None) or (sectionCredits == None) or (sectionStartTimes == None) or (sectionEndTimes == None) or (buldingName == None) or (roomNum == None) or (userID == None):
            return False

        if(type(sectionNum) ==int):
            return False
        if (type(sectionType) == int):
            return False
        if(type(sectionMeetsDays) != list ):
            return False

        if(type(sectionCampus) == int):
            return False
        if(type(sectionCredits) != int):
            return False
        if (sectionCredits <0):
            return False
        if(type(sectionStartTimes) ==int):
            return False
        if (type(sectionEndTimes) == int):
            return False
        if (type(buldingName) == int):
            return False
        if (type(roomNum) == int):
            return False
        try:
            course = Course.objects.get(id=classID)
            section = Section(
                Course_ID=course,
                Section_Number=sectionNum,
                Section_Type=sectionType,
                Meets_Days=sectionMeetsDays,
                Campus=sectionCampus,
                Start_Date=datetime.datetime.strptime(sectionStartDate, '%Y-%m-%d').date(),
                End_Date=datetime.datetime.strptime(sectionEndDate, '%Y-%m-%d').date(),
                Credits=sectionCredits,
                Start_Times=sectionStartTimes,
                End_Times=sectionEndTimes,
                Building_Name=buldingName,
                Room_Number=roomNum
            )
            section.save()
            return section
        except Exception as e:
            return False, str(e)


    @classmethod
    def editAssignment(self, section_id, assigned_user_ids, user):
        if (user == None):
            return False
        user_role = User.objects.get(id=user).User_Role.Role_Name
        if user_role in ['TA']:
            return False

        if section_id:
            section = Section.objects.get(id=section_id)
            course_id = section.Course_ID.id


            Assign_User_Junction.objects.filter(Section_ID=section).delete()

            for user_id in assigned_user_ids:
                Assign_User_Junction.objects.create(
                    User_ID_id=user_id,
                    Course_ID_id=course_id,
                    Section_ID_id=section_id
                )
            return True
        else:
            return False



    @classmethod
    def userAssignment(self, courseID, userID, user):
        if (courseID == None):
            return False
        if (userID == None):
            return False
        if (user == None):
            return False
        if (User.objects.filter(id=user.id).exists() == False):
            return "INVALID"
        if (Course.objects.filter(id=courseID).exists() == False):
            return False
        if (User.objects.filter(id=userID).exists() == False):
            return False
        if ((User.objects.get(id=userID).User_Role.Role_Name != 'TA')
                and (User.objects.get(id=userID).User_Role.Role_Name != 'Instructor')):
            return False
        if user.User_Role.Role_Name != 'Supervisor':
            return False

        if(Assign_User_Junction.objects.filter(Course_ID=Course.objects.get(id=courseID), User_ID=User.objects.get(id=userID)).exists()):
            return True

        assigned = Assign_User_Junction.objects.create(Course_ID=Course.objects.get(id=courseID), User_ID=User.objects.get(id=userID))

        if(assigned == None):
            return False

        return True

    @classmethod
    def deleteAssignment(self, courseID, user):
        pass

    @classmethod
    def viewAllSectionAssignments(self, user_id):
        pass

    @classmethod
    def viewUserAssignments(self, user_id, course_id):
        if(User.objects.filter(id=user_id).exists() == False):
            return False

        user_role = User.objects.get(id=user_id).User_Role.Role_Name
        if user_role in ['Supervisor']:
            courses_query = Course.objects.all() if not course_id else Course.objects.filter(id=course_id)
        else:
            courses_query = Assign_User_Junction.objects.filter(
                User_ID=user_id,

            ).select_related('Course_ID').distinct()


        courses = [course_junction.Course_ID for course_junction in
                   courses_query] if user_role != 'Supervisor' else courses_query

        if user_role != 'Supervisor':
            sections = Section.objects.filter(
                Course_ID__in=courses,

            ).distinct()
        else:
            sections = Section.objects.filter(
                Course_ID__in=courses
            ).select_related('Course_ID')


        sections_data = []
        for section in sections:
            assigned_users = section.assign_user_junction_set.all().select_related('User_ID')
            assigned_user_details = [
                f"{au.User_ID.User_FName} {au.User_ID.User_LName} ({au.User_ID.User_Role})"
                for au in assigned_users
            ]
            sections_data.append({
                'course_name': section.Course_ID.Course_Name,
                'section_number': section.Section_Number,
                'section_type': section.Section_Type,
                'meets_days': section.Meets_Days,
                'campus': section.Campus,
                'start_date': section.Start_Date.strftime('%Y-%m-%d'),
                'end_date': section.End_Date.strftime('%Y-%m-%d'),
                'credits': section.Credits,
                'start_times': section.Start_Times,
                'end_times': section.End_Times,
                'building': section.Building_Name,
                'room_number': section.Room_Number,
                'assigned_users': ', '.join(assigned_user_details)
            })

        context = {
            'courses': courses,
            'sections': sections_data
        }
        return context
