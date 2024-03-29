# Generated by Django 4.2.9 on 2024-01-17 10:42

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('number', phone_field.models.PhoneField(max_length=31)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('spam_reports', models.IntegerField(default=0)),
                ('is_spam', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', phone_field.models.PhoneField(max_length=31, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('hashed_password', models.CharField(max_length=255)),
                ('is_logged_in', models.BooleanField(default=False)),
                ('personal_contacts', models.ManyToManyField(blank=True, to='api.contact')),
            ],
        ),
        migrations.CreateModel(
            name='SpamReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reported_number', phone_field.models.PhoneField(max_length=31)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.registereduser')),
            ],
        ),
    ]
