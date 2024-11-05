# GAI_KMS_02
Это прототип решения типа Agentic RAG (Retrieval-Augmented Generation) на основе LangGraph с данными из Jira, Confluence и Git.


## Описание

![GenAI_Powered_KMS_02.png](Images%2FGenAI_Powered_KMS_02.png)

Система управления знаниями GenAI-Powered Knowledge Management System» предназначена для оптимизации управления 
знаниями в организации с использованием передовых возможностей искусственного интеллекта.

**1. Взаимодействие с пользователем (User Interaction):**

* **User**: Процесс начинается с пользователя, который задает вопрос агентам AI.
* **GenAI_Agent**: Агенты GenAI являются ключевыми компонентами, получающими вопросы от пользователей и 
предоставляющими ответы.

**2. Управление контекстом (Context Management):**

* **Контекст данных (Data Context)**: Агенты GenAI взаимодействуют с контекстом данных, размещенным в истории чата. 
Они получают данные контекста и обновляют их по мере необходимости, обеспечивая актуальный поток информации.

**3. Использование инструментов (Tool Utilization):**

* **Инструмент поиска и суммаризации (Search Tool & Summary Tool)**: Для предоставления точных и релевантных ответов 
агенты GenAI используют инструменты поиска и суммаризации. Эти инструменты взаимодействуют с векторными базами данных 
для извлечения релевантных фрагментов информации.

**4. Внешний поиск (External Search):**

* **Вебпоиск (WebSearch)**: В дополнение к внутренним данным агенты GenAI могут выполнять веб-поиск для сбора 
дополнительной информации, которая может иметь отношение к вопросу пользователя.

**5. Загрузка данных (Data Ingestion):**

* **Загрузчики документов (Document Loaders)**: Эти компоненты наполняют векторные базы данных из различных исходных 
систем - Jira, Confluence и Git, обеспечивая агентам GenAI богатый набор данных для работы.


Эта архитектура обеспечивает бесшовную интеграцию данных и интеллектуальное разрешение запросов, используя как 
структурированные внутренние данные, так и внешние ресурсы для повышения эффективности управления знаниями.

### Используемые материалы:

Course: **AI Agents in LangGraph** https://learn.deeplearning.ai/courses/ai-agents-in-langgraph/lesson/1/introduction

Documentation: https://python.langchain.com/v0.2/docs/introduction/

GitHub: https://github.com/langchain-ai/langgraph/tree/main

LangGraph and RAG: https://github.com/langchain-ai/langgraph/tree/main/examples/rag

Agentic RAG: https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_agentic_rag.ipynb

# Реализация

## 0.Генерация синтетических данных

### 0.1. Генерация синтетических данных в формате JSON для эмуляции данных Confluence
(_01_SyntheticDataGeneration_Confluence.py_)

Этот модуль предназначен для генерации запрошенного количества записей синтетических данных, 
с метаданными и описаниями, и сохранить их в указанном JSON-файле.

Данные посвящены описанию вымышленного программного продукта под названием «Moon Flight System».

### 0.2. Генерация синтетических данных в формате CSV для эмуляции данных Jira (_02_SyntheticDataGeneration_Jira.py_)

Этот модуль использует библиотеку Faker для генерации реалистичных случайных данных для различных полей.

Данные содержат информацию о тикетах Jira для вымышленного программного продукта под названием «Moon Flight System».

### 1.1. Создание новой векторной базы знаний для Jira (_11_Create_Vector_Db_Jira.py_)
Этот модуль предназначен для преобразования CSV-файла с данными тикетов Jira в формат JSON, 
разбивает данные на фрагменты и создает векторную базу данных FAISS для эффективного поиска. 

**Краткое описание**

1. **Преобразование из CSV to JSON**: Преобразует указанный CSV-файл в JSON-файл для сохранении информации о заголовках 
столбцов.
2. **Загрузка документа**: Загружает JSON-файл и обрабатывает его с помощью Langchain `TextLoader`.
3. **Разделение текста (Text Splitting)**: Разбивает загруженный текстовый документ на фрагменты (chunks) с помощью 
Langchain's `RecursiveCharacterTextSplitter`.
4. **Создание базы данных**: Создает векторную базу данных FAISS на основе обработанных текстовых фрагментов (chunks) 
для эффективного поиска и хранения информации.

### 1.2. Создание новой векторной базы знаний для Confluence (_12_Create_Vector_Db_Confluence.py_)

Этот Python-модуль обрабатывает JSON-файл, содержащий данные Confluence, разбивает их на фрагменты, 
и создает векторную базу данных FAISS для эффективного поиска. 

**Краткое описание**

- **Загрузка данных в формате JSON**: Считывает данные Confluence из файла JSON.
- **Создание документа**: Преобразует JSON-данные в объекты `Document`, совместимые с Langchain.
- **Разделение текста (Text Splitting)**: Разбивает документ на фрагменты (chunks).
- **Создание базы данных**: Создает векторную базу данных FAISS из фрагментов документов для эффективного поиска данных.

###  1.3. Создание новой базы знаний для Git (_13_Create_Vector_Db__Git.py_)
Этот Python-модуль предназначен для клонирования Git-репозитория, загрузки из него определенных файлов, 
разделение данных на фрагменты (chunks) и создания векторной базы знаний.  

**Краткое описание**
- **Клонирование репозитория Git**: Клонирует определенный Git-репозиторий с GitHub в локальную директорию.
- **Загрузка документов**: Использует `GitLoader` для загрузки документов из клонированного репозитория.
- **Фильтрация**: Фильтрует загруженные документы, чтобы использовать только файлы Python.
- **Разделение текста (Text Splitting)**: Разделяет содержимое загруженных документов на фрагменты (chunks).
- **Создание векторной базы данных**: Создает векторную базу данных FAISS из фрагментов документов для эффективного 
поиска данных.

### 2.1. Simple RAG for Jira (_21_RAG_Jira.py_)
This Python module is designed to process and retrieve specific information from a dataset of Jira tickets 
using a vector-based knowledge system. 

It involves loading the dataset, splitting the text for easier processing, loading an existing knowledge base, 
and then querying that knowledge base to extract relevant information.

**Summary**

1. **Imports and Initial Setup**:
    - Import necessary libraries and modules: `re`, custom module `AI_Tools` as `tls`, `logger` from `loguru` for logging, `TextLoader` and `RecursiveCharacterTextSplitter` from `Langchain`.

2. **Loading Data**:
    - Load a JSON file containing Jira ticket data using `Langchain`'s `TextLoader` with UTF-8 encoding.
    - `json_file_path` specifies the path to the JSON file containing the Jira tickets data.
  
3. **Text Splitting**:
    - Split the loaded JSON documents into smaller chunks of text for easier processing using `RecursiveCharacterTextSplitter`.
    - The `chunk_size` is set to 512 characters and there is no overlap between chunks.
  
4. **Loading Knowledge Base**:
    - Load an existing vector knowledge base of Jira data using a custom tool from `AI_Tools`.
    - The `jira_db_file_name` specifies the file name for the vector knowledge base.
  
5. **Main Execution Block**:
    - Configure the logger to log debug information to a specific file with file rotation after it reaches 100 KB and compression into zip format.
    - Log a debug statement to indicate the start of the process.
  
6. **Generating Query and Response**:
    - Define a query topic for retrieving specific Jira tickets.
    - Use the custom tool to generate a message content based on the query topic, the loaded knowledge base, and the split text chunks.
    - Define a system content and user content for the AI request.
    - Send a message content request to a GPT-based system to get a formatted response and log the response.

This module is useful for anyone needing to process large collections of textual data and search for specific topics or
items within that data using vector-based retrieval techniques, particularly in the context of Jira tickets.

### 2.2. Simple RAG for Confluence (_22_RAG_Confluence.py_)
This module is designed to process a JSON dataset containing information from Confluence system, 
split the content into manageable chunks, and interact with a vector knowledge base for 
retrieval-augmented generation (RAG). 

It integrates various tools and libraries to load the data, split it into text chunks, 
and query a pre-existing vector database to answer user queries to the data from Confluence.

#### 2.2.1. Description
The logic of this module is similar to the Simple RAG for Jira module described above.

### 2.3. (_23_RAG_Git.py_)
This Python module facilitates the extraction and processing of Python source files from a given Git repository. 
The primary steps involved in this module include:

1. **Initialization**:
   - Import required libraries and custom tools.
   - Configure a GitLoader to filter and load only Python files from a specified repository.

2. **Loading and Logging**:
   - Load these filtered documents from the repository.
   - Log the number of documents loaded and their source file paths.

3. **Document Processing**:
   - Split the loaded documents into smaller chunks for easier processing.
   - Load or create a vector-based knowledge database from these document chunks using custom AI tools.

4. **Query and Response Generation**:
   - Define and configure the logger for detailed logging.
   - Define a specific query to search within the source code repository.
   - Retrieve relevant content from the knowledge base.
   - Generate a response to the query using GPT-based tools.

5. **Logging Execution Details**:
   - Log key details including the response and the elapsed time for the execution.

This module serves as a useful tool for searching and querying specific information within a codebase, 
leveraging AI tools to provide meaningful insights and responses.



### 2.4. WebSearch (_24_WebSearch.py_)
This module performs a web search using DuckDuckGo's search engine. 
It utilizes the `DuckDuckGoSearchRun` class from the `langchain_community.tools` package to execute the search query. 

This module is suitable for scenarios where automated web search and detailed logging of the search process are required. 
It can be used in automation tasks, data gathering, and performance analysis.

### 3.0. Agents (_30_Agents.py_)

This module integrates various AI tools to create an intelligent agent capable of answering queries 
related to Jira tickets and Confluence documentation. 
It leverages retrievers for fetching relevant information from pre-loaded databases, 
linguistic models for interpreting and generating responses, 
and a workflow graph for managing the agent's decision process.

**Summary**

1. **Loading Databases**:
   - Loads Jira and Confluence databases into retrievers for querying.

2. **Creating Retriever Tools**:
   - Sets up tools for querying Jira tickets and Confluence documentation.

3. **Agent State Definition**:
   - Defines the state for agent, which will include messages.

4. **Graph Nodes**:
   - **Agent**: Handles invocation of the agent model.
   - **Retrieve**: Retrieves documents using retrievers.
   - **Rewrite**: Rewrites queries to be more effective.
   - **Generate**: Generates responses based on relevant documents.

5. **Graph Edges**:
   - Defines the workflow for how different nodes interact based on conditions.

6. **Main Execution**:
   - Initializes logging and demonstrates usage with sample queries.

By integrating various AI components, this module provides an interactive agent capable of handling complex queries 
and fetching relevant information dynamically.

**Nodes and Edges**

We can lay out an agentic RAG graph like this:

* The state is a set of messages
* Each node will update (append to) state
* Conditional edges decide which node to visit next

![Nodes_Edges_01.png](Images%2FNodes_Edges_01.png)

### 3.1. Agents (_31_Agents.py_)

This module is similar to the _30_Agents.py_ module described above. Added capable of answering queries related to  Git.

#### Overview
This Python module is designed to facilitate intelligent document retrieval and responsive query handling using 
a combination of local knowledge databases, Large Language Models (LLMs), and custom AI tools. 
It connects to knowledge bases from platforms like Jira, Confluence, and Git, allowing users to input queries 
and receive processed, relevant information in response. 
The system is designed with a modular architecture and uses a directed graph workflow to manage the query 
lifecycle steps.

**Functionality Breakdown**

1. **Imports and Dependencies**
    - **`time`**: Used for measuring execution time.
    - **`loguru.logger`**: For logging various activities and events in the system.
    - **`AI_Tools as tls`**: Custom AI tools package for database loading.
    - **`langchain.tools.retriever.create_retriever_tool`**: Function to create retriever tools.
    - **`Annotated, Sequence, TypedDict` from `typing`**: Utility types for type hints. 
    - **`BaseMessage` from `langchain_core.messages`**: Base message class for handling message structures.
    - **`add_messages` from `langgraph.graph.message`**: Function for appending messages in the workflow graph.

2. **Knowledge Base Loading**
    - Loads existing vectorized knowledge bases for Jira, Confluence, and Git using custom AI tools (`tls`).
    - Creates retrievers for these knowledge bases to facilitate retrieval operations.

3. **Tool Creation**
    - Creates specific retriever tools for Jira, Confluence, and Git, each with pre-defined information to fetch 
(e.g., Jira tickets, Confluence documentation, Git source code).

4. **Agent State Definition**
    - Defines the `AgentState` type using `TypedDict` for structuring the state which includes a sequence of messages.

5. **Relevance Grading**
    - Defines the logic to grade the retrieved documents' relevance to the user query using an LLM (GPT-4).
    - Uses a predefined prompt to instruct the model on relevance assessment.

6. **Agent Invocation**
    - Handles logic for agent actions which include deciding on retrieval, generating responses, or ending 
interactions based on the query and state.

7. **Query Rewriting**
    - Transforms the user query to a semantically improved version for better understanding and processing by the LLM.

8. **Response Generation**
    - Generates a final response based on the relevant documents and the refined query using an LLM.

9. **Graph-based Workflow Management**
    - Uses a state graph workflow to manage the cycle between nodes including agent decisions, document retrieval, 
query rewriting, and response generation.

10. **Main Execution and Query Interface**
    - Provides a function `ask_agent(question)` to allow users to input questions and interact with the system.
    - Measures performance and logs the response time for each query.
    - Main block to initialize the logging setup and test the system with sample queries.

**Usage**
This module allows users to interact with complex knowledge bases through simple queries. It integrates document 
retrieval with LLMs to provide coherent and relevant responses. 
The graph workflow logic ensures that the process is streamlined and maintains a clear state through different stages 
of query handling.

**Example Usages**
- Asking for specific Jira ticket details.
- Requesting documentation from Confluence.
- Finding specific lines or files within a repository on Git.

The thoughtful combination of knowledge bases, AI-driven tools, and a well-structured state graph makes this module 
suitable for environments needing intelligent document retrieval and query resolution.

### _AI_Tools.py_
This module facilitates advanced text processing and retrieval using embeddings 
and other natural language processing techniques. 
It leverages various tools such as OpenAI for generating responses, FAISS for efficient vector similarity search, 
Loguru for robust logging, and LangChain for splitting text into manageable chunks and calculating embeddings.

This code covers setting up API clients, splitting text into chunks, obtaining embeddings, creating and 
loading vector knowledge bases, and combining different retrieval methods to get the most relevant text chunks 
based on a given topic. 
Each function is modular and well-documented, easing the maintenance and extension of functionality.
