# Generated by Django 4.0.5 on 2022-06-28 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('stage', models.IntegerField(default=1)),
                ('priority', models.CharField(choices=[('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW')], default='LOW', max_length=20)),
                ('deadline', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
