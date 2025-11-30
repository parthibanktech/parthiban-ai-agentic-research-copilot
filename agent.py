from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import get_tools
import os

def get_agent_executor():
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Get tools
    tools = get_tools()

    # Define the prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI assistant. You have access to several tools to help you answer questions. "
                       "If a tool fails, please report the error and try to answer as best as you can or ask for clarification. "
                       "Always check the stock price using the get_stock_price tool if asked about stocks."),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create the executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    return agent_executor
