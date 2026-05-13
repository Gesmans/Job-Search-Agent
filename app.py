import os

import streamlit as st
from agent import get_page_date, is_job_active, is_recent, is_search_page, summarise_cv, AIAgent, generate_cover_letter, fetch_job_page, extract_job_title
import re

def upload_CV():
    # Step 1: Upload CV
    st.header("Step 1: Upload Your CV")
    cv_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])
    return cv_file

def select_tasks(cv_file):
    # Step 2: Select Task
    st.header("Step 2: Select Task")
    tab1, tab2 = st.tabs(["Search Jobs", "Generate Cover Letter"])

    with tab1:
        # Check for saved job opportunities
        if os.path.exists("job_opportunities/job_opportunities.txt"):
            use_saved = st.checkbox("Use previously saved job opportunities", key="use_saved_jobs")
            # If the user chooses to use saved job opportunities, load and display them
            if use_saved:
                with open("job_opportunities/job_opportunities.txt", "r") as f:
                    saved_jobs = f.read()
                st.success("Loaded saved job opportunities")
                expand = st.expander("Saved Job Opportunities", icon=":material/info:")
                with expand:
                    st.write(saved_jobs)
                if st.button("Create Cover Letters for Saved Jobs", key="create_cover_letters_saved_jobs"):
                    with st.spinner("Generating cover letters for saved jobs..."):
                        job_lines = saved_jobs.splitlines() 
                        for job_line in job_lines:
                            if "URL:" in job_line:  # Check if the line contains a URL
                                url_match = re.search(r'\*{0,2}URL:\*{0,2}\s*(https?://\S+)', job_line)
                                if url_match:
                                    job_url = url_match.group(1)
                                    if is_search_page(job_url):
                                        st.warning(f"URL {job_url} appears to be a search results page. Skipping cover letter generation for this job.")
                                        continue
                                    page_date = get_page_date(job_url)
                                    if page_date and not is_recent(page_date):
                                        st.warning(f"Job posting at {job_url} is not recent. Skipping.")
                                        continue
                                    job_description = fetch_job_page(job_url)[:3000]
                                    if not is_job_active(job_description):
                                        st.warning(f"Job posting at {job_url} does not appear to be active. Skipping.")
                                        continue
                                    job_title = extract_job_title(job_line)
                                cover_letter = generate_cover_letter(cv_file, job_line, job_title)
                                st.subheader(f"Generated Cover Letter for {job_title}")
                                st.write(cover_letter)
                                st.download_button(f"Download Cover Letter for {job_title}", cover_letter, file_name=f"{job_title}_Cover-Letter.txt")   
                else:
                    st.info("Click the button to generate cover letters for the saved job opportunities.")
            # If the user does not choose to use saved job opportunities, proceed with search
            else:
                search_query = st.text_input("Enter your job search query (e.g., 'Software Engineer in London')", key="search_query_no_saved")
                if st.button("Search Jobs", key="search_jobs_no_saved"):
                    with st.spinner("Searching for jobs..."):
                        agent = AIAgent()
                        job_listings = agent.search_jobs(search_query)
                        st.subheader("Job Listings")
                        for job in job_listings:
                            st.write(f"**{job['title']}** at {job['company']} - {job['location']}")
                            st.write(f"[View Job Posting]({job['url']})")
                       
        else:
            # No saved job opportunities, proceed with search
            st.header("Search for Jobs", key="search_jobs_header")
            search_query = st.text_input("Enter your job search query (e.g., 'Software Engineer in London')", key="search_query")
            if st.button("Search Jobs", key="search_jobs"):
                if search_query:
                    agent = AIAgent()
                    job_listings = agent.search_jobs(search_query)
                    st.subheader("Job Listings")
                    for job in job_listings:
                        st.write(f"**{job['title']}** at {job['company']} - {job['location']}")
                        st.write(f"[View Job Posting]({job['url']})")
                else:
                    st.error("Please enter a search query.")

    with tab2:
        st.header("Generate Cover Letter")
        job_title = st.text_input("Enter the Job Title you are applying for")
        job_url = st.text_input("Paste the Job Link here")
        if st.button("Generate Cover Letter", key="generate_cover_letter"):
            if job_url and job_title:
                job_page = fetch_job_page(job_url) 
                cover_letter = generate_cover_letter(cv_file, job_page, job_title)
                st.subheader("Generated Cover Letter") 
                st.write(cover_letter)
                st.download_button("Download Cover Letter", cover_letter, file_name=f"{job_title}_Cover-Letter.txt")

            else:
                st.error("Please enter a valid job link and job title.")


def main():
    st.title("Job Search Agent")
    st.write("Welcome to your personal job search assistant")
    cv_file = upload_CV()
    if cv_file:
        select_tasks(cv_file)


if __name__ == "__main__":
    main()     