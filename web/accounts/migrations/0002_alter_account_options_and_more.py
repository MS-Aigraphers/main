# Generated by Django 4.2.4 on 2023-09-04 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': '유저 정보'},
        ),
        migrations.RenameField(
            model_name='account',
            old_name='store_ID',
            new_name='username',
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=200),
        ),
        migrations.AlterModelTable(
            name='account',
            table='account_user',
        ),
    ]
