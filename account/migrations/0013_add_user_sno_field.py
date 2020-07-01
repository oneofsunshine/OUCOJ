from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_userprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sno',
            field=models.TextField(null=True),
        ),
    ]
