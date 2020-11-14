from django.shortcuts import redirect, render

from coding_systems.snomedct.models import Concept as SnomedConcept

from ..coding_systems import CODING_SYSTEMS
from ..definition import Definition
from ..hierarchy import Hierarchy
from ..presenters import build_definition_rows
from .decorators import load_version


@load_version
def version(request, clv, expect_draft):
    if expect_draft != clv.is_draft:
        return redirect(clv)

    definition_rows = {}
    child_map = None
    code_to_status = None
    code_to_term = None
    parent_map = None
    tree_tables = None
    if clv.coding_system_id in ["ctv3", "ctv3tpp", "snomedct"]:
        if clv.coding_system_id in ["ctv3", "ctv3tpp"]:
            coding_system = CODING_SYSTEMS["ctv3"]
        else:
            coding_system = CODING_SYSTEMS["snomedct"]

        hierarchy = Hierarchy.from_codes(coding_system, clv.codes)
        parent_map = {p: list(cc) for p, cc in hierarchy.parent_map.items()}
        child_map = {c: list(pp) for c, pp in hierarchy.child_map.items()}
        code_to_term = coding_system.code_to_term(hierarchy.nodes)
        code_to_status = {
            code: "+" if code in clv.codes else "-" for code in hierarchy.nodes
        }
        ancestor_codes = hierarchy.filter_to_ultimate_ancestors(
            set(clv.codes) & hierarchy.nodes
        )
        tree_tables = sorted(
            (type.title(), sorted(codes, key=code_to_term.__getitem__))
            for type, codes in coding_system.codes_by_type(
                ancestor_codes, hierarchy
            ).items()
        )

        definition = Definition.from_codes(set(clv.codes), hierarchy)
        rows = build_definition_rows(coding_system, hierarchy, definition)

        if clv.coding_system_id == "snomedct":
            inactive_codes = SnomedConcept.objects.filter(
                id__in=clv.codes, active=False
            ).values_list("id", flat=True)
            definition_rows = {
                "active": [r for r in rows if r["code"] not in inactive_codes],
                "inactive": [r for r in rows if r["code"] in inactive_codes],
            }
        else:
            definition_rows = {"active": rows, "inactive": []}

    headers, *rows = clv.table

    ctx = {
        "clv": clv,
        "codelist": clv.codelist,
        "versions": clv.codelist.versions.order_by("-version_str"),
        "headers": headers,
        "rows": rows,
        "tree_tables": tree_tables,
        "parent_map": parent_map,
        "child_map": child_map,
        "code_to_term": code_to_term,
        "code_to_status": code_to_status,
        "definition_rows": definition_rows,
    }
    return render(request, "codelists/version.html", ctx)
