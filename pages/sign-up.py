import streamlit as st # type: ignore
import json
import os
import hashlib
from cryptography.fernet import Fernet # type: ignore

st.set_page_config(page_title="Sign up", page_icon="📝", initial_sidebar_state="collapsed", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Create Account")

# Input fields
name = st.text_input("Name")
phone = st.text_input("Phone Number")
password = st.text_input("Password", type="password")
location = st.text_input("Location")

# Password & phone hash functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# def hash_phone(phone):
#     return hashlib.sha256(phone.encode()).hexdigest()

# --- ENCRYPTION SETUP ---
KEY_FILE = "secret.key"
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

fernet = Fernet(key)

def encrypt_location(location):
    return fernet.encrypt(location.encode()).decode()
def encrypt_phone(phone):
    return fernet.encrypt(phone.encode()).decode()

ACCOUNTS_FILE = "accounts.json"

# Load existing accounts
if os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, "r") as f:
        accounts = json.load(f)
else:
    accounts = []

# Account creation
if st.button("Submit"):
    if not name or not phone or not password or not location:
        st.error("All fields are required.")
    elif any(acc for acc in accounts if acc.get("phone") == encrypt_phone(phone)):
        st.error("An account with this phone number already exists.")
    else:
        new_account = {
            "name": name,
            "phone": encrypt_phone(phone),
            "password": hash_password(password),
            "location": encrypt_location(location)
        }
        accounts.append(new_account)

        with open(ACCOUNTS_FILE, "w") as f:
            json.dump(accounts, f, indent=2)

        st.success("Account created successfully!")

def go_to_login():
    st.session_state.go_to_login = True

st.button("Log in instead", on_click=go_to_login)

if st.session_state.get("go_to_login"):
    st.session_state.go_to_login = False 
    st.switch_page("pages/log-in.py")
