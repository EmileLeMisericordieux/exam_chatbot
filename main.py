from openai import OpenAI
import streamlit as st
from instructions import context
from helper_functions import log_in

st.title("Examen de vente")

log_in()

if st.session_state.logged_in:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "o4-mini-2025-04-16"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Que voulez-vous dire?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=
                    [{
                    "role": "system",
                    "content": [
                        {
                        "type": "text",
                        "text": context
                        }
                    ]
                    }] +
                    [{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages]
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
        st.session_state.messages.append({"role": "assistant", "content": response})
