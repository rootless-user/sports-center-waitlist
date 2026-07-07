# Sports Center Waitlist

A simple Flask + SQLite web application for managing client waitlist requests in a sports center.

Built to solve a real workflow problem: administrators need a structured way to store client requests, preferences, trainer choices, comments, and current status.

---

## Features

- Add new clients to the waitlist
- Store contact information and social media links
- Track preferred days and time
- Save trainer preferences
- Update client status
- Add comments for each request
- Search and view waitlist records
- Local SQLite database
- Simple browser-based interface

---

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Git / GitHub

---

## Project Structure

```text
sports-center-waitlist/
├── app.py
├── schema.sql
├── requirements.txt
├── start_waitlist.bat
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── clients.html
│   ├── add_client.html
│   └── search_clients.html
└── README.md
