# TIFC2DEV-PY-DL-04: Automate, Test, and Deliver

Use the learner handouts to complete the automation, diagnose the GitHub Actions failure, open a pull request, and optionally deploy with Render.

## Local setup

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest
```

Expected starter result:

```text
1 passed, 7 failed
```

The health test passes. The seven automation tests fail with `NotImplementedError` until `build_report()` is completed.

## Run the automation

```bash
cd backend
python -m automation.export_overdue_tickets
```

The source data is in `backend/data/tickets.json`. The generated report is written to `backend/reports/overdue_high_priority.json`.

## GitHub Actions

The repository contains a workflow in `.github/workflows/helpdesk-tests.yml`. Follow the learner handout: predict the result before changing the workflow, then use the first failed check and its logs to diagnose the configuration.

## Optional Render deployment

Use these settings:

```text
Language: Python
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: gunicorn run:app
```

Verify:

- `/` returns the health response.
- `/api/tickets` returns HTTP 200 with a JSON list. An empty list is acceptable.
