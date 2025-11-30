import chainlit as cl
from agent import get_agent_executor
from langchain_core.messages import HumanMessage, AIMessage

@cl.on_chat_start
async def on_chat_start():
    agent_executor = get_agent_executor()
    cl.user_session.set("agent", agent_executor)
    cl.user_session.set("chat_history", [])
    
    # --- Feature Guide (Side View) ---
    guide = """
# 🚀 Parthiban's AI Agent

**Author:** *Parthiban K – Java Full Stack & AI/ML Engineer*  
**Project:** Intelligent Research & Market Insights Agent

---

## 🧩 Tech Stack

- 🧠 **LLM Orchestration:** LangChain
- 💬 **Frontend Chat UI:** Chainlit
- 🔑 **Model Provider:** OpenAI
- 📊 **Market Data:** Alpha Vantage
- 🌐 **Web Research:** Tavily Search
- 📚 **Knowledge Base:** Wikipedia + LLM reasoning

---

## 🌟 What This Agent Can Do

### 📈 Market & Stock Intelligence
- Get near real-time stock prices and key metrics.
- Ask for trend explanations and concise summaries.

### 🌐 Deep Web & Knowledge Research
- Research any topic using web search + Wikipedia.
- Get structured answers, overviews, and follow-ups.

### 🧠 Contextual Multi-Turn Chat
- Remembers previous questions in this session.
- Builds on your previous queries for better answers.

---

> 🔧 *Built with care by **Parthiban** to explore real-world agentic AI workflows.*
"""

    # Send the side view element (fixed to side)
    await cl.Message(
        content="",
        elements=[
            cl.Text(
                name="🔍 Feature Guide",
                content=guide,
                display="side"
            )
        ],
    ).send()

    # --- Main Welcome Message ---
    welcome_message = """
# 👋 Hey Guys, your AI Agent is online!

Welcome to your **personal AI Research & Market Insights Agent**.  
This assistant combines **LangChain**, **OpenAI**, and multiple tools to help you experiment with real agentic workflows.

---

## 🧭 What I Can Help You With

1. 📊 **Stocks & Market Data**
   - _Example_: `How is AAPL performing today?`
   - _Example_: `Compare Tesla and Nvidia over the last year.`
   - _Example_: `Show me the trend for Microsoft (MSFT) with a chart.`

2. 🌍 **Topic & Web Research**
   - _Example_: `Give me the latest developments in Generative AI.`
   - _Example_: `Summarize recent trends in Indian stock market regulation.`

3. 📚 **General Knowledge & Explanations**
   - _Example_: `Ex plain RAG in simple terms.`
   - _Example_: `Who invented the transistor and why is it important?`

---

## 🧑‍💻 About This Project

- **Owner:** *Parthiban K*
- **Role:** Java Full Stack Developer & AI/ML Enthusiast  
- **Goal:** Practice building **agentic AI systems** with:
  - Multi-tool agents (stocks, web search, wiki)
  - Conversation memory
  - Clean Chainlit UI for demos & interviews

---

💡 **Tip:**  
Start with a message like:

> `Analyze the stock performance of Apple (AAPL). I want to see the price chart and a summary of its recent market movements.`

I’ll take it from there 🚀
"""

    await cl.Message(content=welcome_message).send()


@cl.on_message
async def on_message(message: cl.Message):
    agent_executor = cl.user_session.get("agent")
    chat_history = cl.user_session.get("chat_history")

    # Run the agent with Langchain callback (for nice traces in Chainlit)
    res = await agent_executor.ainvoke(
        {"input": message.content, "chat_history": chat_history},
        config={"callbacks": [cl.LangchainCallbackHandler()]}
    )
    
    answer = res["output"]

    # Update in-memory chat history for contextual responses
    chat_history.append(HumanMessage(content=message.content))
    chat_history.append(AIMessage(content=answer))
    cl.user_session.set("chat_history", chat_history)

    await cl.Message(content=answer).send()
