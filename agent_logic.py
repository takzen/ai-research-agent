# agent_logic.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

def create_agent_executor():
    """
    Creates and returns an AI agent executor capable of researching topics online.
    """
    # 1. Initialize the LLM (Gemini 1.5 Pro)
    # The API key is automatically read from the GOOGLE_API_KEY environment variable
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

    # 2. Define the tools the agent can use
    # The Tavily API key is automatically read from the TAVILY_API_KEY env variable
    search_tool = TavilySearchResults(max_results=3)
    tools = [search_tool]

    # 3. Create the prompt template
    # This defines the agent's persona and instructions
    prompt_template = """
    You are an expert researcher. Your goal is to provide a comprehensive, well-structured report on a given topic.
    You have access to a powerful internet search tool.

    Follow these steps:
    1.  First, think about a plan to answer the user's question. Formulate a series of search queries you will need to perform.
    2.  Execute the search queries using your tool.
    3.  Analyze the search results and synthesize the information.
    4.  Finally, generate a detailed, well-organized report that directly answers the user's question.
    
    Provide only the final report in your answer.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_template),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 4. Create the agent "brain"
    # This binds the LLM, tools, and prompt together
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 5. Create the agent executor
    # This is the runtime that makes the agent work
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True, # Set to True to see the agent's thought process in the terminal
        handle_parsing_errors=True # Helps with robustness
    )
    
    return agent_executor