from Knowledge_Base_Router import get_responce
import streamlit as st

from loguru import logger

# Настройка логирования с использованием loguru
logger.add("Log/st.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB", compression="zip")


# Функция получения ответа от агента
def get_model_response(q):

    r = get_responce(q)
    response = q + "\n" + r
    return response

# db = load_all()
# Поля ввода
question_input = st.text_input("Введите вопрос: ", key="input_text_field")


response_area = st.empty()


if question_input:
    model_response = get_model_response(question_input)
    response_area.text_area("Ответ", value=model_response, height=400)





