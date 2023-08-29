# Generated by Django 4.2.4 on 2023-08-28 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kiosk',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('store_id', models.IntegerField(verbose_name=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.model'))),
                ('name', models.CharField(max_length=32, verbose_name='상품명')),
                ('price', models.IntegerField(verbose_name='상품가격')),
                ('stock', models.IntegerField(verbose_name='수량')),
                ('registered_date', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
            ],
            options={
                'verbose_name': '상품',
                'verbose_name_plural': '상품',
                'db_table': 'kiosk',
            },
        ),
    ]