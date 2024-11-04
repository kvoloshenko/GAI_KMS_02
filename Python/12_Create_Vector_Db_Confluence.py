# Import necessary libraries
import AI_Tools as tls                        # Custom AI tools for splitting documents and creating databases
from loguru import logger                     # Logging utility for better logging management
import json                                   # Import json modules
from langchain_core.documents import Document                      # Langchain class for document handling
from langchain_community.document_loaders import TextLoader        # Langchain class for loading texts
from langchain.text_splitter import RecursiveCharacterTextSplitter # Langchain class for splitting text

if __name__ == "__main__":
    # Setting up the logger to write logs to a file with rotation and compression
    logger.add("Log/12_Create_Vector_Db_Confluence.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('12_Create_Vector_Db_Confluence............')

    # Load JSON content from the file
    file_name = './Dataset/moon_flight_system_data_10k.json'
    with open(file_name, 'r') as f:
        confluence_data = json.load(f)

    # Create Langchain Document objects from JSON data
    # Create a list to hold Langchain Document objects created from JSON data
    confluence_documents = []
    for d in confluence_data:
        confluence_documents.append(Document(page_content=d['page_content'], metadata=d['metadata']))
    logger.debug(len(confluence_documents))

    # Split Confluence documents into manageable chunks using a custom tool
    logger.debug(len(confluence_documents))
    confluence_source_chunks = tls.split_documents(confluence_documents)

    # Create the FAISS vector database for Confluence data
    # Define the file name for the FAISS vector database
    confluence_db_file_name = './Db/DB_Confluence'

    # Create the FAISS vector database for the Confluence data
    confluence_db = tls.create_db(confluence_source_chunks, tls.embeddings, confluence_db_file_name)