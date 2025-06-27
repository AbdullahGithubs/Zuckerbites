import streamlit as st # type: ignore
import json
import os
import hashlib
from cryptography.fernet import Fernet # type: ignore
import time

st.set_page_config(page_title="Log in", page_icon="🔑", initial_sidebar_state="collapsed", layout="wide")
st.title("Log in")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hide():
    st.session_state.hide = True

KEY_FILE = "secret.key"
with open(KEY_FILE, "rb") as f:
    key = f.read()

fernet = Fernet(key)

def decrypt_data(data):
    return fernet.decrypt(data.encode()).decode()

name = st.text_input("Name")
phone = st.text_input("Phone Number")
password = st.text_input("Password", type="password")

ACCOUNTS_FILE = "accounts.json"

if st.button("Submit"):
    if not os.path.exists(ACCOUNTS_FILE):
        st.error("No accounts found. Please create one first.")
    else:
        with open(ACCOUNTS_FILE, "r") as f:
            accounts = json.load(f)

        hashed_password = hash_password(password)
        matched = None

        for acc in accounts:
            try:
                decrypted_phone = decrypt_data(acc["phone"])
                if acc.get("name") == name and acc["password"] == hashed_password and decrypted_phone == phone:
                    matched = acc
                    break
            except:
                continue

        if matched:
            st.session_state.logged_in = True
            st.session_state.user = matched
            hide()
            decrypted_location = decrypt_data(matched["location"])
            st.success(f"Welcome back, {matched['name']}!")
            st.info(f"Your saved location is: {decrypted_location}")
            time.sleep(1)
            st.switch_page("Home.py")
        else:
            st.error("Invalid name, password, or phone number")

if st.button("Create Account Instead"):
    st.session_state.go_to_signup = True

if st.session_state.get("go_to_signup"):
    st.session_state.go_to_signup = False
    st.switch_page("pages/Sign-up.py")