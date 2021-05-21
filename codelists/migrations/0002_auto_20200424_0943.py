# Generated by Django 2.2.11 on 2020-04-24 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codelists", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="codelist",
            name="coding_system_id",
            field=models.CharField(
                choices=[
                    ("bnf", "Pseudo BNF"),
                    ("ctv3", "CTV3 (Read V3)"),
                    ("ctv3tpp", "CTV3 (Read V3) with TPP extensions"),
                    ("dmd", "Dictionary of Medicines and Devices"),
                    ("readv2", "Read V2"),
                    ("snomedct", "SNOMED CT"),
                ],
                max_length=32,
                verbose_name="Coding system",
            ),
        ),
    ]
