# KONFERENCA Project Documentation

## Overview
KONFERENCA is a Django-based web application designed to manage conference attendees, arrivals, and user accounts. It includes REST API endpoints, Celery task scheduling, and email notifications for daily attendee reports.

## Features
- User authentication and custom user model
- Attendee management (add, edit, list, change log)
- Arrival tracking
- REST API for attendees
- Scheduled daily email reports using Celery
- Admin interface for all models

## Project Structure
- `accounts/` – Custom user model and authentication
- `attendees/` – Attendee models, forms, views, serializers, Celery tasks
- `arrivals/` – Arrival models, views, serializers
- `konferenca/` – Project settings, Celery configuration, URLs, templates, static files
- `manage.py` – Django management script
- `db.sqlite3` – SQLite database
- `data.json` – Example data file

## Celery Integration
- Celery is configured in `konferenca/celery.py` and uses Redis as the broker and result backend.
- A scheduled task (`attendees.tasks.daily_new_attendees_report`) sends a daily email report of new attendees to `admin@example.com`.

## Email Configuration
- Email backend is set up in `konferenca/settings.py` (update with your SMTP credentials).

## How to Run
1. Install dependencies from `dependencies.txt`.
2. Set up and run Redis server for Celery.
3. Start Django server:
   ```
   python manage.py runserver
   ```
4. Start Celery worker:
   ```
   celery -A konferenca worker --loglevel=info
   ```
5. (Optional) Start Celery beat for scheduled tasks:
   ```
   celery -A konferenca beat --loglevel=info
   ```

## API Endpoints
- `/api/attendees/` – List all attendees (GET)

## Templates
- HTML templates are in `konferenca/templates/` for attendee and arrival management, authentication, and base layout.

## Static Files
- CSS styles are in `konferenca/static/styles.css`

## License
Specify your license here.

## Author
Add your name and contact information here.
