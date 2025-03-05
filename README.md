# Cold Email Generator

An automated tool for generating personalized cold emails based on job postings and portfolio projects.

## Features

- Extracts job details from provided URLs
- Matches job requirements with relevant portfolio projects
- Generates personalized cold emails
- Clean and intuitive Streamlit interface

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment variables:
- Create a `.env` file
- Add required API keys

3. Prepare portfolio data:
- Update `sample_portfolio.csv` with your projects

## Usage

1. Run the application:

```bash
streamlit run main.py
```

2. Enter a job posting URL
3. Click Submit to generate personalized emails

## Project Structure

- `main.py`: Streamlit application entry point
- `chains.py`: Language model chains for text processing
- `portfolio.py`: Portfolio management and matching
- `utils.py`: Utility functions
- `sample_portfolio.csv`: Portfolio data storage

## Dependencies

- Streamlit
- LangChain
- ChromaDB
- Groq LLM
