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
        st.write(f"Bienvenue {st.session_state.username}, voici votre examen de vente. Êtes-vous prêt?")
