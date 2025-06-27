from cryptography.fernet import Fernet
import streamlit as st
import json

# Load the encryption key
with open("secret.key", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# Load accounts
with open("accounts.json", "r") as f:
    accounts = json.load(f)

user_names = [acc.get("name") for acc in accounts if acc.get("name")]
selected_name = st.selectbox("Select user to view info:", user_names)

user = next(acc for acc in accounts if acc.get("name") == selected_name)

try:
    encrypted_location = user.get("location")
    if encrypted_location:
        decrypted_location = fernet.decrypt(encrypted_location.encode()).decode()
        st.success(f"Decrypted location: {decrypted_location}")
    else:
        st.warning("No location stored.")
except Exception as e:
    st.error("Error decrypting location: " + str(e))

# Decrypt phone
try:
    encrypted_phone = user.get("phone")
    if encrypted_phone:
        decrypted_phone = fernet.decrypt(encrypted_phone.encode()).decode()
        st.info(f"Decrypted phone: {decrypted_phone}")
    else:
        st.warning("No phone stored.")
except Exception as e:
    st.error("Error decrypting phone: " + str(e))
