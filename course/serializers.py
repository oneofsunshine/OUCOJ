from utils.api import serializers

from .models import Course, JoinCourseRequest


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ("students", "contests")


class CourseToAddSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=20)
    s_year = serializers.CharField(max_length=4)
    short_description = serializers.CharField(max_length=40, required=False)
    is_exist = serializers.BooleanField()
    status = serializers.BooleanField()


class JoinCourseRequestSerializer(serializers.ModelSerializer):
    request_username = serializers.CharField(source='user.username')
    request_sno = serializers.CharField(source='user.sno')
    request_real_name = serializers.CharField(source='user.userprofile.real_name')

    class Meta:
        model = JoinCourseRequest
        exclude = ("user", "course")


class CourseUserJoinRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    is_agree = serializers.CharField(max_length=1)
    user_request_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)


class CourseContestRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    is_add = serializers.CharField(max_length=1)
    contest_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)


class CourseUserRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    is_add = serializers.CharField(max_length=1)
    user_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)


class CreateCourseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    s_year = serializers.CharField(max_length=4)
    short_description = serializers.CharField(max_length=40, required=False)


class EditCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=20, required=False)
    s_year = serializers.CharField(max_length=4)
    short_description = serializers.CharField(max_length=40, required=False)