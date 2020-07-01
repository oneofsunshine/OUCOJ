from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('s_year', models.CharField(max_length=4)),
                ('short_description', models.CharField(max_length=40, default='ownerless')),
                ('contests', models.ManyToManyField(to='contest.Contest')),
                ('students', models.ManyToManyField(to='account.User')),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='JoinCourseRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name="join_course_requests", to='course.Course')),
            ],
            options={
                'db_table': 'join_course_request',
            },
        ),
    ]