# Generated by Django 2.0.4 on 2018-06-10 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cith2', '0007_auto_20180608_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='plz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Cith2.Plz'),
        ),
    ]
