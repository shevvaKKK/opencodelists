import pytest
from django.db.utils import IntegrityError

from codelists.models import CodelistVersion, Handle


def test_handle_cannot_belong_to_user_and_organisation(codelist, user, organisation):
    with pytest.raises(IntegrityError, match="codelists_handle_organisation_xor_user"):
        Handle.objects.create(
            codelist=codelist,
            name="Test",
            slug="test",
            is_current=True,
            user=user,
            organisation=organisation,
        )


def test_handle_must_belong_to_user_or_organisation(codelist):
    with pytest.raises(IntegrityError, match="codelists_handle_organisation_xor_user"):
        Handle.objects.create(
            codelist=codelist,
            name="Test",
            slug="test",
            is_current=True,
        )


def test_handle_slug_and_name_can_be_reused_by_different_organisation(
    codelist, another_organisation
):
    Handle.objects.create(
        codelist=codelist,
        name=codelist.name,
        slug=codelist.slug,
        is_current=True,
        organisation=another_organisation,
    )


def test_handle_slug_and_name_can_be_reused_by_different_user(codelist, user):
    Handle.objects.create(
        codelist=codelist,
        name=codelist.name,
        slug=codelist.slug,
        is_current=True,
        user=user,
    )


def test_handle_slug_cannot_be_reused_by_organisation(codelist):
    with pytest.raises(
        IntegrityError,
        match="UNIQUE constraint failed: codelists_handle.organisation_id, codelists_handle.slug",
    ):
        Handle.objects.create(
            codelist=codelist,
            name="New name",
            slug=codelist.slug,
            is_current=True,
            organisation=codelist.organisation,
        )


def test_handle_name_cannot_be_reused_by_organisation(codelist):
    with pytest.raises(
        IntegrityError,
        match="UNIQUE constraint failed: codelists_handle.organisation_id, codelists_handle.name",
    ):
        Handle.objects.create(
            codelist=codelist,
            name=codelist.name,
            slug="new-slug",
            is_current=True,
            organisation=codelist.organisation,
        )


def test_handle_slug_cannot_be_reused_by_user(user_codelist):
    with pytest.raises(
        IntegrityError,
        match="UNIQUE constraint failed: codelists_handle.user_id, codelists_handle.slug",
    ):
        Handle.objects.create(
            codelist=user_codelist,
            name="New name",
            slug=user_codelist.slug,
            is_current=True,
            user=user_codelist.user,
        )


def test_handle_name_cannot_be_reused_by_user(user_codelist):
    with pytest.raises(
        IntegrityError,
        match="UNIQUE constraint failed: codelists_handle.user_id, codelists_handle.name",
    ):
        Handle.objects.create(
            codelist=user_codelist,
            name=user_codelist.name,
            slug="new-slug",
            is_current=True,
            user=user_codelist.user,
        )


def test_old_style_codes(old_style_version):
    assert old_style_version.codes == (
        "128133004",
        "156659008",
        "202855006",
        "239964003",
        "35185008",
        "429554009",
        "439656005",
        "73583000",
    )


def test_old_style_table(old_style_version):
    assert old_style_version.table == [
        ["id", "name"],
        ["429554009", "Arthropathy of elbow (disorder)"],
        ["128133004", "Disorder of elbow (disorder)"],
        ["202855006", "Lateral epicondylitis (disorder)"],
        ["439656005", "Arthritis of elbow (disorder)"],
        ["73583000", "Epicondylitis (disorder)"],
        ["35185008", "Enthesopathy of elbow region (disorder)"],
        ["239964003", "Soft tissue lesion of elbow region (disorder)"],
        [
            "156659008",
            "(Epicondylitis &/or tennis elbow) or (golfers' elbow) (disorder)",
        ],
    ]


def test_old_style_codeset(old_style_version):
    assert old_style_version.codeset.codes() == set(old_style_version.codes)


def test_new_style_codes(version_with_some_searches):
    assert version_with_some_searches.codes == (
        "128133004",
        "156659008",
        "202855006",
        "239964003",
        "35185008",
        "429554009",
        "439656005",
        "73583000",
    )


def test_new_style_table(version_with_some_searches):
    assert version_with_some_searches.table == [
        ["code", "term"],
        ["128133004", "Disorder of elbow"],
        ["156659008", "(Epicondylitis &/or tennis elbow) or (golfers' elbow)"],
        ["202855006", "Lateral epicondylitis"],
        ["239964003", "Soft tissue lesion of elbow region"],
        ["35185008", "Enthesopathy of elbow region"],
        ["429554009", "Arthropathy of elbow"],
        ["439656005", "Arthritis of elbow"],
        ["73583000", "Epicondylitis"],
    ]


def test_new_style_codeset(version_with_some_searches):
    assert version_with_some_searches.codeset.codes() == set(
        version_with_some_searches.codes
    )


def test_old_style_is_new_style(old_style_codelist):
    assert not old_style_codelist.is_new_style()


def test_new_style_is_new_style(new_style_codelist):
    assert new_style_codelist.is_new_style()


def test_visible_versions_user_has_edit_permissions(
    new_style_codelist,
    user,
):
    assert len(new_style_codelist.visible_versions(user)) == 3


def test_visible_versions_user_doesnt_have_edit_permissions(
    new_style_codelist,
    user_without_organisation,
):
    assert len(new_style_codelist.visible_versions(user_without_organisation)) == 1


def test_latest_visible_version_user_has_edit_permissions(
    new_style_codelist,
    new_style_codelist_latest_version,
    user,
):
    assert (
        new_style_codelist.latest_visible_version(user)
        == new_style_codelist_latest_version
    )


def test_latest_visible_version_user_doesnt_have_edit_permissions(
    new_style_codelist,
    new_style_codelist_latest_published_version,
    user_without_organisation,
):
    assert (
        new_style_codelist.latest_visible_version(user_without_organisation)
        == new_style_codelist_latest_published_version
    )


def test_latest_visible_version_no_versions_visible(
    codelist_from_scratch, user_without_organisation
):
    assert (
        codelist_from_scratch.latest_visible_version(user_without_organisation) is None
    )


def test_get_by_hash(new_style_version):
    assert (
        CodelistVersion.objects.get_by_hash(new_style_version.hash) == new_style_version
    )
