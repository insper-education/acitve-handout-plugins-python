# Generated by Django 4.1.2 on 2022-12-31 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_exercisetag_unique_course_tag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
