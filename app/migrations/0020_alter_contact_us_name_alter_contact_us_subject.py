# Generated by Django 5.1.4 on 2024-12-09 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_contact_us_name_alter_contact_us_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_us',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contact_us',
            name='subject',
            field=models.CharField(max_length=100),
        ),
    ]