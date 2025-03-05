"""
Chain Module

This module implements the language model chains for processing job postings
and generating cold emails. It uses the Groq LLM API for text generation.
"""

import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langsmith import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "cold_email_generator"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Initialize LangSmith client with explicit API key
client = Client(
    api_url="https://api.smith.langchain.com",
    api_key=os.getenv("LANGSMITH_API_KEY"),
)

class Chain:
    """
    Manages language model chains for job processing and email generation.
    
    This class handles:
    - Job information extraction from postings
    - Cold email generation based on job details and portfolio
    """

    def __init__(self):
        """
        Initializes the Chain with a Groq LLM configuration.
        """
        self.llm = ChatGroq(
                        model="llama-3.3-70b-versatile",
                        temperature=0,
                        max_tokens=None,
                        timeout=None,
                        max_retries=2)
    
    
    def extract_jobs(self, cleaned_text):
        """
        Extracts structured job information from cleaned job posting text.
        
        Args:
            cleaned_text (str): Preprocessed job posting text
            
        Returns:
            list: List of dictionaries containing job details with keys:
                 'role', 'experience', 'skills', and 'description'
                 
        Raises:
            OutputParserException: If content is too large to parse
        """
        prompt_extract = PromptTemplate.from_template("""
                I will give you scraped text from the job posting. 
                Your job is to extract the job details & requirements in a JSON format containing the following keys: 'role', 'experience', 'skills', and 'description'. 
                Only return valid JSON. No preamble, please.
                Here is the scraped text: {page_data}
                """)    
        
        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={"page_data" : cleaned_text})
        
        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Content too big, unable to parse jobs.")
        
        return response if isinstance(response, list) else [response]


    def write_email(self, job_description, portfolio_urls):
        """
        Generates a personalized cold email based on job details and portfolio.
        
        Args:
            job_description (dict): Extracted job details
            portfolio_urls (list): Relevant portfolio project URLs
            
        Returns:
            str: Generated cold email content
        """
        prompt_email = PromptTemplate.from_template(
                """
                I will give you a role and a task that you have to perform in that specific role.
                Your Role: Your name is Harmeet, You are an incredible business development officer who knows how to get clients. You work for AllInOneAI Consulting firm, your firm works with all sorts of IT clients and provide solutions in the domain of Data Science and AI. 
                AllInOneAI focuses on efficient tailored solutions for all clients keeping costs down. 
                Your Job: Your Job is to write cold emails to clients regarding the Job openings that they have advertised. Try to pitch your clients with an email hook that opens a conversation about a possibility of working with them. Add the most relevant portfolio URLs from
                the following (shared below) to showcase that we have the right expertise to get the job done. 
                I will now provide you with the Job description and the portfolio URLs:
                JOB DESCRIPTION: {job_description}
                ------
                PORTFOLIO URLS: {portfolio_urls}
                """)
        
        chain_email = prompt_email | self.llm
        response = chain_email.invoke({"job_description": str(job_description), "portfolio_urls": portfolio_urls})

        return response.content
        