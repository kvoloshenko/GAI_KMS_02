# Import necessary modules and tools
import AI_Tools as tls
from loguru import logger # Import logger for detailed logging
# Import csv and json modules
import csv
import json
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Converting a CSV file to an JSON file
def csv_to_json(csv_file_path, json_file_path):
    """
    Function to convert a CSV file to a JSON file.

    :param csv_file_path: Path to the input CSV file.
    :param json_file_path: Path to the output JSON file.
    """

    # Open and read the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        rows = list(csv_reader)

    # Write data to JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(rows, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Setup logger with specifics for logging
    logger.add("Log/11_Create_Vector_Db_Jira.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('11_Create_Vector_Db_Jira............')

    # Define file paths and convert CSV file to JSON file
    csv_file_path = 'Dataset/jira_tickets_100.csv'
    json_file_path = 'Dataset/jira_tickets_100.json'
    # Call the function to convert CSV to JSON
    csv_to_json(csv_file_path, json_file_path)

    # Load JSON data into a Langchain TextLoader
    loader = TextLoader(json_file_path, encoding='UTF-8')
    documents = loader.load()

    # Split the loaded documents using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    jira_source_chunks = text_splitter.split_documents(documents)

    # Create the FAISS vector database for Jira data
    jira_db_file_name = './Db/DB_Jira'
    jira_db = tls.create_db(jira_source_chunks, tls.embeddings, jira_db_file_name)

