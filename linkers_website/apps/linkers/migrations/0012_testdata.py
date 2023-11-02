# Generated by Django 4.2.2 on 2023-07-26 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkers', '0011_alter_linker_region_alter_linker_secondary_structure'),
    ]

    operations = [
        migrations.CreateModel(
            name='testdata',
            fields=[
                ('id', models.CharField(default='1', max_length=15, primary_key=True, serialize=False)),
                ('Sequence', models.CharField(max_length=100)),
                ('backbone', models.CharField()),
                ('average_flexibility', models.FloatField(default=0)),
            ],
        ),
    ]