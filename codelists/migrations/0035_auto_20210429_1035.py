# Generated by Django 3.1.8 on 2021-04-29 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("codelists", "0034_auto_20210429_1029"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="codelist",
            name="codelists_codelist_organisation_xor_user",
        ),
        migrations.AlterUniqueTogether(
            name="codelist",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="codelist",
            name="name",
        ),
        migrations.RemoveField(
            model_name="codelist",
            name="organisation",
        ),
        migrations.RemoveField(
            model_name="codelist",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="codelist",
            name="user",
        ),
    ]
