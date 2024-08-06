from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from agents import get_agent_instr

genai = GoogleGenerativeAI(model="models/gemini-1.5-flash")
prompt = ChatPromptTemplate.from_messages([
    ("system","{agent_instr}"),
    ("user","{question}")
])
chain = prompt|genai


def ask_question(agent, query):
    agent_instr = get_agent_instr(agent)
    return chain.invoke({"agent_instr":agent_instr,"question":query})