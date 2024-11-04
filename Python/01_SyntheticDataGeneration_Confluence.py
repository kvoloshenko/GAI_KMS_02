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
        "API Reference"
    ]

    descriptions = [
        "This document describes the contents of Moon Flight System 2024.1, March 2024. Purpose: The work completed for this release encompasses the following areas: Enhanced Navigation Algorithms, New User Interfaces, Extended Data Integration, Enhanced Security Features.",
        "The system requirements for Moon Flight System release 2024.1 are described as follows: requires a quad-core processor, 16GB RAM, 250GB SSD, and Internet connectivity.",
        "Deliverables: The server software is distributed in the form of a zip file. For example, in the MFS-2024.1-UNIX.zip file, contains binaries, libraries, and installation scripts.",
        "Installation Instructions: Unzip the MFS-2024.1.zip file, run the installer script with sudo privileges. Follow the prompts to complete the installation process.",
        "API Reference: Moon Flight System offers a comprehensive API with endpoints for mission planning, trajectory calculation, system status, user management, and data retrieval.",
        "System Architecture: The system consists of three major modules: Flight Control, Data Analytics, and User Interaction. Each module is further divided into microservices."
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