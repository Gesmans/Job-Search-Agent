import anthropic
import os
from dotenv import load_dotenv
import requests 
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta



os.makedirs('cover_letters', exist_ok=True)  # Create a directory to store cover letters if it doesn't exist
os.makedirs('job_opportunities', exist_ok=True)  # Create a directory to store job opportunities if it doesn't exist

load_dotenv()  # Load environment variables from .env file

messages = []

# This is your connection to Claude
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def save_results(content):
        with open('job_opportunities/job_opportunities.txt', 'w') as file:
            file.write(content)

def save_cover_letter(content, job_name):
        with open(f'cover_letters/{job_name}_cover_letter.txt', 'w') as file:
            file.write(content)

def save_summarise_cv(cv_summary):
        with open('cv_summary.txt', 'w') as file:
            file.write(cv_summary)

def is_recent(date_string, days=3):
    try:
        posted = datetime.fromisoformat(date_string[:10]) 
        return datetime.now() - posted <= timedelta(days=days)
    except:
        return None  # unknown date

def get_page_date(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try common date meta tags
    for tag in ['article:published_time', 'date', 'pubdate']:
        meta = soup.find('meta', property=tag) or soup.find('meta', attrs={'name': tag})
        if meta:
            return meta.get('content', '')
    
    # Try time element
    time_tag = soup.find('time')
    if time_tag:
        return time_tag.get('datetime', '')
    
    return None

def is_search_page(url):
    search_patterns = [
        '/jobs/search',
        '/jobs?',
        'q-',
        'SRCH_',
        '/job-search',
        'search?',
        '/jobs/results',
        '/in-central-london'
    ]
    return any(pattern in url for pattern in search_patterns)
    

def job_score(jobs, cv_summary):
    response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system=f"You are a job scoring assistant. Score each job from 1-10 based on how well it matches the CV. Format your response as: Job Title — Company Score: X/10 Reason: one sentence why ---",
    messages=[{"role": "user", "content": f"Here is the CV content: {cv_summary} Here are the job opportunities: {jobs} Score each job based on how well it matches the CV."}]
    )
    
    reply = ""
    for block in response.content: 
        if block.type == "text":
            reply += block.text  
    return reply


def AIAgent():
    system_prompt = f"You are a Job search agent. Your task is to analyze the provided CV and generate a list of potential job opportunities that match the skills and experience outlined. You should extract skills from the CV. Only find mid level roles. Provide a list of the top 5 job opportunities with a brief description and a For each job found, provide the direct URL to that specific job posting, not a search results page or job board homepage. If you cannot find any relevant job opportunities, please respond with 'No relevant job opportunities found.' If the Job says the vacancy is closed or has expired, please remove it from the list. Always provide the most up-to-date information. If no link is available, please provide the company name and job title instead. If you are not 100% certain a job is still actFormat each job as: Job Title: .., Company: ..., Requirements: ..., URL: https://... URLs must link directly to a single job posting page. Never include job board search pages or listing pages."
    with open('cv_summary.txt', 'r') as file:
            cv_summary = file.read()
        
    '''if os.path.exists("job_opportunities/job_opportunities.txt"):
            print("Found saved job results. Use these? (yes/no)")
            use_saved = input().strip().lower()
            if use_saved == "yes":
                with open("job_opportunities/job_opportunities.txt", "r") as f:
                    reply = f.read()
                    print(f"Loaded saved jobs:\n{reply}")

                    job_list = reply.split("---")
                    print("\nWould you like to generate cover letters for all jobs found?")
                    choice = input("yes/no: ").strip().lower()
                    if choice == "yes":
                        for job in job_list:
                            if "URL:" in job:
                                url_match = re.search(r'\*{0,2}URL:\*{0,2}\s*(https?://\S+)', job)
                                
                                if url_match:
                                    job_url = url_match.group(1)
                                    if is_search_page(job_url):
                                        print(f"Skipping — search results page, not a specific job")
                                        continue
                                    page_date = get_page_date(job_url)
                                    if page_date and not is_recent(page_date):
                                        print(f"Skipping — posted {page_date}, too old")
                                        continue
                                    job_description = fetch_job_page(job_url)[:3000]
                                    if not is_job_active(job_description):
                                        print("Skipping — position no longer active")
                                        continue
                                    job_title = extract_job_title(job_description)
                                    generate_cover_letter(job_description, cv_summary, job_title)
                            else:
                                print(f"No URL found for job: {job}. Skipping cover letter generation.")
                        
                        return'''


    while True:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    print("Exiting the Job Search Agent. Goodbye!")
                    mainMenu()
                    break

                if len(messages) == 0:
                    content = f"Here is my CV summary:\n{cv_summary}\n\n{user_input}"
                else:
                    content = user_input
        
                messages.append({"role": "user", "content": content})

                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    system=system_prompt,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=messages[-6:]
                )

                reply = ""
                for block in response.content:
                    if block.type == "text":
                        reply += block.text 

                print(f"Claude: {reply}")
                save_results(reply)
                # scores = job_score(reply[:1000], cv_summary)
                # print(f"Job Scores: {scores}")
                # save_results(f"{reply}\n\nJob Scores:\n{scores}")
                job_list = reply.split("---")
                print("\nWould you like to generate cover letters for all jobs found?")
                choice = input("yes/no: ").strip().lower()
                if choice == "yes":
                    for job in job_list:
                        if "URL:" in job:
                            url_match = re.search(r'\*{0,2}URL:\*{0,2}\s*(https?://\S+)', job)
                            
                            if url_match:
                                job_url = url_match.group(1)
                                if is_search_page(job_url):
                                    print(f"Skipping — search results page, not a specific job")
                                    continue
                                page_date = get_page_date(job_url)
                                if page_date and not is_recent(page_date):
                                    print(f"Skipping — posted {page_date}, too old")
                                    continue
                                job_description = fetch_job_page(job_url)[:3000]
                                if not is_job_active(job_description):
                                    print("Skipping — position no longer active")
                                    continue
                                job_title = extract_job_title(job_description)
                                generate_cover_letter(job_description, cv_summary, job_title)
                        else:
                            print(f"No URL found for job: {job}. Skipping cover letter generation.")

                messages.append({"role": "assistant", "content": reply})

def summarise_cv(cv_content):
    if os.path.exists("cv_summary.txt"):
        with open("cv_summary.txt", "r") as f:
            return f.read()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": f"Summarise this CV in under 200 words, keeping only job titles, skills, and years of experience: {cv_content}"}]
    )
    reply = ""
    for block in response.content:
        if block.type == "text":
            reply += block.text
    save_summarise_cv(reply)
    return reply
    
    

def fetch_job_page(job_url):
        responce = requests.get(job_url)
        if responce.status_code == 200: 
            soup = BeautifulSoup(responce.content, 'html.parser')
            return soup.get_text()[:2000]
        else:
            print(f"Failed to fetch the page. Status code: {responce.status_code}")
            return ""
        
def generate_cover_letter(job_description, cv_summary, job_title):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="You are a cover letter generator. Generate a personalized cover letter based on the job description and CV. Keep it concise, direct, and below 100 words.",
        messages=[{"role": "user", "content": f"Job description: {job_description}\n\nCV: {cv_summary}\n\nGenerate a tailored cover letter."}]
    )
    letter = ""
    for block in response.content:
        if block.type == "text":
            letter += block.text
    save_cover_letter(letter, job_title)
    return letter

def extract_job_title(job_description):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{"role": "user", "content": f"Extract only the job title from this text. Return just the title, nothing else: {job_description[:2000]}"}]
    )
    title = ""
    for block in response.content:
        if block.type == "text":
            title += block.text
    return title.strip()

def extract_urls(text):
    pattern = r'https?://[^\s\)]+'
    return re.findall(pattern, text)      

def is_job_active(job_description):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,
        messages=[{"role": "user", "content": f"Is this job still active based on the description? {job_description[:2000]} Answer yes or no."}]
    )
    reply = ""
    for block in response.content:
        if block.type == "text":
            reply += block.text
    return reply.strip().lower() == "yes"

def mainMenu():
        with open('cv.txt', 'r') as file:
            cv_content = file.read()
            summarise_cv(cv_content)
        while True:
            print("Main Menu:")
            print("1. Analyze CV and find job opportunities")
            print("2. Create Cover Letter for a specific job")
            print("3. Exit")
            choice = input("Enter your choice (1, 2, or 3): ").strip()

            if choice == "1":
                AIAgent()
            elif choice == "2":
                job_title = input("Enter the Company you want to apply to: ")
                job_url = input("Paste the job URL: ")
                job_description = fetch_job_page(job_url)
                letter = generate_cover_letter(job_description, cv_content, job_title)
            elif choice == "3":
                print("Exiting the Job Search Agent. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    mainMenu()

