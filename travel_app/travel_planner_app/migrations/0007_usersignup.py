# Generated by Django 4.2.3 on 2023-07-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_planner_app', '0006_rename_name_review_name_of_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSignup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
