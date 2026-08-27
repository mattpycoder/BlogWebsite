# BlogWebsite

A lightweight Flask blog platform where users can register, write, and share personal blogs.

## Features

- **User Authentication**: Register and login with secure password hashing (`Bcrypt`).
- **User Profiles**: View author details, stories, bookmarks, and account settings.
- **Clean Structure**: Blueprint-based routes, WTForms form validation, and SQLAlchemy database models.

---

## Installation & Setup

Make sure you have [uv](https://docs.astral.sh/uv/) installed.

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Setup pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

---

## Running the App

Start the development server:

```bash
uv run python run.py
```

Open [http://127.0.0.1:5001](http://127.0.0.1:5001) in your browser.

---

## Pre-commit & Code Quality

Run checks manually across all files:

```bash
uv run pre-commit run --all-files
```

Hooks configured in `.pre-commit-config.yaml`:
- `ruff format`: Code formatting
- `ruff check`: Linting
- `ty check`: Type checking