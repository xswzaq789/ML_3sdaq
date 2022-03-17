# Generated by Django 4.0.3 on 2022-03-02 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BbsUser',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('user_pwd', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
            ],
        ),

        migrations.CreateModel(
            name='SBS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField(max_length=100)),
                ('title', models.TextField(max_length=100)),
                ('url', models.TextField(max_length=100)),
            ],
        ),
    ]
