from django.db import models

from account.models import User
from contest.models import Contest


class Course(models.Model):
    name = models.TextField()
    s_year = models.CharField(max_length=4)
    short_description = models.TextField(default="ownerless")
    contests = models.ManyToManyField(Contest)
    students = models.ManyToManyField(User)

    class Meta:
        db_table = "course"
        unique_together = (("name", "s_year"),)


class JoinCourseRequest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="join_course_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    class Meta:
        db_table = "join_course_request"
        unique_together = (("user", "course"),)

