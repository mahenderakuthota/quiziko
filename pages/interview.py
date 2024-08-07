import streamlit as st
import interview.bot as ibot

if "messages" not in st.session_state:
    st.session_state.messages = []

resume_file = st.file_uploader("Upload Resume", type="pdf")
first_question=""

if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False

if resume_file is not None and not st.session_state['initialized']:
    with open(resume_file.name, mode='wb') as w:
            w.write(resume_file.getvalue())
            first_question = ibot.init_interview(w)
            print(f"first question : {first_question}")
            st.session_state.messages.append({"role":"assistant","content":first_question})
            st.session_state['initialized'] = True



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(placeholder="Provice Answer")
if question:
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.markdown(question)
    
    if len(st.session_state.messages) > 1:
       response = ibot.submit_answer(question)
       print(f'next question : {response}')
       st.session_state.messages.append({"role":"assistant","content":response})
       with st.chat_message("assistant"):
            st.markdown(response)

