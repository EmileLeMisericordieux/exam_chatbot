from openai import OpenAI
import streamlit as st


def authenticate(username, password):
    return username in st.secrets["credentials"] and st.secrets["credentials"][username] == password

def log_in():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'username' not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    else:
        st.write(f"Bienvenue {st.session_state.username}, voici votre examen de vente. Le téléphone de votre bureau sonne. Répondez ci-bas!")

def restart_chat():
    st.session_state.messages = []

def evaluate(evaluator_context, messages):
    evaluator = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    stream = evaluator.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=
            [{
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": evaluator_context
                }
            ]
            }] +
            [{
            "role": "user",
            "content": f"Dis-moi comment j'ai performé dans cette intéraction avec un client: {messages}"
            }]
        ,
        response_format={
            "type": "text"
        },
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True
    )
    response = st.write_stream(stream)
    return response
