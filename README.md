# Job Application Tracker

A command-line tool to track job applications, statuses, and follow-ups. Built with Python and SQLite.

## Features

- Add, list, update, and delete job applications
- Filter the list by status: `wishlist`, `applied`, `interview`, `offer`, `rejected`
- Follow-up reminders for applications that need attention
- Export all applications to CSV
- Automated tests with pytest

## Requirements

- Python 3.10 or newer
- No third-party packages needed to run the app (pytest is only needed for the tests)

## Setup

```
git clone https://github.com/Souvik-005/job-application-tracker.git
cd job-application-tracker
python -m venv .venv
.venv\Scripts\activate        # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run all commands from the project root.

```
python -m src.tracker add "Google" "Python Developer"
python -m src.tracker add "Amazon" "Backend Engineer" --url "https://amazon.com/job" --notes "Referred by a friend" --follow-up 2026-12-01
python -m src.tracker list
python -m src.tracker list --status interview
python -m src.tracker status 1 interview
python -m src.tracker due
python -m src.tracker export applications.csv
python -m src.tracker delete 1
```

| Command | What it does |
|---|---|
| `add <company> <title>` | Adds an application. Optional: `--url`, `--notes`, `--follow-up YYYY-MM-DD` |
| `list` | Lists all applications. Optional: `--status <status>` |
| `status <id> <new_status>` | Changes the status of an application |
| `due` | Shows in-progress applications whose follow-up date is today or earlier |
| `export <path>` | Exports all applications to a CSV file |
| `delete <id>` | Deletes an application |

Your data is stored in a local SQLite file (`applications.db`), which is ignored by Git so personal job data is never pushed.

## Demo

```
$ python -m src.tracker add "Google" "Python Developer" --follow-up 2026-11-01
Added application #1

$ python -m src.tracker add "Amazon" "Backend Engineer"
Added application #2

$ python -m src.tracker status 2 interview
Updated application #2 to interview

$ python -m src.tracker list
#1  Google - Python Developer  [applied]
#2  Amazon - Backend Engineer  [interview]

$ python -m src.tracker list --status interview
#2  Amazon - Backend Engineer  [interview]

$ python -m src.tracker due
#1  Google - Python Developer  (follow up: 2026-11-01)

$ python -m src.tracker export applications.csv
Exported 2 applications to applications.csv
```

## Running tests

```
python -m pytest -v
```

The tests use a temporary database for each test, so they never touch your real data.

## Project structure

```
job-application-tracker/
├── src/
│   └── tracker/
│       ├── __init__.py
│       ├── __main__.py    # Entry point for `python -m src.tracker`
│       ├── models.py      # Status enum and Application dataclass
│       ├── database.py    # SQLite storage, queries, and CSV export
│       └── cli.py         # Command-line interface (argparse)
├── tests/
│   ├── __init__.py
│   └── test_database.py   # pytest tests for the database layer
├── requirements.txt
├── LICENSE
└── README.md
```

## Design notes

- **Separation of concerns:** the CLI contains no SQL. It only calls functions from `database.py`.
- **Parameterized queries:** all SQL uses `?` placeholders instead of string formatting, which prevents SQL injection and handles names like `O'Reilly`.
- **Enum for status:** allowed statuses are defined once in `Status`, so typos can't reach the database.
- **Testable by design:** every database function accepts a `db_path`, so tests run against temporary databases.

## How this was built

Claude guided the design and reviewed my code. I typed, ran, and tested every part, and can explain each of them.

## What I learned

I learned how to build a small app in layers: models for the data, a database layer for SQLite, and a command-line interface that contains no SQL. I learned to use parameterized queries to prevent SQL injection, and to write pytest tests that run against temporary databases so my real data is never touched. A bug where changing an argument order broke an existing test taught me to use keyword arguments and to run the tests after every change.

## Future ideas

- An `edit` command for fields other than status
- Date validation for `--follow-up`
- A Flask web interface

## License

MIT
