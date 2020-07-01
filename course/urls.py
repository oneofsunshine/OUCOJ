from django.conf.urls import url

from .views import CourseAPI, CourseGradeAPI, CourseContestAPI, CourseUserAPI, CourseJoinRequestAnswer

urlpatterns = [
    url(r"^courses/?$", CourseAPI.as_view(), name="course_list_api"),
    url(r"^course/grade/?$", CourseGradeAPI.as_view(), name="course_grade_api"),
    url(r"^course/contest/?$", CourseContestAPI.as_view(), name="course_contest_api"),
    url(r"^course/user/?$", CourseUserAPI.as_view(), name="course_user_api"),
    url(r"^course/user_requests/?$", CourseJoinRequestAnswer.as_view(), name="course_user_request_api"),
]