from langchain.document_loaders import PyPDFLoader
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage,SystemMessage, trim_messages
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from agents import get_agent_instr
import uuid
import os
import streamlit as st

os.environ["GROQ_API_KEY"] == st.secrets["GROQ_API_KEY"]

load_dotenv()

def parse_resume(resume):
    loader = PyPDFLoader(resume.name)
    pages = loader.load()
    resume_text=""
    for page in pages:
        resume_text+=page.page_content + " \n\n"
    return resume_text
model = ChatGroq(model="Gemma2-9b-It")
parser = StrOutputParser()
store={}
trimmer = trim_messages(
    max_tokens=4000,
    strategy="last",
    token_counter=model,
    include_system=True
)

chat_session_id=uuid.uuid4()
models= {"Gemmma-2":"Gemma2-9b-It","Llama-3":"Llama3-8b-8192","Mixtral":"Mixtral-8x7b-32768"}

def create_model(model_key):
    print(model_key)
    print(models.get(model_key))
    #model = ChatGroq(model=models.get(model_key))
    print(model)

def start_new_session():
    chat_session_id=uuid.uuid4()


def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if(session_id not in store):
        store[session_id]=ChatMessageHistory()
    return store[session_id]

with_message_history=None
prompt=None
config=None
chain=None
system_prompt=""

config = {"configurable":{"session_id":chat_session_id}}

def init_interview(resume_file):
    resume_text = parse_resume(resume_file)

    system_prompt=f"""
    I want you to act as an interviewer, start interview and ask the questions based on following resume, focus only on technical, 
    ask one question at a time and not lengthy question, start with basics and gradually deep dive into advanced topics, cover as many as topics possible,
    if use provides not relavent answer move onto other topics mentioned in the resume, strictly limit to 5 questions
    {resume_text}
    """
    #print(system_prompt)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","{system_prompt}"),
            MessagesPlaceholder(variable_name="messages")
        ]
    )
    chain=prompt | trimmer| model | parser
    global with_message_history
    with_message_history=RunnableWithMessageHistory(chain,get_session_history, input_messages_key="messages")
    return with_message_history.invoke({"messages": [HumanMessage(content="")],"system_prompt":system_prompt},config=config)


def submit_answer(user_answer):
    return  with_message_history.invoke({"messages": [HumanMessage(content=user_answer)],"system_prompt":system_prompt},config=config)


