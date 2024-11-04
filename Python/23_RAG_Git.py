# Importing necessary libraries and modules
import AI_Tools as tls    # Custom AI tools for handling embeddings and database operations
import time               # Library for time-related operations
from loguru import logger # Importing the logger for logging events and messages
from langchain_community.document_loaders import GitLoader # Git loader for handling documents from a repo

# Filtering files to load only Python files
loader = GitLoader(
    repo_path="./Git_Kind_Doctor",
    file_filter=lambda file_path: file_path.endswith(".py"),
)
# Load filtered documents from the repository
docs = loader.load()
logger.debug(len(docs))

# Extract the source file paths from the loaded documents
doc_sources = [doc.metadata["source"] for doc in docs]
logger.debug(doc_sources)

# Splitting the documents into chunks
git_source_chunks = tls.split_documents(docs)

# Load the existing Vector Knowledge Base using custom tools (tls)
git_db_file_name = './Db/Git_Kind_Doctor'
git_db = tls.load_db(git_db_file_name, tls.embeddings)

if __name__ == "__main__":
    # Configure the logger to write logs to a file with specific settings
    logger.add("Log/23_RAG_Git.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('23_RAG_Git............')
    start_time = time.time()

    # Define the topic for query
    git_topic = "I'm looking for where in the source code was defined the file name where is the prompt"

    # Get the content related to the query
    git_message_content = tls.get_message_content_ensemble(git_topic, git_db, git_source_chunks, 4)

    # Define the system content for the assistant
    system_content = '''You are a useful assistant.
    You have the source code from Git.'''

    # Define the user content for the query
    user_content = f'{git_topic}. The data is here: {git_message_content}'

    # Make a GPT request to generate a response for the given user content
    response = tls.gpt_request(user_content, system_content)

    # Log the generated response
    logger.debug(f'response={response}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'23_RAG_Git elapsed_time = {elapsed_time} sec')