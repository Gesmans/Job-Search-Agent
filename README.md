# Job Search Agent
 
An AI-powered job search agent built with Python and the Anthropic Claude API. The agent reviews your CV, searches for relevant job opportunities, scores them against your profile, and generates tailored cover letters.

## Features
 
- **CV Analysis** — Summarises your CV and caches it locally to avoid repeated API calls
- **Live Job Search** — Searches the web for mid to senior-level roles posted in the last 3 days
- **Job Validation** — Filters out expired, closed, and search result pages automatically
- **Date Filtering** — Skips jobs older than 3 days using page metadata
- **Cover Letter Generation** — Generates tailored cover letters for each job found
- **Result Caching** — Saves job results locally so you can regenerate cover letters without repeating searches
- **Individual Cover Letters** — Each cover letter is saved separately, named after the job title

## Project Structure
 
```
AI-Agent-JobSearch/
│
├── agent.py                  # Main application
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
pip install anthropic python-dotenv requests beautifulsoup4
```
 
### 3. Add your API key
 
Create a `.env` file in the root directory:
 
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
 
Get your API key from [platform.anthropic.com](https://platform.anthropic.com)
 
### 4. Add your CV
 
Create a `cv.txt` file in the root directory and paste your CV content into it.
 
### 5. Run the agent
 
```bash
python3 agent.py
```
 
## Usage
 
### Main Menu
```
Main Menu:
1. Analyze CV and find job opportunities
2. Create Cover Letter for a specific job
3. Exit
```
 
### Option 1 — Analyze CV and find jobs
 
- If saved job results exist, you can reuse them without making a new API call
- The agent searches for mid to senior roles posted in the last 3 days
- Expired, closed, and irrelevant jobs are automatically filtered out
- You will be asked if you want to generate cover letters for all jobs found
- Cover letters are saved to the `cover_letters/` folder
### Option 2 — Create a cover letter for a specific job
 
- Paste a direct job URL
- Uses your full CV for a more personalised letter
- Saved to the `cover_letters/` folder
## How It Works
 
```
CV loaded from cv.txt
        ↓
CV summarised and cached in cv_summary.txt
        ↓
Agent searches web for matching jobs
        ↓
Each job URL is validated:
  - Is it a direct job page? (not a search results page)
  - Was it posted in the last 3 days?
  - Is the position still active?
        ↓
Cover letters generated and saved per job
```
 
## Cost
 
Uses the Anthropic Claude API on a pay-as-you-go basis:
 
| Action | Model Used |
|---|---|
| Job search | claude-haiku |
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
 
- [ ] Flask web interface
- [ ] Deploy to cloud (Railway / Render)
- [ ] Job scoring system
- [ ] Email integration
## Built With
 
- [Python 3](https://python.org)
- [Anthropic Claude API](https://anthropic.com)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
