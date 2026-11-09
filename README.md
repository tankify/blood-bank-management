# LifeLink — Django Blood Bank Demo

A refreshed Django app based on the Blood Bank Management System. It retains Django, server-rendered templates, URL routing, Django authentication, models, and the admin interface.

## Important demo limitations

The project uses SQLite shared-cache memory storage in a single local server process. It is volatile: restarting the server clears demo accounts and submissions. A separate process or serverless instance has a separate database. This is not suitable for reliable shared hosting or real donor data. All preloaded contacts and locations are fictional, contact details are hidden, and forms clearly warn users not to enter real information.

## Run locally

Requires Python 3.12. Create and activate a virtual environment, then install dependencies:

    python -m pip install -r requirements.txt

Start the server with:

    python manage.py run_demo

Open http://127.0.0.1:8000. The custom command applies migrations, seeds sample records, and runs Django in single-threaded mode in the same process so the memory database remains available between local requests.

## Test suite

The project includes Django tests for dashboard rendering, blood-group/city filters, account-gated submissions, and form validation. Run them later with:

    python manage.py test

The test runner creates its own temporary in-memory test database. Do not use the sample app for real medical coordination or personal contact information.
