# Generated by Django 3.0.7 on 2020-07-22 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("codelists", "0006_auto_20200722_1437"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="codelist",
            name="csv_data",
        ),
        migrations.RemoveField(
            model_name="codelist",
            name="version_str",
        ),
    ]
