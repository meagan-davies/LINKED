# Generated by Django 4.2.2 on 2023-07-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkers', '0007_alter_linker_origin_alter_linker_aasequence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linker',
            name='length',
            field=models.PositiveIntegerField(max_length=50),
        ),
    ]
