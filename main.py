"""
Cold Email Generator Application

This Streamlit application automates the process of generating personalized cold emails 
based on job postings. It extracts job details from provided URLs, matches them with 
relevant portfolio projects, and generates tailored cold emails.

Main components:
- URL input for job postings
- Job information extraction
- Portfolio matching
- Email generation
"""

from dotenv import load_dotenv

load_dotenv()

# Now import the rest
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    """
    Creates and configures the Streamlit application interface.
    """
    # Add custom styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E88E5;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section with description
    st.markdown('<h1 class="main-header">Cold Email Generator</h1>', unsafe_allow_html=True)
    st.markdown("""
        Generate personalized cold emails based on job postings. Simply paste a job URL below 
        and get tailored emails that highlight relevant portfolio projects.
    """)

    # Create two columns for input
    col1, col2 = st.columns([3, 1])
    with col1:
        url_input = st.text_input("Enter Job Posting URL:", placeholder="https://example.com/job-posting")
    with col2:
        submit_button = st.button("Generate Emails", type="primary")

    # Add a spinner during processing
    if submit_button and url_input:
        with st.spinner("Analyzing job posting and generating emails..."):
            try:
                # Load and process job posting
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                # Display results in expandable sections
                for i, job in enumerate(jobs, 1):
                    with st.expander(f"Email {i}: {job.get('role', 'Job Role')}", expanded=True):
                        # Show job details in a clean format
                        st.markdown("### Job Details")
                        st.markdown(f"**Role:** {job.get('role', 'N/A')}")
                        st.markdown(f"**Experience:** {job.get('experience', 'N/A')}")
                        
                        # Display skills as tags
                        st.markdown("**Required Skills:**")
                        skills = job.get("skills", [])
                        st.markdown(" ".join([f"`{skill}`" for skill in skills]))
                        
                        # Generate and display email
                        skills = job.get("skills", [])
                        portfolio_urls = portfolio.query_links(skills)
                        email = llm.write_email(job, portfolio_urls)
                        
                        st.markdown("### Generated Email")
                        st.code(email, language="markdown")
                        
                        # Add copy button for email
                        st.button("📋 Copy Email", key=f"copy_{i}", 
                                on_click=lambda: st.write("Email copied to clipboard!"))

            except Exception as e:
                st.error(f"An Error Occurred: {e}")
                st.markdown("""
                    Please check that:
                    - The URL is valid and accessible
                    - The job posting is publicly available
                    - Your internet connection is stable
                """)
    
    # Add helpful information in the sidebar
    with st.sidebar:
        st.markdown("### How It Works")
        st.markdown("""
            1. Paste a job posting URL
            2. Click Generate Emails
            3. Review generated emails
            4. Copy and customize as needed
            
            **Tips:**
            - Use public job posting URLs
            - Make sure portfolio data is up-to-date
            - Review and personalize emails before sending
        """)
        
        # Add example URL
        st.markdown("### Example URL")
        st.code("https://example.com/job-posting")
        
        # Add version info and credits
        st.markdown("---")
        st.markdown("v1.0.0 | Made by Harmeet")

if __name__ == "__main__":
    # Configure page settings
    st.set_page_config(
        page_title="Cold Email Generator",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize components
    chain = Chain()
    portfolio = Portfolio(file_path="./sample_portfolio.csv")
    create_streamlit_app(chain, portfolio, clean_text)