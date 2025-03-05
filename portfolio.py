"""
Portfolio Module

Manages the portfolio database using ChromaDB for efficient storage and 
retrieval of project information based on technical skills.
"""

import csv
import chromadb
import uuid


class Portfolio:
    """
    Handles portfolio management including storage, retrieval, and matching
    of projects based on technical skills.
    
    Attributes:
        file_path (str): Path to the CSV file containing portfolio data
        data (list): Processed portfolio data
        chroma_client: ChromaDB client instance
        collection: ChromaDB collection for portfolio data
    """

    def __init__(self, file_path) -> None:
        """
        Initializes the Portfolio manager.
        
        Args:
            file_path (str): Path to the portfolio CSV file
        """
        self.file_path = file_path
        self.data = self.read_csv_file(self.file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore2')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
   

    def read_csv_file(self, file_path):
        """
        Reads and processes the portfolio CSV file.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            list: List of tuples containing (skills, project_link)
        """
        data = []
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            # Skip the header row
            next(csv_reader)
            for row in csv_reader:
                # Separate technical skills (list) and project link (string)
                skills = tuple(row[:-1])  # Exclude the last element (project link)
                project_link = row[-1]  # Get the last element (project link)
                data.append((skills, project_link))  # Create a tuple with skills and link
        return data


    def load_portfolio(self):
        """
        Loads portfolio data into the ChromaDB collection if not already loaded.
        Creates embeddings for efficient similarity search.
        """
        if not self.collection.count():
            #for value_set in data: 
            for skills, portfolio_url in self.data:
                self.collection.add(
                    documents=str(skills),
                    metadatas = {"portfolio_url": portfolio_url},
                    ids = [str(uuid.uuid4())])
    

    def query_links(self, skills):
        """
        Queries the portfolio database for projects matching given skills.
        
        Args:
            skills (list): List of technical skills to match
            
        Returns:
            list: Metadata containing matching portfolio URLs
        """
        return self.collection.query(query_texts=skills, n_results=2).get("metadatas", [])
                
    

    