# Importing necessary libraries and modules
import re
import AI_Tools as tls
import time
from loguru import logger # Import logger
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load JSON data into a Langchain TextLoader
# Define the path to the JSON file
json_file_path = './Dataset/moon_flight_system_data_10k.json'
# Initialize a TextLoader with the specified JSON file
loader = TextLoader(json_file_path, encoding = 'UTF-8')
# Load the documents from the specified JSON file
documents = loader.load()

# Split the loaded documents using RecursiveCharacterTextSplitter
# Initialize a RecursiveCharacterTextSplitter for splitting documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
# Split the loaded documents into chunks for easier processing
confluence_source_chunks = text_splitter.split_documents(documents)

# Loading an existing Vector Knowledge Base
# Define the path to the existing Vector Knowledge Base
confluence_db_file_name = './Db/DB_Confluence'
# Load the existing Vector Knowledge Base using custom tools (tls)
confluence_db = tls.load_db(confluence_db_file_name, tls.embeddings)

if __name__ == "__main__":
    # Configure the logger to write logs to a file with specific settings
    logger.add("Log/22_RAG_Confluence.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('22_RAG_Confluence............')
    start_time = time.time()

    # Define the topic for query, which is about installing the moon flight system
    # confluence_topic = "How to install Moon Flight System? Give me the main details."
    confluence_topic = "Как установить Moon Flight System? Дай мне информацию из документации."
    # Get the content related to the query using an ensemble method for message content retrieval
    confluence_message_content = tls.get_message_content_ensemble(confluence_topic, confluence_db, confluence_source_chunks, 3)

    # Define the system content for the assistant
    system_content = '''You are a useful assistant.
    You have data on the necessary docs in Confluence.'''

    # Define the user content for the query
    user_content = f'{confluence_topic}. The data is here: {confluence_message_content}'

    # Make a GPT request to generate a response for the given user content
    response = tls.gpt_request(user_content, system_content)
    # Log the generated response
    logger.debug(f'response={response}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'22_RAG_Confluence elapsed_time = {elapsed_time} sec')