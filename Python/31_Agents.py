import time
from loguru import logger                                   # Import logger for logging
import AI_Tools as tls                                      # Import custom AI tools package
from langchain.tools.retriever import create_retriever_tool # Import for creating retriever tools
from typing import Annotated, Sequence, TypedDict           # Import typing utilities
from langchain_core.messages import BaseMessage             # Import base message class
from langgraph.graph.message import add_messages            # Import message handling for the graph

# Load existing Vector Knowledge Bases for Jira, Confluence and Git
jira_db_file_name = './Db/DB_Jira'
jira_db = tls.load_db(jira_db_file_name, tls.embeddings)
confluence_db_file_name = './Db/DB_Confluence'
confluence_db = tls.load_db(confluence_db_file_name, tls.embeddings)
# Load the existing Vector Knowledge Base using custom tools (tls)
git_db_file_name = './Db/Git_Kind_Doctor'
git_db = tls.load_db(git_db_file_name, tls.embeddings)

# Create retrievers for Jira, Confluence and Git
retriever_jira = jira_db.as_retriever()
retriever_confluence = confluence_db.as_retriever()
retriever_git = git_db.as_retriever()

# Create tools for retrieval using the retrievers
jira_retriever_tool = create_retriever_tool(
    retriever_jira,
    "retrieve_jira_tickets",
    "Search and return information about Jira tickets on Summary, Ticket key, Ticket id, "
    "Ticket Type, Status, Project key, Project name, Project type, Project lead and Project description.",
)

confluence_retriever_tool = create_retriever_tool(
    retriever_confluence,
    "retrieve_confluence",
    "Search and return information from Confluence on products documentations.",
)

git_retriever_tool = create_retriever_tool(
    retriever_git,
    "retriever_git",
    "Search and return information from Git on components' and programs' source code.",
)


# List of tools available for the agent to use
tools = [jira_retriever_tool, confluence_retriever_tool, git_retriever_tool]

# Define AgentState type
class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Import necessary modules for nodes and edges
from typing import Annotated, Literal, Sequence, TypedDict
from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import tools_condition

### Edges

# Function to grade documents' relevance to the question
def grade_documents(state) -> Literal["generate", "rewrite"]:
    logger.debug(f'grade_documents............')
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """

    logger.debug("---CHECK RELEVANCE---")

    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    # Load the model and chain with the prompt
    model = ChatOpenAI(temperature=0, model="gpt-4o", streaming=True)

    # LLM with tool and validation
    llm_with_tool = model.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    # Chain
    chain = prompt | llm_with_tool

    messages = state["messages"]
    last_message = messages[-1]

    question = messages[0].content
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})

    score = scored_result.binary_score

    if score == "yes":
        logger.debug("---DECISION: DOCS RELEVANT---")
        return "generate"

    else:
        logger.debug("---DECISION: DOCS NOT RELEVANT---")
        logger.debug(score)
        return "rewrite"


### Nodes

# Function for the agent node
def agent(state):
    logger.debug(f'agent............')
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    print("---CALL AGENT---")
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4o")
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Function to rewrite a query for better understanding
def rewrite(state):
    logger.debug(f'rewrite............')
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    logger.debug("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f""" \n
    Look at the input and try to reason about the underlying semantic intent / meaning. \n
    Here is the initial question:
    \n ------- \n
    {question}
    \n ------- \n
    Formulate an improved question: """,
        )
    ]

    # Grader
    model = ChatOpenAI(temperature=0, model="gpt-4o", streaming=True)
    response = model.invoke(msg)
    return {"messages": [response]}

# Function to generate an answer based on the documents
def generate(state):
    logger.debug(f'generate............')
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
         dict: The updated state with re-phrased question
    """
    logger.debug("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]

    docs = last_message.content

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")

    # LLM
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, streaming=True)

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [response]}


logger.debug("*" * 20 + "Prompt[rlm/rag-prompt]" + "*" * 20)
prompt = hub.pull("rlm/rag-prompt").pretty_print()  # Show what the prompt looks like

from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode

# Define a new graph for the agent workflow
workflow = StateGraph(AgentState)

# Define the nodes we will cycle between
workflow.add_node("agent", agent)        # agent
retrieve = ToolNode([jira_retriever_tool, confluence_retriever_tool, git_retriever_tool ])
workflow.add_node("retrieve", retrieve)  # retrieval
workflow.add_node("rewrite", rewrite)    # Re-writing the question
workflow.add_node(
    "generate", generate
)  # Generating a response after we know the documents are relevant
# Call agent node to decide to retrieve or not
workflow.add_edge(START, "agent")

# Decide whether to retrieve
workflow.add_conditional_edges(
    "agent",
    # Assess agent decision
    tools_condition,
    {
        # Translate the condition outputs to nodes in our graph
        "tools": "retrieve",
        END: END,
    },
)

# Edges taken after the `action` node is called.
workflow.add_conditional_edges(
    "retrieve",
    # Assess agent decision
    grade_documents,
)
workflow.add_edge("generate", END)
workflow.add_edge("rewrite", "agent")

# Compile the graph
graph = workflow.compile()

# TODO
# from IPython.display import Image, display
# # Display the compiled graph
# try:
#     display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass

import pprint
def ask_agent(question):
  # Function to ask a question to the agent
  logger.debug('ask_agent............')
  response = 'Stub for the response'
  start_time = time.time()
  logger.debug(f'question = {question}')
  inputs = {
    "messages": [
        ("user", question),
    ]
  }
  for output in graph.stream(inputs, {"recursion_limit": 30}):
    for key, value in output.items():
        pprint.pprint(f"Output from node '{key}':")
        pprint.pprint("---")
        pprint.pprint(value, indent=2, width=80, depth=None)
        response = value
    pprint.pprint("---END---")

  end_time = time.time()
  elapsed_time = end_time - start_time
  logger.debug(f'ask_agent elapsed_time = {elapsed_time} sec')
  return response



if __name__ == "__main__":
    logger.add("Log/31_Agents.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('31_Agents............')
    # Ask a question related to Jira to the agent
    response = ask_agent("Give me tickets related to Moon Flight System. I need Ticket id, Summary and Project name.")
    logger.debug(response)

    # Ask a question related to Confluence to the agent
    response = ask_agent("How to install Moon Flight System? Give me the main details")
    logger.debug(response)

    # Ask a question related to Git to the agent
    response = ask_agent("I'm looking for where in the source code was defined the file name where is the prompt")
    logger.debug(response)


