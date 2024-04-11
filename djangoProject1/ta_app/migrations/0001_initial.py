# Generated by Django 5.0.3 on 2024-04-11 02:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Course_Name', models.CharField(max_length=50)),
                ('Course_Description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role_Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Semester_Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Is_Lab', models.BooleanField()),
                ('Section_Meet', models.DateTimeField()),
                ('Course_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_app.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='Course_Semester_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_app.semester'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Password', models.CharField(max_length=50)),
                ('User_Email', models.CharField(max_length=50)),
                ('User_FName', models.CharField(max_length=50)),
                ('User_LName', models.CharField(max_length=50)),
                ('User_Home_Address', models.CharField(max_length=50)),
                ('User_Role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_app.role')),
            ],
        ),
        migrations.CreateModel(
            name='Assign_User_Junction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Course_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_app.course')),
                ('Section_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_app.section')),
                ('User_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ta_app.user')),
            ],
            options={
                'unique_together': {('User_ID', 'Course_ID')},
            },
        ),
    ]