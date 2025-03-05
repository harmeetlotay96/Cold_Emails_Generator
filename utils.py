"""
Utility Module

Provides text processing utilities for the cold email generator application.
"""

import re

def clean_text(text):
    """
    Cleans and normalizes input text by removing HTML, URLs, special characters,
    and excess whitespace.
    
    Args:
        text (str): Raw input text
        
    Returns:
        str: Cleaned and normalized text
        
    Example:
        >>> clean_text("<p>Hello  World! http://example.com</p>")
        'Hello World'
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text