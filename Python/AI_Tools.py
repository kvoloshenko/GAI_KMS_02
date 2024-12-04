from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS # Import FAISS module
from loguru import logger # Import logger
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI


# Функция для запроса LLM
def gpt_request(user_content, system_content):
    logger.debug('gpt_request............')
    start_time = time.time()
    logger.debug(f'user_content={user_content}')
    logger.debug(f'system_content={system_content}')
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio") #<-- Это настройка для LM Studio
    response = client.chat.completions.create(
    model="LL_MODEL",
    messages=[
      {"role": "system", "content": system_content}, # <-- Это системное сообщение
      {"role": "user", "content": user_content}      # <-- Это сообщение пользователя
    ]
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'gpt_request = {elapsed_time} sec')
    return response.choices[0].message.content


# Функция для разделения (splitting) документов
# RecursiveCharacterTextSplitter см. здесь:
# https://python.langchain.com/v0.2/docs/how_to/recursive_text_splitter/
def split_documents(documents):
  # Function to split documents into chunks using RecursiveCharacterTextSplitter
    logger.debug('split_documents............')
    start_time = time.time()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    source_chunks = text_splitter.split_documents(documents)
    logger.debug(type(source_chunks))
    logger.debug(len(source_chunks))
    logger.debug(source_chunks[10].metadata)
    # logger.debug(source_chunks[10].page_content)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'split_documents elapsed_time = {elapsed_time} sec')
    return source_chunks

def get_embeddings(type='cpu'):
  # Функция для получения embeddings model from HuggingFace
    logger.debug('get_embeddings............')
    start_time = time.time()
    model_id = 'intfloat/multilingual-e5-large' # <-- Это имя используемой embeddings модели
    if type=='cpu':
        model_kwargs = {'device': 'cpu'}
    else:
        model_kwargs = {'device': 'cuda'}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs=model_kwargs
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'get_embeddings elapsed_time = {elapsed_time} sec')
    return embeddings

# Initialize embeddings
# embeddings = get_embeddings(type='cuda')

# Getting Embeddings
# embeddings = get_embeddings()

# Функция для создания новой векторной базы знаний
def create_db(source_chunks, embeddings, db_file_name):
    start_time = time.time()
    logger.debug('create_db............')
    db = FAISS.from_documents(source_chunks, embeddings)
    db.save_local(db_file_name)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'create_db elapsed_time = {elapsed_time} sec')
    return db

# Функция для загрузки существующей векторной базы знаний
def load_db(db_file_name, embeddings):
  logger.debug('load_db............')
  start_time = time.time()
  new_db = FAISS.load_local(db_file_name, embeddings, allow_dangerous_deserialization=True)
  end_time = time.time()
  elapsed_time = end_time - start_time
  logger.debug(f'load_db elapsed_time = {elapsed_time} sec')
  return new_db

def split_text(text, max_length):
    """
    Splitting a line into parts with a carriage return
    @param text:
    @param max_length:
    @return:
    """
    words = text.split()  # Split the line into words
    result = []  # List for result

    current_line = ""  # Current line
    for word in words:
      if len(current_line) + len(word) <= max_length:  # If adding a word does not exceed the maximum length
        current_line += word + " "  # Add a word and a space to the current line
      else:
        result.append(current_line.strip())  # Add the current line to the result without extra spaces
        current_line = word + " "  # Start a new line with the current word

    if current_line:  # If there is an unfinished line left
      result.append(current_line.strip())  # Add an unfinished line to the result

    return '\n'.join(result)  # Return the result by concatenating the strings with a newline character.


