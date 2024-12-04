from loguru import logger
from langchain_openai import ChatOpenAI
import time
import AI_Tools as tls
import re

# Получаем эмбеддинги
embeddings = tls.get_embeddings()


def get_message_content(topic, index_db, num_relevant_chunks):
    """Извлекает релевантные куски текста из Базы Знаний."""
    logger.debug('Получение содержимого сообщения...')
    logger.debug(f'Тема: {topic}; Число релевантных кусочков: {num_relevant_chunks}')

    start_time = time.time()

    # Поиск схожести
    docs = index_db.similarity_search(topic, k=num_relevant_chunks)

    # Форматирование извлеченных данных
    message_content = re.sub(r'\n{2}', ' ', '\n'.join(
        [f'#### {i + 1} Relevant chunk ####\n' + str(doc.metadata) + '\n' + doc.page_content for i, doc in
         enumerate(docs)]
    ))

    logger.debug(message_content)
    elapsed_time = time.time() - start_time
    logger.debug(f'Время выполнения get_message_content = {elapsed_time:.2f} сек')

    return message_content


def process_question(question, db_file_name, system_message, num_chunks=3):
    """Обрабатывает вопрос, загружает БД, получает содержимое и запрашивает LLM."""
    db = tls.load_db(db_file_name, embeddings)
    message_content = get_message_content(question, db, num_chunks)

    user_content = f'{question}. Данные: {message_content}'
    response = tls.gpt_request(user_content, system_message)

    logger.debug(f'Ответ: {response}')

    return response


if __name__ == "__main__":
    # Jira
    response = process_question(
        question="Какие есть tickets на Moon Flight System?",
        db_file_name='./Db/DB_Jira',
        system_message='Вы полезный ассистент. Вы отвечаете на вопросы о тикетах Jira, связанных с программными продуктами и системами.'
    )
    print(response)

    # Confluence
    response = process_question(
        question="Как установить Moon Flight System?",
        db_file_name='./Db/DB_Confluence',
        system_message='Вы полезный ассистент. Вы отвечаете на вопросы о документации, хранящейся в Confluence, о программных продуктах и системах.'
    )
    print(response)

    # Git
    response = process_question(
        question="Где в исходном коде было определено file_name??",
        db_file_name='./Db/Git_Kind_Doctor',
        system_message='Вы полезный ассистент. Вы отвечаете на вопросы о исходном коде программных продуктов и систем, хранящемся в Git.'
    )
    print(response)