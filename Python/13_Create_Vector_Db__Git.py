# Importing necessary libraries and modules
import AI_Tools as tls    # Custom tools for AI/NLP operations
import time               # Library for time-related operations
from loguru import logger # Importing logger for better logging functionality
from git import Repo      # Git library to manage and interact with Git repositorie
from langchain_community.document_loaders import GitLoader # Git loader for handling documents from a repo

if __name__ == "__main__":
    # Configure the logger to write logs to a file with specific settings
    logger.add("Log/13_Create_Vector_Db__Git.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('13_Create_Vector_Db__Git............')
    # Record the start time of the process
    start_time = time.time()

    # Clone an existing Git repository from the URL to a specified directory on disk
    repo = Repo.clone_from('https://github.com/kvoloshenko/Kind_Doctor_TG_Bot_01.git',
                           to_path="./Git_Kind_Doctor")

    # Initialize branch variable to 'master'
    branch = "master"

    # Set the branch to the active branch of the cloned repo
    branch = repo.head.reference

    # Load all documents from the repository
    loader = GitLoader(repo_path="./Git_Kind_Doctor/", branch=branch)
    data = loader.load()
    logger.debug(len(data))
    logger.debug(data[0])

    # Filtering files to load only Python files
    loader = GitLoader(
        repo_path="./Git_Kind_Doctor",
        file_filter=lambda file_path: file_path.endswith(".py"),
    )
    # Load filtered documents
    docs = loader.load()
    logger.debug(len(docs))

    # Extract the source file paths from the loaded documents
    doc_sources = [doc.metadata["source"] for doc in docs]
    logger.debug(doc_sources)

    # Splitting the documents into chunks
    git_source_chunks = tls.split_documents(docs)

    # Creating a vector-based knowledge base from the document chunks
    git_db_file_name = './Db/Git_Kind_Doctor'
    git_db = tls.create_db(git_source_chunks, tls.embeddings, git_db_file_name)

    # Record the end time of the process and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'13_Create_Vector_Db__Git elapsed_time = {elapsed_time} sec')

