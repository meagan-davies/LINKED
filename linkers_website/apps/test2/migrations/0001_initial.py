# Generated by Django 4.2.2 on 2023-07-24 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='testdata',
            fields=[
                ('id', models.CharField(default='1', max_length=15, primary_key=True, serialize=False)),
                ('Sequence', models.CharField(max_length=100)),
                ('backbone', models.CharField(max_length=10000)),
            ],
        ),
    ]
