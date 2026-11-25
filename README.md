# My Notes Web Application

A lightweight, responsive web app built with Flask (Python) where users can securely register, log in, and manage their personal notes.

## Features

- Sign up and login with hashed passwords
- Session-based login with an optional "Remember me"
- CSRF protection on every form and on note deletion
- Flash messages for success and error feedback
- Create, read, and delete your own notes (newest first, with timestamps)
- Mobile-friendly layout

## Tech Stack

- Backend: Python, Flask, Flask-Login, Flask-WTF
- Database: SQLite (Flask-SQLAlchemy)
- Frontend: HTML5, CSS3, vanilla JavaScript

## Local Setup

```bash
# 1. (Recommended) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python main.py
```

Then open http://127.0.0.1:5000

## Configuration

| Variable      | What it does                                                                                              |
| ------------- | --------------------------------------------------------------------------------------------------------- |
| `SECRET_KEY`  | Signs login sessions. If not set, a random key is created once in `instance/secret_key`.                  |
| `FLASK_DEBUG` | `1` (default) enables debug mode for local development. Set to `0` anywhere other than your own computer. |

## Project Structure

```
main.py                 entry point
website/
  __init__.py           app factory (config, extensions, database)
  models.py             User and Note tables
  auth.py               login, logout, sign up
  views.py              home page, add and delete notes
  templates/            HTML pages
  static/               CSS and JavaScript
instance/               created automatically: database and secret key (not committed)
```
