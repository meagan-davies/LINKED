# Generated by Django 4.2.2 on 2023-08-09 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test3', '0005_remove_flexibility_pdb_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexibility',
            name='backbone',
            field=models.CharField(default='NA'),
        ),
    ]