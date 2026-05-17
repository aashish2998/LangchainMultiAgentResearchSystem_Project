from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
import os
from dotenv import load_dotenv

load_dotenv()


#Model Initialisation
# gemini = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=0,
#     google_api_key=os.getenv("GEMINI_API_KEY")
# )

# groq = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0,
#     api_key=os.getenv("GROQ_API_KEY")
# )

# llm = gemini.with_fallbacks([groq])

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

#First Agent creation

def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search]

    )

# Second Agent creation 
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [web_search]

    )


# writer chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()



#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()