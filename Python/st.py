from Agents import ask_agent
import streamlit as st

from loguru import logger

# Настройка логирования с использованием loguru
logger.add("Log/st.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB", compression="zip")

#TODO
# @st.cache_data
# def load_all():
#     dir = 'pdf'
#     # db_file_name = 'db/db_systems_analyst'
#     db_file_name = 'db/db_sa_ml'
#     db = get_index_db(dir, db_file_name)
#     logger.debug('Данные загружены')
#     return db

# Функция получения ответа от агента
def get_model_response(q):

    r = ask_agent(q)
    response = q + "\n" + r
    return response

# db = load_all()
# Поля ввода
question_input = st.text_input("Введите вопрос: ", key="input_text_field")


response_area = st.empty()


if question_input:
    model_response = get_model_response(question_input)
    response_area.text_area("Ответ", value=model_response, height=400)





