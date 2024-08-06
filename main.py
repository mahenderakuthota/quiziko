import streamlit as st
from chatbot import init_chat, ask_question,start_new_session,create_model

def start_new_chat():
    st.session_state.messages=[]
    start_new_session()


st.title("Quiziko")

with st.sidebar:
    st.title("Settings")
    ##m_model=st.selectbox("Select LLM Model",["Gemma-2","Llama-3","Mixtral"], on_change=create_new_model)
    agent = st.selectbox("Select AI Agent",["General","English Translator","Spoken English Teacher","Travel Guide","Storyteller", "Interviewer"], on_change=start_new_chat)
    st.button("Start New Chat Session", on_click=start_new_chat)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(placeholder="What is your question?")
if question:
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.markdown(question)
    
    if len(st.session_state.messages) == 1:
       response = init_chat(agent, question)
    else:
       response = ask_question(agent, question)
   
    st.session_state.messages.append({"role":"assistant","content":response})


    with st.chat_message("assistant"):
        st.markdown(response)

