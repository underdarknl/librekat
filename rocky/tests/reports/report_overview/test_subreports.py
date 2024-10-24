from django.urls import resolve, reverse
from pytest_django.asserts import assertContains
from reports.views.report_overview import ReportHistoryView, SubreportView

from octopoes.models.ooi.reports import Report
from octopoes.models.pagination import Paginated
from tests.conftest import setup_request


# Test if the subreports that belong to one parent are collected well enough
def test_report_subreports_table(
    rf, client_member, mock_organization_view_octopoes, mocker, report_list_six_subreports, get_subreports
):
    mocker.patch("reports.views.base.get_katalogus")
    kwargs = {"organization_code": client_member.organization.code}
    url = reverse("subreports", kwargs=kwargs)
    parent_report = report_list_six_subreports[0][0]

    request = rf.get(url, {"report_id": parent_report.primary_key})
    request.resolver_match = resolve(url)

    setup_request(request, client_member.user)

    mock_organization_view_octopoes().query_many.return_value = get_subreports

    response = SubreportView.as_view()(request, organization_code=client_member.organization.code)

    assert response.status_code == 200

    # Check header
    assertContains(
        response,
        f'<a href="/en/test/reports/view?report_id={parent_report}" title="Shows report details">{parent_report}</a>',
        html=True,
    )
    assertContains(response, "<h1>Subreports</h1>", html=True)
    assertContains(
        response,
        (
            '<a class="button ghost" href="/en/test/reports/report-history/">'
            '<span class="icon ti-chevron-left"></span>Back to Reports History</a>'
        ),
        html=True,
    )

    # Check table rows
    assertContains(
        response,
        '<a href="/en/test/objects/detail/?ooi_id=Hostname%7Cinternet%7Cexample.com">example.com</a>',
        html=True,
    )

    # Check subreports, show only 5
    total_subreports = str(len(report_list_six_subreports[0][1]))
    child_report_1 = report_list_six_subreports[0][1][0]
    child_report_2 = report_list_six_subreports[0][1][1]
    child_report_3 = report_list_six_subreports[0][1][2]
    child_report_4 = report_list_six_subreports[0][1][3]
    child_report_5 = report_list_six_subreports[0][1][4]
    child_report_6 = report_list_six_subreports[0][1][5]
    assertContains(response, f"Showing {total_subreports} of {total_subreports} subreports")
    assertContains(response, child_report_1)
    assertContains(response, child_report_2)
    assertContains(response, child_report_3)
    assertContains(response, child_report_4)
    assertContains(response, child_report_5)
    assertContains(response, child_report_6)

    # Check if all report types are shown
    assertContains(response, "RPKI Report")
    assertContains(response, "Safe Connections Report")
    assertContains(response, "System Report")
    assertContains(response, "Mail Report")
    assertContains(response, "IPv6 Report")
    assertContains(response, "Web System Report")


def test_report_history_report_type_summary(
    rf, client_member, mock_organization_view_octopoes, mocker, reports_more_input_oois
):
    mocker.patch("reports.views.base.get_katalogus")
    request = setup_request(rf.get("report_history"), client_member.user)

    mock_organization_view_octopoes().list_reports.return_value = Paginated[tuple[Report, list[Report | None]]](
        count=len(reports_more_input_oois), items=reports_more_input_oois
    )

    response = ReportHistoryView.as_view()(request, organization_code=client_member.organization.code)

    assert response.status_code == 200

    assertContains(response, "RPKI Report")
    assertContains(response, "Safe Connections Report")
    assertContains(response, "This report consist of 4 subreports with the following report types and objects.")
    assertContains(response, "<td>4</td>", html=True)
