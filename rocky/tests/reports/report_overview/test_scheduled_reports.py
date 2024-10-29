from django.urls import resolve, reverse
from pytest_django.asserts import assertContains
from reports.views.report_overview import ScheduledReportsView

from octopoes.models.tree import ReferenceTree
from tests.conftest import setup_request

TREE_DATA = {
    "root": {"reference": "ReportRecipe|31c79490-fb51-440d-9108-0c388276f655", "children": {}},
    "store": {
        "ReportRecipe|31c79490-fb51-440d-9108-0c388276f655": {
            "object_type": "ReportRecipe",
            "scan_profile": {
                "scan_profile_type": "empty",
                "reference": "ReportRecipe|31c79490-fb51-440d-9108-0c388276f655",
                "level": 0,
                "user_id": 1,
            },
            "user_id": 1,
            "primary_key": "ReportRecipe|31c79490-fb51-440d-9108-0c388276f655",
            "recipe_id": "31c79490-fb51-440d-9108-0c388276f655",
            "report_name_format": "Scheduled report ${report_type} for ${oois_count} objects",
            "subreport_name_format": "${report_type} for ${ooi}",
            "input_recipe": {"input_oois": ["Hostname|internet|mispo.es"]},
            "parent_report_type": "concatenated-report",
            "report_types": ["dns-report", "findings-report", "ipv6-report", "mail-report"],
            "cron_expression": "0 0 * * *",
        }
    },
}


def test_scheduled_reports_without_generated_reports(
    rf, client_member, mock_organization_view_octopoes, mocker, mock_scheduler, get_report_schedules
):
    """
    Test if the scheduled reports are shown in the table with the correct data.
    Should contain:

    - Table column data
    - "Edit report recipe" button
    """

    mocker.patch("reports.views.base.get_katalogus")
    mocker.patch("katalogus.client.KATalogusClientV1")
    mocker.patch("katalogus.client.httpx")
    mocker.patch("katalogus.utils.get_katalogus")
    mocker.patch("reports.views.base.get_katalogus")

    kwargs = {"organization_code": client_member.organization.code}
    url = reverse("scheduled_reports", kwargs=kwargs)

    request = rf.get(url)
    request.resolver_match = resolve(url)

    setup_request(request, client_member.user)

    # Mock ReportRecipe
    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.model_validate(TREE_DATA)
    # Mock ReportSchedule
    mock_organization_view_octopoes().list_objects.return_value = get_report_schedules

    response = ScheduledReportsView.as_view()(request, organization_code=client_member.organization.code)

    assert response.status_code == 200
    response.render()
    print(response.content)
    assertContains(response, "Report Name")
    assertContains(response, "Report types")
    assertContains(response, "Scheduled for")
    assertContains(response, "Recurrence")
    assertContains(response, "Open details")


def test_scheduled_reports_with_generated_reports(
    rf, client_member, mock_organization_view_octopoes, mocker, mock_scheduler, get_report_schedules
):
    """
    Test if the scheduled reports are shown in the table with the correct data.
    Should contain:

    - Table column data
    - Generated reports when row is expanded
    - "Edit report recipe" button
    """

    mocker.patch("reports.views.base.get_katalogus")
    kwargs = {"organization_code": client_member.organization.code}
    url = reverse("scheduled_reports", kwargs=kwargs)

    request = rf.get(url)
    request.resolver_match = resolve(url)

    setup_request(request, client_member.user)

    # Mock ReportRecipe
    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.model_validate(TREE_DATA)
    # Mock ReportSchedule
    mock_organization_view_octopoes().list_objects.return_value = get_report_schedules

    response = ScheduledReportsView.as_view()(request, organization_code=client_member.organization.code)

    assert response.status_code == 200
    assertContains(response, "Report Name")
    assertContains(response, "Report types")
    assertContains(response, "Scheduled for")
    assertContains(response, "Recurrence")
    assertContains(response, "Open details")
