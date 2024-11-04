# Importing necessary libraries and modules
from loguru import logger # Import logger for logging purposes
import time               # Import time module to track execution time
from langchain_community.tools import DuckDuckGoSearchRun # Import DuckDuckGoSearchRun for performing web searches

# Create an instance of DuckDuckGoSearchRun for performing web queries
search = DuckDuckGoSearchRun()

if __name__ == "__main__":
    # Configure the logger to write logs to a file with specific settings
    logger.add("Log/24_WebSearch.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('24_WebSearch............')
    # Record the starting time to measure the elapsed time of the search process
    start_time = time.time()

    # Define the search query for DuckDuckGo
    search_query = 'Describe how to use Sy policy in 5g'

    # Execute the search query using the DuckDuckGoSearchRun instance
    search_results = search.run(search_query)
    logger.debug(f'search_results={search_results}')

    # Record the ending time and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'24_WebSearch elapsed_time = {elapsed_time} sec')