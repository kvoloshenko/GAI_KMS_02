# Importing necessary libraries and modules
import re
import AI_Tools as tls
import time
from loguru import logger # Import logger
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load JSON data into a Langchain TextLoader
# Define the path to the JSON file
json_file_path = './Dataset/jira_tickets_10k.json'
# Initialize a TextLoader with the specified JSON file
loader = TextLoader(json_file_path, encoding = 'UTF-8')
# Load the documents from the specified JSON file
documents = loader.load()

# Split the loaded documents using RecursiveCharacterTextSplitter
# Initialize a RecursiveCharacterTextSplitter for splitting documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
# Split the loaded documents into chunks for easier processing
jira_source_chunks = text_splitter.split_documents(documents)

# Loading an existing Vector Knowledge Base
# Define the path to the existing Vector Knowledge Base
jira_db_file_name = './Db/DB_Jira'
# Load the existing Vector Knowledge Base using custom tools (tls)
jira_db = tls.load_db(jira_db_file_name, tls.embeddings)

if __name__ == "__main__":
    # Configure the logger to write logs to a file with specific settings
    logger.add("Log/21_RAG_Jira.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('21_RAG_Jira............')
    start_time = time.time()

    # Define the topic for query, which is about installing the moon flight system
    jira_topic = "Give me tickets related to Moon Flight System. I need Ticket id, Summary and Project name."

    # Get the content related to the query using an ensemble method for message content retrieval
    jira_message_content = tls.get_message_content_ensemble(jira_topic, jira_db, jira_source_chunks, 10)

    # Define the system content for the assistant
    system_content = '''You are a useful assistant.
    You have data on the necessary tickets in Jira.'''

    # Define the user content for the query
    user_content = f'{jira_topic}. The data is here: {jira_message_content}'

    # Make a GPT request to generate a response for the given user content
    response = tls.gpt_request(user_content, system_content)
    # Log the generated response
    logger.debug(f'response={response}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'21_RAG_Jira elapsed_time = {elapsed_time} sec')