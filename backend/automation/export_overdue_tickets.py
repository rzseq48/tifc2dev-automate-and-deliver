import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "tickets.json"
REPORT_FILE = BASE_DIR / "reports" / "overdue_high_priority.json"
DEFAULT_THRESHOLD_DAYS = 14
TERMINAL_STATUSES = {"Resolved", "Closed"}


def _parse(value):
    return datetime.fromisoformat(value)


def build_report(tickets, threshold_days, as_of):
    included = []

    for ticket in tickets:
        created_at = _parse(ticket["created_at"])
        age_days = (as_of - created_at).days

        is_overdue = age_days > threshold_days
        is_high_priority = ticket["priority"] == "High"
        is_open = ticket["status"] not in TERMINAL_STATUSES

        if is_overdue and is_high_priority and is_open:
            included.append(
                {
                    "id": ticket["id"],
                    "title": ticket["title"],
                    "priority": ticket["priority"],
                    "status": ticket["status"],
                    "created_at": ticket["created_at"],
                    "age_days": age_days,
                    "assigned_to": ticket.get("assigned_to"),
                }
            )

    return {
        "summary": {
            "tickets_processed": len(tickets),
            "tickets_included": len(included),
            "generated_at": as_of.isoformat(),
        },
        "tickets": included,
    }



def load_tickets(path=DATA_FILE):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def export_report(report, path=REPORT_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def main():
    tickets = load_tickets()
    as_of = datetime.now(timezone.utc)
    report = build_report(tickets, DEFAULT_THRESHOLD_DAYS, as_of)
    export_report(report)
    print(f"Tickets processed: {report['summary']['tickets_processed']}")
    print(f"Tickets included: {report['summary']['tickets_included']}")
    print(f"Report created: {REPORT_FILE}")


if __name__ == "__main__":
    main()
