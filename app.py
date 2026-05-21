import io
import os
import PyPDF2
import streamlit as st
from agent import search_jobs, get_page_date, is_job_active, is_recent, is_search_page, summarise_cv, generate_cover_letter, fetch_job_page, extract_job_title, search_jobs
import re
import time

st.sidebar.header("Instructions")
with st.sidebar.expander("How to Use This App", icon=":material/info:"):
    st.write("""
        1. Upload your CV in the first step. You can upload a .txt or .pdf file.
        2. In the second step, you can either search for jobs based on your CV summary or generate a cover letter for a specific job.
        3. If you choose to search for jobs, you can enter a search query (e.g., 'Software Engineer in London') and the app will return relevant job opportunities.
        4. You can then generate personalized cover letters for the job opportunities found in the search results.
        5. If you choose to generate a cover letter directly, simply enter the job title and paste the job description URL, and the app will create a tailored cover letter for you.
        """)

def read_cv_file(cv_file):
    # Plain text
    if cv_file.name.endswith(".txt"):
        return cv_file.read().decode("utf-8")
    
    # PDF
    elif cv_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(cv_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    else:
        st.error("Please upload a .txt or .pdf file")
        return None

def upload_CV():
    st.header("Step 1: Upload Your CV")
    # Show status if CV already saved
    if os.path.exists("cv.txt"):
        st.success("CV already loaded from previous session")
        if st.button("Remove CV"):
            os.remove("cv.txt")
            if os.path.exists("cv_summary.txt"):
                os.remove("cv_summary.txt")
            st.rerun()
        with open("cv.txt", "r") as f:
            return f.read()
    
    # No saved CV — show uploader
    cv_file = st.file_uploader("Upload your CV", type=["txt", "pdf"])
    if cv_file is not None:
        cv_content = read_cv_file(cv_file)  # ← use this instead of .decode()
        if cv_content:
            with open("cv.txt", "w") as f:
                f.write(cv_content)
            return cv_content
    
    return None

def select_tasks(cv_content):
    # Step 2: Select Task
    st.header("Step 2: Select Task")
    tab1, tab2, tab3 = st.tabs(["Search Jobs", "Generate Cover Letter", "Keyword Confidence"])

    with tab1:
        # Check for saved job opportunities
        if os.path.exists("job_opportunities/job_opportunities.txt"):
            use_saved = st.segmented_control("Use previously saved job opportunities", ["Yes", "No"], default="Yes", key="use_saved_jobs")
            # If the user chooses to use saved job opportunities, load and display them
            if use_saved == "Yes":
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
                                cover_letter = generate_cover_letter(cv_content, job_line, job_title)
                                st.subheader(f"Generated Cover Letter for {job_title}")
                                st.write(cover_letter)
                                st.download_button(f"Download Cover Letter for {job_title}", cover_letter, file_name=f"{job_title}_Cover-Letter.txt")   
                
            # If the user does not choose to use saved job opportunities, proceed with search
            else:
                st.header("Search for Jobs")
                search_query = st.text_input("Enter your job search query (e.g., 'Software Engineer in London')", key="search_query")
                cv_summary = summarise_cv(cv_content)
                with st.expander("CV Summary", icon=":material/info:"):
                    st.write(cv_summary)
                if st.button("Search Jobs", key="search_jobs"):
                    with st.spinner("Searching for jobs..."):
                        st.session_state.reply = search_jobs(cv_summary, search_query)
                        st.write(st.session_state.reply)
                    if st.button("Create Cover Letters for Search Results", key="create_cover_letters_search_results"):
                        with st.spinner("Generating cover letters for search results..."):
                            job_lines = st.session_state.reply.splitlines() 
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
                                    cover_letter = generate_cover_letter(cv_content, job_line, job_title)
                                    st.subheader(f"Generated Cover Letter for {job_title}")
                                    st.write(cover_letter)
                                    st.download_button(f"Download Cover Letter for {job_title}", cover_letter, file_name=f"{job_title}_Cover-Letter.txt")


            
        else:
            # No saved job opportunities, proceed with search
            st.header("Search for Jobs")
            search_query = st.text_input("Enter your job search query (e.g., 'Software Engineer in London')", key="search_query")
            cv_summary = summarise_cv(cv_content)
            with st.expander("CV Summary", icon=":material/info:"):
                    st.write(cv_summary)
            if st.button("Search Jobs", key="search_jobs"):
                with st.spinner("Searching for jobs..."):
                    st.session_state.reply = search_jobs(cv_summary, search_query)
                    st.write(st.session_state.reply)
                if st.button("Create Cover Letters for Search Results", key="create_cover_letters_search_results"):
                        with st.spinner("Generating cover letters for search results..."):
                            job_lines = st.session_state.reply.splitlines() 
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
                                    cover_letter = generate_cover_letter(cv_content, job_line, job_title)
                                    st.subheader(f"Generated Cover Letter for {job_title}")
                                    st.write(cover_letter)
                                    st.download_button(f"Download Cover Letter for {job_title}", cover_letter, file_name=f"{job_title}_Cover-Letter.txt")


    with tab2:
        st.header("Generate Cover Letter")
        job_title = st.text_input("Enter the Job Title you are applying for")
        job_url = st.text_input("Paste the Job Link here")
        if st.button("Generate Cover Letter", key="generate_cover_letter"):
            if job_url and job_title:
                job_page = fetch_job_page(job_url) 
                cover_letter = generate_cover_letter(cv_content, job_page, job_title)
                st.subheader("Generated Cover Letter") 
                st.write(cover_letter)
                st.download_button("Download Cover Letter", cover_letter, file_name=f"{job_title}_Cover-Letter.txt")

            else:
                st.error("Please enter a valid job link and job title.")
    with tab3:
        st.header("Keyword Confidence")
        st.write("This tab will display the keyword confidence analysis for your CV and job descriptions.")
        # Add your keyword confidence analysis code here

def main():
    st.title("Job Search Agent")
    st.write("Welcome to your personal job search assistant")
    cv_content = upload_CV()
    if cv_content :
        select_tasks(cv_content)


if __name__ == "__main__":
    main()     