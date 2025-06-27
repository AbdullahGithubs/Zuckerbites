import streamlit as st  # type: ignore
import base64
import json
import os
from datetime import datetime

st.set_page_config(page_title="Shifa Illahi Foods", page_icon="🍪", initial_sidebar_state="expanded", layout="wide")

REVIEW_FILE = "reviews.json"

if not os.path.exists(REVIEW_FILE):
    with open(REVIEW_FILE, "w") as f:
        json.dump([], f)

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_image("zuckerbites.sweets.png")



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

st.markdown(""" 
    <body>
<style>
  div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
      height: 7rem;
      width: auto;
  }
  
  div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
  div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
      display: flex;
      align-items: center;
  }
</style>
</body>
""", unsafe_allow_html=True)

st.logo("shifa (1).png", size="large")

st.sidebar.write("Shifa Illahi Foods - The Sweet and savoury haven")

quest = st.sidebar.selectbox("How would you like to contact us", ("Email", "Phone"))

if quest == "Email":
    st.sidebar.success("Our email is shifaillahi@gmail.com")
elif quest == "Phone":
    st.sidebar.success("Our phone number is 03xx xxxx xxx")  

st.title("Shifa Illahi Foods - The Sweet and savoury haven")
st.info("""
At Shifa Illahi, we don’t just make chocolate — we craft moments of joy. Each bite is a bold fusion of rich cocoa, playful creativity, and irresistible flavor. Whether you're a classic dark lover or a daring flavor explorer, Shifa Illahi Foods brings a spark of delight to every craving.

Rooted in quality and driven by passion, we use ethically-sourced ingredients and small-batch craftsmanship to ensure every bar, truffle, and bite-sized treat is as unforgettable as it is delicious.

Treat yourself. Share the joy. Join the chocolate revolution — only at Shifa Illahi Foods.""")

st.markdown(f"""
<style>
.container {{
  position: relative;
  width: 400px;
  margin: 20px auto;
}}
.image {{
  width: 100%;
  height: 60%;
  display: block;
  border-radius: 8px;
}}
.overlay {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.6);
  opacity: 0;
  transition: 0.3s ease;
  border-radius: 8px;
}}
.container:hover .overlay {{
  opacity: 1;
}}
.text {{
  color: white;
  font-size: 16px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}}
</style>

<div class="container">
  <img src="data:image/png;base64,{img_base64}" class="image">
  <div class="overlay">
    <div class="text">Shifa Illahi Foods Giveaway</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 💬 What Our Customers Say")
st.error("“Shifa Illahi Foods is the best thing that happened to my snack life!” – Ibrahim")
st.info("“Love the packaging and the bold flavors. 10/10!” – Abdullah")
st.success("“Best thing that happened to my life. Makes you say WOW” – Fiza")
st.warning("Great chocolates!")

st.sidebar.info("Have you tasted Shifa Illahi Foods? What would you rate it?")
st.sidebar.feedback("stars")

review = st.sidebar.text_input("And don't forget to write a review...")

submit = st.sidebar.button("Submit")

if submit:
    if not st.session_state.get("logged_in"):
        st.sidebar.warning("Please log in before submitting a review.")
    elif not review.strip():
        st.sidebar.error("Please don't leave it blank.")
    else:
        new_entry = {
            "review": review.strip(),
            "timestamp": datetime.now().isoformat(),
            "user": st.session_state.user["name"]  # Optional: attach user's name
        }
        with open(REVIEW_FILE, "r") as f:
            existing_reviews = json.load(f)
        existing_reviews.append(new_entry)
        with open(REVIEW_FILE, "w") as f:
            json.dump(existing_reviews, f, indent=2)
        st.sidebar.success("Thanks for your feedback! 🍬")

st.sidebar.markdown("""
<a href="https://www.youtube.com/watch?v=wK5JH9fpaMs" target="_blank">
    <button style="
        background-color: #FF0000;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
    ">🎬 Watch on YouTube</button>
</a>
""", unsafe_allow_html=True)

st.sidebar.subheader("----------  Or just watch it here!  ----------")
st.sidebar.video("https://www.youtube.com/watch?v=wK5JH9fpaMs")

if st.button("Shop Shifa Illahi Foods"):
    st.switch_page("pages/Shop.py")

if st.session_state.get("hide"):
    st.sidebar.markdown("")
elif st.sidebar.button("Log in"):
    st.switch_page("pages/log-in.py")

if st.session_state.get("hide"):
    st.sidebar.markdown("")
elif st.sidebar.button("Sign up"):
    st.switch_page("pages/sign-up.py")
