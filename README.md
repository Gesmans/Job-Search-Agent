# Job Search Agent

An AI-powered job search agent built with Python, Streamlit, and the Anthropic Claude API. Upload your CV, search for live job opportunities, score them against your profile, and generate tailored cover letters — all from a web interface.

## Features

- **CV Upload** — Upload your CV as a PDF or TXT file via the web interface
- **CV Analysis** — Summarises your CV and caches it locally to avoid repeated API calls
- **Live Job Search** — Searches the web for mid to senior-level roles posted in the last 3 days
- **Job Scoring** — Scores each job 1-10 based on how well it matches your CV
- **Job Validation** — Filters out expired, closed, and search result pages automatically
- **Date Filtering** — Skips jobs older than 3 days using page metadata
- **Cover Letter Generation** — Generates tailored cover letters for each job found
- **Individual Cover Letters** — Download each cover letter separately, named after the job title
- **Result Caching** — Saves job results locally so you can regenerate cover letters without repeating searches
- **Web Interface** — Full Streamlit web app, no terminal needed

## Project Structure

```
AI-Agent-JobSearch/
│
├── app.py                    # Streamlit web interface
├── agent.py                  # AI agent logic and API calls
├── cv.txt                    # Your CV (not tracked in git)
├── cv_summary.txt            # Auto-generated CV summary (not tracked in git)
├── .env                      # API key (not tracked in git)
├── .gitignore
├── requirements.txt
│
├── cover_letters/            # Generated cover letters (not tracked in git)
│   └── Job_Title_cover_letter.txt
│
└── job_opportunities/        # Saved job search results (not tracked in git)
    └── job_opportunities.txt
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd AI-Agent-JobSearch
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install anthropic python-dotenv requests beautifulsoup4 streamlit pypdf2
```

### 3. Add your API key

Create a `.env` file in the root directory:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get your API key from [platform.anthropic.com](https://platform.anthropic.com)

### 4. Run the app

```bash
streamlit run app.py
```

## Usage

### Step 1 — Upload your CV
Upload a PDF or TXT version of your CV. It is saved locally so you only need to do this once.

### Tab 1 — Find Jobs
- Enter a search query (e.g. "Product Manager London")
- Click **Search Jobs** — the agent searches the web for live matching roles
- Click **Score these jobs** — each job is scored 1-10 against your CV
- Click **Generate Cover Letters** — tailored letters are created for each valid job
- Download each cover letter directly from the browser

### Tab 2 — Individual Cover Letter
- Paste a direct job URL
- Enter the job title
- Click **Generate Cover Letter**
- Uses your full CV for a more personalised letter
- Download directly from the browser

## How It Works

```
CV uploaded via Streamlit
        ↓
CV summarised and cached in cv_summary.txt
        ↓
Agent searches web for matching jobs (Claude + web search tool)
        ↓
Each job URL is validated:
  - Is it a direct job page? (not a search results page)
  - Was it posted in the last 3 days?
  - Is the position still active?
        ↓
Jobs scored 1-10 against CV summary
        ↓
Cover letters generated and saved per job
        ↓
Download buttons shown in browser
```

## Cost

Uses the Anthropic Claude API on a pay-as-you-go basis:

| Action | Model Used |
|---|---|
| Job search | claude-haiku |
| Job scoring | claude-haiku |
| Cover letter generation | claude-haiku |
| CV summarisation | claude-haiku |
| Job title extraction | claude-haiku |
| Active job check | claude-haiku |

Running a full search and generating cover letters costs approximately **$0.02–0.05 per run**.

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

## .gitignore

The following are excluded from version control:

```
.env
cv.txt
cv_summary.txt
cover_letters/
job_opportunities/
__pycache__/
*.pyc
```

## Roadmap

- [x] CV analysis and summarisation
- [x] Live job search via web
- [x] Job scoring system
- [x] Cover letter generation
- [x] Streamlit web interface
- [ ] Deploy to Streamlit Community Cloud
- [ ] Email integration
- [ ] Support for DOCX CV uploads

## Built With

- [Python 3](https://python.org)
- [Anthropic Claude API](https://anthropic.com)
- [Streamlit](https://streamlit.io)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- [PyPDF2](https://pypi.org/project/pypdf2/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)