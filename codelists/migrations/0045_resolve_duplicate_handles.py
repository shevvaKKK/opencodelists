# Generated by Django 3.2.8 on 2021-10-26 09:44
#
# This migration fixes codelist handles where an owner (a user or organisation) has two
# handles with the same name or slug.  When an owner has two handles with the same name/slug,
# we add " 1"/"-1" to the name/slug of the handle that was created second.
#
# This will not break any existing URLs, because any URLs that look up an affected
# codelist will return a 500, because it does a .get(), which returns multiple results.
#
# The next migration will enforce this properly at the database level.

from django.db import migrations
from django.db.models import Count


def resolve_duplicate_handles(apps, schema_editor):
    Handle = apps.get_model("codelists", "Handle")

    for record in (
        Handle.objects.filter(organisation__isnull=True)
        .values("user_id", "slug")
        .annotate(n=Count("id"))
        .filter(n__gt=1)
    ):
        handles = Handle.objects.filter(
            user_id=record["user_id"], slug=record["slug"]
        ).order_by("created_at")
        update_slugs(handles)

    for record in (
        Handle.objects.filter(user__isnull=True)
        .values("organisation_id", "slug")
        .annotate(n=Count("id"))
        .filter(n__gt=1)
    ):
        handles = Handle.objects.filter(
            organisation_id=record["organisation_id"], slug=record["slug"]
        ).order_by("created_at")
        update_slugs(handles)

    for record in (
        Handle.objects.filter(organisation__isnull=True)
        .values("user_id", "name")
        .annotate(n=Count("id"))
        .filter(n__gt=1)
    ):
        handles = Handle.objects.filter(
            user_id=record["user_id"], name=record["name"]
        ).order_by("created_at")
        update_names(handles)

    for record in (
        Handle.objects.filter(user__isnull=True)
        .values("organisation_id", "name")
        .annotate(n=Count("id"))
        .filter(n__gt=1)
    ):
        handles = Handle.objects.filter(
            organisation_id=record["organisation_id"], name=record["name"]
        ).order_by("created_at")
        update_names(handles)


def update_slugs(handles):
    for ix, h in enumerate(handles):
        if ix == 0:
            continue
        new_slug = f"{h.slug}-{ix}"
        print(f"Updating slug '{h.slug}' to '{new_slug}'")
        h.slug = new_slug
        h.save()


def update_names(handles):
    for ix, h in enumerate(handles):
        if ix == 0:
            continue
        new_name = f"{h.name} {ix}"
        print(f"Updating name '{h.name}' to '{new_name}'")
        h.name = new_name
        h.save()


class Migration(migrations.Migration):

    dependencies = [
        ("codelists", "0044_auto_20210608_1515"),
    ]

    operations = [migrations.RunPython(resolve_duplicate_handles)]
