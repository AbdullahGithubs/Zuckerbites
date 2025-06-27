import streamlit as st # type: ignore
import json
from datetime import datetime
from cryptography.fernet import Fernet  # type: ignore
import time

st.set_page_config(page_title="Checkout", page_icon="🧾", initial_sidebar_state="collapsed", layout="wide")

st.title("🧾 Checkout")

initial_status = False

with open("secret.key", "rb") as f:
    key = f.read()

fernet = Fernet(key)

if "cart" not in st.session_state:
    st.session_state.cart = []

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    if st.button("🔑 Log in to autofill"):
        st.session_state.go_to_login = True
        st.switch_page("pages/log-in.py")

if st.session_state.get("go_to_login"):
    st.session_state.go_to_login = False
    st.switch_page("pages/log-in.py")

if st.session_state.cart:
    st.subheader("Your Cart:")
    total = 0
    for item in st.session_state.cart:
        st.markdown(f"- **{item['title']}** — Rs. {item['price']}")
        total += item["price"]
    st.markdown(f"### 🧮 Total: Rs. {total}")

    st.subheader("Billing Info")

    autofill_name = st.session_state.user["name"] if st.session_state.get("logged_in") else ""
    autofill_phone = st.session_state.user["phone"] if st.session_state.get("logged_in") else ""

    autofill_address = ""
    if st.session_state.get("logged_in"):
        try:
            encrypted_address = st.session_state.user.get("location", "")
            autofill_address = fernet.decrypt(encrypted_address.encode()).decode()
        except Exception as e:
            st.error(f"Could not decrypt address: {e}")
        try:
            encrypted_phone = st.session_state.user.get("phone", "")
            autofill_phone = fernet.decrypt(encrypted_phone.encode()).decode()
        except Exception as e:
            st.error(f"Could not decrypt phone: {e}")
    name = st.text_input("Name", value=autofill_name)
    phone = st.text_input("Phone Number", value=autofill_phone)
    address = st.text_area("Delivery Address", value=autofill_address)

    if st.button("✅ Confirm Order & Save"):
        if name and phone and address:
            order = {
                "name": name,
                "phone": phone,
                "address": address,
                "items": st.session_state.cart,
                "total": total,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            initial_status = True
            st.session_state.cart = []
            st.session_state.cart_confirmed = False
            filename = f"order_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(order, f, indent=2)
            st.success(f"🎉 Order saved as `{filename}`!")
        else:
            st.warning("Please complete all fields before confirming.")
else:
    st.warning("🛒 Your cart is empty. Go back to the Shop page to add items.")

if initial_status:
    time.sleep(1)
    st.rerun()