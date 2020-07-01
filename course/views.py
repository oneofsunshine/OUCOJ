import io
import xlsxwriter

from django.http import HttpResponse
from django.db.models import Q

from account.decorators import super_admin_required
from account.models import User, AdminType
from problem.models import Problem
from contest.models import Contest, ACMContestRank
from .models import Course, JoinCourseRequest
from utils.api import APIView, validate_serializer
from account.serializers import UserAdminSerializer
from contest.serializers import ContestAdminSerializer
from .serializers import (CourseUserRequestSerializer, CourseSerializer, CourseUserJoinRequestSerializer,
                          CourseContestRequestSerializer, CreateCourseSerializer,
                          EditCourseSerializer, JoinCourseRequestSerializer, )


class CourseAPI(APIView):
    @validate_serializer(CreateCourseSerializer)
    @super_admin_required
    def post(self, request):
        data = request.data
        if not data["name"].isdigit():
            return self.error("Course name must be digital")
        if not data["s_year"].isdigit():
            return self.error("Course year must be digital")
        if Course.objects.filter(name=data["name"], s_year=data["s_year"]).exists():
            return self.error("Course already exists")

        course = Course.objects.create(name=data["name"],
                                       s_year=data["s_year"],
                                       short_description=data["short_description"])
        return self.success(CourseSerializer(course).data)

    @validate_serializer(EditCourseSerializer)
    @super_admin_required
    def put(self, request):
        data = request.data
        course_id = data.pop("id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        if not data["name"].isdigit():
            return self.error("Course name must be digital")
        if not data["s_year"].isdigit():
            return self.error("Course year must be digital")
        if Course.objects.filter(name=data["name"], s_year=data["s_year"]).exclude(id=course_id).exists():
            return self.error("Course already exists")

        course.name = data["name"]
        course.s_year = data["s_year"]
        course.short_description = data["short_description"]
        course.save()

        return self.success(CourseSerializer(course).data)

    @super_admin_required
    def get(self, request):
        courses = Course.objects.all().order_by("-id")
        keyword = request.GET.get("keyword")
        if keyword:
            courses = courses.filter(Q(name__icontains=keyword) |
                                     Q(short_description__icontains=keyword) |
                                     Q(s_year__icontains=keyword))
        return self.success(self.paginate_data(request, courses, CourseSerializer))

    @super_admin_required
    def delete(self, request):
        """
        Delete one course.
        """
        course_id = request.GET.get("id")
        if course_id:
            try:
                Course.objects.get(id=course_id).delete()
            except Course.DoesNotExist:
                return self.error("Course does not exist")

        else:
            self.error("Parameter wrong")
        return self.success()


class CourseJoinRequestAnswer(APIView):
    @super_admin_required
    def get(self, request):
        course_id = request.GET.get("course_id")
        handle_request = request.GET.get("handle_request") == "1"
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return self.error("Course does not exist")
        else:
            self.error("Parameter wrong")
        join_requests = course.join_course_requests.select_related("user").\
            filter(status=handle_request).order_by("accepted", "user__sno")
        keyword = request.GET.get("keyword")
        if keyword:
            join_requests = join_requests.filter(Q(user__username__icontains=keyword) |
                                                 Q(user__userprofile__real_name__icontains=keyword) |
                                                 Q(user__sno__icontains=keyword)).order_by("user__sno")
        return self.success(self.paginate_data(request, join_requests, JoinCourseRequestSerializer))

    @validate_serializer(CourseUserJoinRequestSerializer)
    @super_admin_required
    def post(self, request):
        """
        agree or Refuse user join requests.
        """
        data = request.data
        try:
            course = Course.objects.get(id=data["course_id"])
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        join_requests = course.join_course_requests.filter(id__in=data["user_request_ids"])
        if data["is_agree"] == "1":
            for jrs in join_requests:
                jrs.status = True
                jrs.accepted = True
                course.students.add(jrs.user)
                jrs.save()
        elif data["is_agree"] == "0":
            for jrs in join_requests:
                jrs.status = True
                jrs.accepted = False
                jrs.save()
        else:
            self.error("parameter is_agree wrong")
        return self.success()


class CourseContestAPI(APIView):
    @super_admin_required
    def get(self, request):
        course_id = request.GET.get("course_id")
        is_add = request.GET.get("is_add") == "1"
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        contests = course.contests.all().order_by("-id")
        if is_add:
            contests = Contest.objects.all().difference(contests).order_by("-id")

        return self.success(self.paginate_data(request, contests, ContestAdminSerializer))

    @validate_serializer(CourseContestRequestSerializer)
    @super_admin_required
    def post(self, request):
        """
        Add or Remove course contest.
        """
        data = request.data
        try:
            course = Course.objects.get(id=data["course_id"])
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        contests = Contest.objects.filter(id__in=data["contest_ids"])
        if data["is_add"] == "1":
            for con in contests:
                if con not in course.contests.all():
                    course.contests.add(con)
        elif data["is_add"] == "0":
            for con in contests:
                if con in course.contests.all():
                    course.contests.remove(con)
        else:
            self.error("is_add wrong")
        return self.success()


class CourseUserAPI(APIView):
    @super_admin_required
    def get(self, request):
        course_id = request.GET.get("course_id")
        is_add = request.GET.get("is_add") == "1"
        keyword = request.GET.get("keyword", None)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")

        users = course.students.all().order_by("sno")
        if keyword:
            users = users.filter(Q(username__icontains=keyword) |
                                 Q(userprofile__real_name__icontains=keyword) |
                                 Q(sno__icontains=keyword)).order_by("sno")
            if is_add:
                users_tmp = User.objects.all().exclude(Q(username__icontains=keyword) |
                                                       Q(userprofile__real_name__icontains=keyword) |
                                                       Q(sno__icontains=keyword)) | users
                users = User.objects.all().difference(users_tmp).order_by("-sno")

        else:
            if is_add:
                users = User.objects.all().difference(users).order_by("-sno")

        return self.success(self.paginate_data(request, users, UserAdminSerializer))

    @validate_serializer(CourseUserRequestSerializer)
    @super_admin_required
    def post(self, request):
        """
        Add or Remove course user.
        """
        data = request.data
        try:
            course = Course.objects.get(id=data["course_id"])
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        users = User.objects.filter(id__in=data["user_ids"])
        if data["is_add"] == "1":
            for stu in users:
                if stu not in course.students.all():
                    course.students.add(stu)
        elif data["is_add"] == "0":
            for stu in users:
                if stu in course.students.all():
                    course.students.remove(stu)
                    try:
                        course.join_course_requests.get(user=stu).delete()
                    except JoinCourseRequest.DoesNotExist:
                        return self.error("Join course request does not exist")
        else:
            self.error("is_add wrong")
        return self.success()


class CourseGradeAPI(APIView):
    @super_admin_required
    def get(self, request):
        course_id = request.GET.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return self.error("Course does not exist")
        contests = course.contests.all().order_by("id")
        if contests.count() < 1:
            return self.error("This course has no contest")

        sno = request.GET.get("sno")
        if sno:
            students = User.objects.select_related("userprofile").filter(sno=sno, is_disabled=False)
        else:
            students = course.students.filter(admin_type=AdminType.REGULAR_USER, is_disabled=False).\
                select_related("userprofile").order_by("sno")
        if students.count() < 1:
            return self.error("Student does not exist")

        f = io.BytesIO()
        workbook = xlsxwriter.Workbook(f)
        worksheet = workbook.add_worksheet()

        worksheet.write("A1", "User ID")
        worksheet.write("B1", "Sno")
        worksheet.write("C1", "Real Name")

        contest_number = contests.count()
        contest_ids = [item.id for item in contests]
        for index, cid in enumerate(contest_ids):
            worksheet.write(0, 3 + 2 * index, str('C' + str(cid) + "_ac"))
            worksheet.write(0, 4 + 2 * index, str('C' + str(cid) + "_submit"))
        worksheet.write(0, contest_number * 2 + 3, "total_ac")
        worksheet.write(0, contest_number * 2 + 4, "total_submission")

        for index, stu in enumerate(students):
            worksheet.write(index + 1, 0, stu.id)
            worksheet.write(index + 1, 1, stu.userprofile.major)
            worksheet.write(index + 1, 2, stu.userprofile.real_name)

            total_ac = 0
            total_submission = 0

            for i, con in enumerate(contests):
                if ACMContestRank.objects.filter(contest=con, user=stu).count() > 0:
                    rank = ACMContestRank.objects.filter(contest=con).get(user=stu)
                    total_ac += rank.accepted_number
                    total_submission += rank.submission_number

                    worksheet.write(index + 1, 3 + 2 * i, rank.accepted_number)
                    worksheet.write(index + 1, 4 + 2 * i, rank.submission_number)
                else:
                    worksheet.write(index + 1, 3 + 2 * i, 0)
                    worksheet.write(index + 1, 4 + 2 * i, 0)

            worksheet.write(index + 1, contest_number * 2 + 3, total_ac)
            worksheet.write(index + 1, contest_number * 2 + 4, total_submission)

        worksheet2 = workbook.add_worksheet()
        worksheet2.write("A1", "Contest ID")
        worksheet2.write("B1", "Contest Title")
        worksheet2.write("C1", "Contest Problems Number")
        total_problem = 0
        for index, con in enumerate(contests):
            worksheet2.write(index + 1, 0, con.id)
            worksheet2.write(index + 1, 1, con.title)
            con_pro_num = Problem.objects.filter(contest=con, visible=True).count()
            total_problem += con_pro_num
            worksheet2.write(index + 1, 2, con_pro_num)
        worksheet2.write(contests.count() + 1, 2, total_problem)

        workbook.close()
        f.seek(0)
        response = HttpResponse(f.read())
        response["Content-Disposition"] = f"attachment; filename=course-{course.name}-grade.xlsx"
        response["Content-Type"] = "application/xlsx"
        return response

