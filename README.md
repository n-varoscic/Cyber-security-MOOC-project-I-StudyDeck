# StudyDeck - Intentionally Vulnerable Django Application

## Overview

StudyDeck is a simple Django web application designed for the Cyber Security Base MOOC at the University of Helsinki. It allows users to create and manage study decks with flashcards, organized by subjects. The application intentionally includes 5 real security vulnerabilities from the OWASP Top 10 2021 list to demonstrate common security flaws and their fixes.

---

### Core Features

- **User Management**: Registration, login, logout, and profile management
- **Subjects**: Create and manage study subjects
- **Decks**: Organize flashcards within subjects
- **Flashcards**: Add, edit, and delete flashcards with questions and answers
- **Profile Page**: User profile with bio and notes
- **Search Feature**: Search flashcards by question or answer

---

## Project Structure

```
StudyDeck/
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── db.sqlite3                  # SQLite database (created after migrate)
├── studydeck/                  # Main Django project
│   ├── __init__.py
│   ├── settings.py             # Django settings (contains FLAW 4)
│   ├── urls.py                 # Project URL routing
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── decks/                      # Main application
│   ├── __init__.py
│   ├── models.py               # Database models (contains FLAW 2)
│   ├── views.py                # Views (contains FLAW 1, 3, 5)
│   ├── forms.py                # Django forms
│   ├── urls.py                 # App URL routing
│   ├── admin.py                # Django admin configuration
│   ├── apps.py
│   ├── migrations/             # Database migrations
│   │   ├── __init__.py
│   │   ├── 0001_initial.py     # Creates initial schema (Deck, Subject, Profile, Flashcard models)
│   │   ├── 0002_alter_profile_sensitive_note.py  # Changes sensitive_note to BinaryField (flaw 2)
│   │   └── 0003_alter_profile_sensitive_note.py  # Reverts sensitive_note back to TextField (flaw 2)
│   └── templates/              # HTML templates
│       ├── base.html
│       ├── create_deck.html
│       ├── create_flashcard.html
│       ├── create_subject.html
│       ├── dashboard.html
│       ├── decks.html
│       ├── delete_flashcard.html
│       ├── edit_flashcard.html
│       ├── flashcards.html
│       ├── login.html
│       ├── profile.html
│       ├── register.html
│       ├── search.html
│       ├── study_deck.html
│       └── subjects.html
└── screenshots/                # Folder for vulnerability demonstrations
    ├── Flaw 1/
    ├── Flaw 2/
    ├── Flaw 3/
    ├── Flaw 4/
    └── Flaw 5/
```

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Git

### Step 1: Clone/Download the Project

```bash
cd /path/to/StudyDeck
```

### Step 2: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Database

```bash
python manage.py migrate
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

---

## Demo Users & Data

### Creating Demo Users

You can create demo users through the web interface or use existing user credentials to log in:

**User 1:**
- Username: `alice`
- Password: `redqueen`
- Email: `alice@gmail.com`

**User 2:**
- Username: `bob`
- Password: `squarepants`
- Email: `bob@gmail.com`

---

## 5 Intentional Vulnerabilities

This section describes the 5 intentional vulnerabilities and how to test them.

### FLAW 1: Broken Access Control (A01)

Users can access other users' decks by modifying the deck ID in the URL, bypassing authorization checks.

**Flaw 1**: No ownership validation in `view_deck()` function https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/views.py#L147

**Fix 1**: Check ownership with `get_object_or_404(Deck, id=deck_id, owner=request.user)` https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/views.py#L150

**Steps to test the flaw**:
1. Login as `alice` (password: `redqueen`)
2. Create a subject and deck, note the deck ID from the URL (e.g., `/decks/1/`)
3. Login as `bob` (password: `squarepants`)
4. Change the URL to Alice's deck ID: `http://localhost:8000/decks/1/`
5. **Result**: Bob can view Alice's private flashcards

**Steps to test the fix**:
1. Uncomment the fix 1 code
2. Restart the server
3. Repeat steps 1-4 above
4. **Result**: Bob receives a 404 error and cannot access Alice's deck

---

### FLAW 2: Cryptographic Failures (A02)

Sensitive user notes are stored in plaintext in the database without any encryption.

**Flaw 2**: `sensitive_note` field stores data unencrypted 
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/models.py#L16
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/forms.py#L19
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/forms.py#L48
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/forms.py#L61

**Fix 2**: Use `BinaryField` with encryption via Fernet 
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/models.py#L19
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/forms.py#L26
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/forms.py#L35
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/forms.py#L46
- https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/forms.py#L55

**Note on FERNET_KEY**: The encryption key is now loaded from the `FERNET_KEY` environment variable for security. For testing the fix, set this variable:

```bash
# macOS/Linux
export FERNET_KEY='YOUR_BASE64_ENCODED_KEY_HERE'

# Windows (PowerShell)
$env:FERNET_KEY='YOUR_BASE64_ENCODED_KEY_HERE'
```

You can generate a new key with: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key())"`

**Steps to test the flaw**:
1. Login and go to Profile page
2. Add a sensitive note (e.g., "Password: mypassword123")
3. Open database directly in the terminal: `sqlite3 db.sqlite3`
4. Query: `SELECT sensitive_note FROM decks_profile;`
5. **Result**: All sensitive notes visible in plaintext

**Steps to test the fix**:
1. Generate and set the FERNET_KEY environment variable (see note above)
2. Uncomment the fix 2 code
3. Create a new migration: `python manage.py makemigrations`
4. Apply migration: `python manage.py migrate`
5. Login and add a new sensitive note
6. Check the database in the terminal with `sqlite3 db.sqlite3` and query `SELECT sensitive_note FROM decks_profile;`
7. **Result**: Sensitive note is now stored as encrypted binary data

---

### FLAW 3: SQL Injection (A03)

Search functionality uses unsafe string concatenation with user input in raw SQL queries.

**Flaw 3**: Raw SQL with unsanitized user input https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/views.py#L262

**Fix 3**: Use Django ORM or parameterized queries https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/views.py#L273

**Steps to test the flaw**:
1. Go to Search page (`/search/`)
2. Enter in the search box: `' OR '1'='1`
3. Click Search
4. **Result**: All flashcards in database displayed (including other users' flashcards)

**Steps to test the fix**:
1. Uncomment the fix 3 code
2. Comment out the vulnerable code
3. Restart the server
4. Go to Search page and enter: `' OR '1'='1`
5. **Result**: No results returned or only the flascards that contain that phrase specifically.

---

### FLAW 4: Security Misconfiguration (A05)

Django settings expose sensitive information through debug mode and hard-coded secrets.

**Flaw 4**: `DEBUG=True`, `ALLOWED_HOSTS=['*']`, hardcoded `SECRET_KEY` https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/studydeck/settings.py#L15

**Fix 4**: Load configuration from environment variables using `.env` file https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/studydeck/settings.py#L20

**Steps to test the flaw**:
1. Go to a non-existent page: `http://localhost:8000/invalid/`
2. **Result**: Django debug page reveals entire project structure, settings, environment variables, and code
3. Check `settings.py` in repository: hardcoded `SECRET_KEY` is visible

**Steps to test the fix**:
1. Create a `.env` file in project root with secure values
2. Uncomment the fix 4. code
3. Comment out the vulnerable settings
4. Set environment variables: `export DEBUG=False`
5. Restart server and visit a non-existent page
6. **Result**: Generic error page without sensitive information

---

### FLAW 5: Security Logging and Monitoring Failures (A09)

Failed login attempts are not logged, making brute force attacks undetectable.

**Flaw 5**: No logging in `login_view()` for failed authentication attempts https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/views.py#L45

**Fix 5**: Log failed login attempts with `logger.warning()` https://github.com/n-varoscic/Cyber-security-MOOC-project-I-StudyDeck/blob/9292f6a52da02520764ef6507e6c722903221c17/decks/views.py#L51

**Steps to test the flaw**:
1. Go to login page
2. Try logging in with wrong credentials multiple times
3. Check `studydeck.log` file, `grep "Failed login" studydeck.log` or `grep -c "Failed login" studydeck.log`
4. **Result**: No failed login attempts are recorded in logs

**Steps to test the fix**:
1. Uncomment the fix 5 code
2. Restart the server
3. Go to login page and try wrong credentials multiple times
4. Check the logs: `tail -f studydeck.log`, `grep "Failed login" studydeck.log` or `grep -c "Failed login" studydeck.log`
5. **Result**: Failed login attempts are now recorded in logs with username and timestamp

---

## Troubleshooting

**Port 8000 already in use?**
```bash
python manage.py runserver 8001
```

**Database issues?**
```bash
rm db.sqlite3
python manage.py migrate
```

**Static files missing?**
```bash
python manage.py collectstatic
```

**Package installation fails?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Resources

1. OWASP Top 10, A01:2021 Broken Access Control (2021), https://owasp.org/Top10/A01_2021-Broken_Access_Control/ 
2. OWASP Top 10, A02:2021 Cryptographic Failures (2021), https://owasp.org/Top10/2021/A02_2021-Cryptographic_Failures/
3. OWASP Top 10, A03:2021 Injection (2021), https://owasp.org/Top10/2021/A03_2021-Injection/ 
4. OWASP Top 10, A05:2021 Security Misconfiguration (2021), https://owasp.org/Top10/2021/A05_2021-Security_Misconfiguration/
5. OWASP Top 10, A09:2021 Security Logging and Monitoring Failures (2021), https://owasp.org/Top10/2021/A09_2021-Security_Logging_and_Monitoring_Failures/
