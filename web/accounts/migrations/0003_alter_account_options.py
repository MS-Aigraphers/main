# Generated by Django 4.2.4 on 2023-09-05 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': '계정 정보'},
        ),
    ]