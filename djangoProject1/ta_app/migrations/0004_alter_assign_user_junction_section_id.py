# Generated by Django 5.0.3 on 2024-04-12 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ta_app', '0003_alter_user_user_email_alter_user_user_fname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assign_user_junction',
            name='Section_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ta_app.section'),
        ),
    ]
