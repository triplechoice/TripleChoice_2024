# Generated by Django 4.0 on 2021-12-21 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0021_rename_order_requestreview_request_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectedRequestReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.request')),
                ('review', models.ManyToManyField(to='order.RequestReview')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
