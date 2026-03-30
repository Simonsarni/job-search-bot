# Job Search Bot 🤖

A Python automation tool that searches for job listings, saves results to a CSV file, and sends a daily email digest with new opportunities.

## Features

- 🔍 Searches jobs via the Jooble API
- 💾 Saves results to a CSV file (no duplicates on repeated runs)
- 📧 Sends an HTML email with all listings found
- ⚙️ Fully configurable — change search query, location, and number of results

## Technologies

- Python 3
- `urllib` — API requests (no external libraries needed)
- `smtplib` + `email` — sending emails via Gmail
- `json` — parsing API responses
- `csv` — saving results locally
- `datetime` — timestamping results

## Setup

### 1. Get a free Jooble API key
Register at [jooble.org/api/about](https://jooble.org/api/about) and get your free API key.

### 2. Set up Gmail App Password
Since Gmail requires app-specific passwords for scripts:
1. Go to your Google Account → Security
2. Enable 2-Step Verification
3. Go to App Passwords → Generate a password for "Mail"
4. Copy that 16-character password

### 3. Configure the bot
Open `job_search_bot.py` and edit the configuration section:

```python
MY_EMAIL = "your_email@gmail.com"
MY_APP_PASSWORD = "your_16_char_app_password"
API_KEY = "your_jooble_api_key"

SEARCH_QUERY = "software engineer intern"
SEARCH_LOCATION = "remote"
MAX_RESULTS = 10
```

### 4. Run the bot

```bash
python job_search_bot.py
```

## How to Run it Daily (Optional)

### On Mac/Linux — using cron:
```bash
# Open crontab
crontab -e

# Add this line to run every day at 8am
0 8 * * * python /path/to/job_search_bot.py
```

### On Windows — using Task Scheduler:
1. Open Task Scheduler
2. Create a Basic Task
3. Set trigger: Daily at 8:00 AM
4. Set action: Start `python job_search_bot.py`

## Output Example

**Console:**
```
==================================================
🤖 JOB SEARCH BOT — Starting...
==================================================
🔍 Searching 'software engineer intern' in 'remote'...
✅ Found 10 listings.
💾 Results saved to 'jobs_found.csv'.
📧 Email sent successfully.
==================================================
✅ Bot finished.
==================================================
```

**Email:** Formatted HTML digest with job title, company, location, salary, and direct link to apply.

**CSV file:** Saves all results with columns: title, company, location, salary, date, link.

## What I Learned

- Making HTTP requests and consuming REST APIs with Python's `urllib`
- Parsing and handling JSON data
- Automating email sending with `smtplib` and MIME formatting
- Writing and appending data to CSV files
- Structuring a multi-function Python project with clean modular design
