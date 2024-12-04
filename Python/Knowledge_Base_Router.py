from loguru import logger
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json
import time
from SimpyRAG import process_question

def get_route(question):
    logger.debug('get_route............')
    start_time = time.time()
    logger.debug(f"question = {question}")

    router_instructions = """You are an expert in routing a user question.
    You need to determine where to route a user question: to Jira or Confluence or Git or Other.
    Jira contains tickets about software products and systems.
    Confluence contains documentation about software products and systems, including installation instructions.
    Git contains source code for software products and systems.
    If the user's question is not about Jira, Confluence or Git, then it is a question about Other.
    Return the answer in JSON format with a single key 'datasource' and the value 'jira' or 'confluence' or 'git' or 'other'. 
    depending on the question. Don't return anything other than JSON"""

    # LM Studio
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        temperature=0,
        api_key="not-needed"
    )

    llm_json_mode = llm.bind(response_format={"type": "json_object"})

    route_question = llm_json_mode.invoke(
        [SystemMessage(content=router_instructions)]
        + [HumanMessage(content=question)]
    )

    logger.debug(f'route_question={route_question}')

    try:
        # Убедимся, что ответ корректный и является строкой
        response_content = route_question.content.strip()
        if response_content.startswith("```") and response_content.endswith("```"):
            # Извлекаем строку внутри тройных обратных кавычек
            response_content = response_content[3:-3].strip()

        # Пытаемся загрузить JSON
        route_json = json.loads(response_content)
        source = route_json.get("datasource", "unknown")  # Получаем значение, если оно присутствует
    except json.JSONDecodeError:
        logger.debug("Ошибка декодирования JSON. Возможно, ответ не в правильном формате.")
        source = "unknown"
    except Exception as e:
        logger.debug(f"Произошла ошибка: {e}")
        source = "unknown"

    logger.debug(f'source = {source}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'get_route elapsed_time = {elapsed_time} sec')
    return source


def get_responce(question):
    logger.debug('get_responce............')
    start_time = time.time()

    source = get_route(question)
    response = "На этот вопрос нет ответа. Задайте другой вопрос"

    # Вызываем process_question в зависимости от source
    if source == 'confluence':
        response = process_question(
            question=question,
            db_file_name='./Db/DB_Confluence',
            system_message='Вы полезный ассистент. Вы отвечаете на вопросы о документации, хранящейся в Confluence, о программных продуктах и системах.'
        )
    elif source == 'jira':
        response = process_question(
            question=question,
            db_file_name='./Db/DB_Jira',
            system_message='Вы полезный ассистент. Вы отвечаете на вопросы о тикетах Jira, связанных с программными продуктами и системами.'
        )
    elif source == 'git':
        response = process_question(
            question=question,
            db_file_name='./Db/Git_Kind_Doctor',
            system_message='Вы полезный ассистент. Вы отвечаете на вопросы о исходном коде программных продуктов и систем, хранящемся в Git.'
        )

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'response= {response}')
    logger.debug(f'get_responce = {elapsed_time} sec')

    return response



if __name__ == "__main__":


    questions = [
        "Как установить Moon Flight System?",
        "Какие есть tickets на Moon Flight System?",
        "Где в исходном коде было определено file_name?",
        "Как полететь на Луну?"
    ]

    for question in questions:
        responce = get_responce(question)
        print (question)
        print(responce)