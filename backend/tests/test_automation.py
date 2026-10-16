from copy import deepcopy
from datetime import datetime, timedelta, timezone

import pytest

from automation.export_overdue_tickets import build_report


@pytest.fixture()
def as_of():
    return datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)


def make_ticket(as_of, days_old, *, priority="High", status="New", assigned_to=None):
    created = as_of - timedelta(days=days_old, hours=1)
    return {
        "id": 99,
        "title": "Printer offline",
        "priority": priority,
        "status": status,
        "created_at": created.isoformat(),
        "assigned_to": assigned_to,
    }


def test_matching_ticket_is_included_with_required_fields_and_age(as_of):
    report = build_report([make_ticket(as_of, 20, assigned_to=None)], 14, as_of)

    assert report["summary"]["tickets_processed"] == 1
    assert report["summary"]["tickets_included"] == 1
    assert report["summary"]["generated_at"] == as_of.isoformat()
    assert len(report["tickets"]) == 1
    record = report["tickets"][0]
    assert set(record) == {
        "id",
        "title",
        "priority",
        "status",
        "created_at",
        "age_days",
        "assigned_to",
    }
    assert record["age_days"] == 20
    assert record["assigned_to"] is None


def test_in_progress_ticket_is_included(as_of):
    report = build_report([make_ticket(as_of, 20, status="In Progress")], 14, as_of)

    assert [ticket["id"] for ticket in report["tickets"]] == [99]


def test_recent_and_threshold_tickets_are_excluded(as_of):
    recent = make_ticket(as_of, 5)
    at_threshold = make_ticket(as_of, 14)

    report = build_report([recent, at_threshold], 14, as_of)

    assert report["tickets"] == []
    assert report["summary"]["tickets_processed"] == 2
    assert report["summary"]["tickets_included"] == 0


def test_resolved_and_closed_tickets_are_excluded(as_of):
    resolved = make_ticket(as_of, 30, status="Resolved")
    closed = make_ticket(as_of, 30, status="Closed")

    report = build_report([resolved, closed], 14, as_of)

    assert report["tickets"] == []


def test_other_priority_values_are_excluded(as_of):
    medium = make_ticket(as_of, 30, priority="Medium")
    low = make_ticket(as_of, 30, priority="Low")

    report = build_report([medium, low], 14, as_of)

    assert report["tickets"] == []


def test_no_matching_tickets_produces_valid_empty_report(as_of):
    report = build_report([], 14, as_of)

    assert report == {
        "summary": {
            "tickets_processed": 0,
            "tickets_included": 0,
            "generated_at": as_of.isoformat(),
        },
        "tickets": [],
    }


def test_source_ticket_data_is_not_modified(as_of):
    tickets = [make_ticket(as_of, 20)]
    original = deepcopy(tickets)

    build_report(tickets, 14, as_of)

    assert tickets == original
