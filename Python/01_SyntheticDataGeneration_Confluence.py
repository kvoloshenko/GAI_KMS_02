import json
import random
from loguru import logger # Import logger
import time

def generate_synthetic_data(count):
    titles = [
        "Moon Flight System Documentation",
        "Release Notes",
        "Functional Overview",
        "Hardware and Software Requirements",
        "Installation Instructions",
        "System Architecture",
        "User Manual",
        "API Reference",
        "Документация Moon Flight System",
        "Функциональный обзор",
        "Требования к оборудованию и программному обеспечению",
        "Инструкции по установке",
        "Архитектура системы",
        "Руководство пользователя",
        "Справочник API"
    ]

    descriptions = [
        "This document describes the contents of Moon Flight System 2024.1, March 2024. Purpose: The work completed for this release encompasses the following areas: Enhanced Navigation Algorithms, New User Interfaces, Extended Data Integration, Enhanced Security Features.",
        "The system requirements for Moon Flight System release 2024.1 are described as follows: requires a quad-core processor, 16GB RAM, 250GB SSD, and Internet connectivity.",
        "Deliverables: The server software is distributed in the form of a zip file. For example, in the MFS-2024.1-UNIX.zip file, contains binaries, libraries, and installation scripts.",
        "Installation Instructions: Unzip the MFS-2024.1.zip file, run the installer script with sudo privileges. Follow the prompts to complete the installation process.",
        "API Reference: Moon Flight System offers a comprehensive API with endpoints for mission planning, trajectory calculation, system status, user management, and data retrieval.",
        "System Architecture: The system consists of three major modules: Flight Control, Data Analytics, and User Interaction. Each module is further divided into microservices.",
        "В этом документе описывается содержимое Moon Flight System 2024.1, март 2024 г. Назначение: работа, выполненная для этого выпуска, охватывает следующие области: улучшенные алгоритмы навигации, новые пользовательские интерфейсы, расширенная интеграция данных, улучшенные функции безопасности.",
        "Системные требования для выпуска Moon Flight System 2024.1 описаны следующим образом: требуется четырехъядерный процессор, 16 ГБ ОЗУ, 250 ГБ SSD и подключение к Интернету.",
        "Поставляемые материалы: серверное программное обеспечение распространяется в виде zip-файла. Например, в файле MFS-2024.1-UNIX.zip содержатся двоичные файлы, библиотеки и сценарии установки.",
        "Инструкции по установке: распакуйте файл MFS-2024.1.zip, запустите сценарий установки с привилегиями sudo. Следуйте инструкциям, чтобы завершить процесс установки.",
        "Справочник по API: Moon Flight System предлагает комплексный API с конечными точками для планирования миссий, расчет траектории, состояние системы, управление пользователями и извлечение данных.",
        "Архитектура системы: система состоит из трех основных модулей: управление полетом, аналитика данных и взаимодействие с пользователем. Каждый модуль далее делится на микросервисы"
    ]

    data = []

    for i in range(count):
        entry = {
            "metadata": {
                "title": random.choice(titles),
                "id": str(282083988 + i),
                "source": f"https://moonflightsystem.com/docs/{282083988 + i}"
            },
            "page_content": random.choice(descriptions)
        }
        data.append(entry)

    return data

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    logger.add("Log/01_SyntheticDataGeneration_Confluence.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('01_SyntheticDataGeneration_Confluence............')
    start_time = time.time()
    data_count = int(input("Enter the number of synthetic data entries to generate: "))
    logger.debug(f'data_count = {data_count}')
    file_name = input("Enter the output file name (including .json extension): ")
    logger.debug(f'file_name = {file_name}')

    synthetic_data = generate_synthetic_data(data_count)
    save_to_file(synthetic_data, file_name)
    logger.debug(f"Synthetic data saved to {file_name}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'01_SyntheticDataGeneration_Confluence elapsed_time = {elapsed_time} sec')