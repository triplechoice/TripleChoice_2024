# Generated by Django 4.1.2 on 2022-10-27 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0090_request_image_comment_requesthistory_image_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='image_comment',
            field=models.FileField(blank=True, null=True, upload_to='post/'),
        ),
        migrations.AlterField(
            model_name='requesthistory',
            name='image_comment',
            field=models.FileField(blank=True, null=True, upload_to='post/'),
        ),
    ]
