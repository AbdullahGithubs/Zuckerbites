import streamlit as st  # type: ignore
import base64
import json
import os
from datetime import datetime
import time

st.set_page_config(page_title="Zucker&Salzig bites", page_icon="🍪", initial_sidebar_state="expanded", layout="wide")



REVIEW_FILE = "reviews.json"
if not os.path.exists(REVIEW_FILE):
    with open(REVIEW_FILE, "w") as f:
        json.dump([], f)

# HIDE NAVIGATION AND COLLAPSED ICON
st.markdown("""
<style>
[data-testid="stSidebarNav"], [data-testid="collapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# GET BASE64 IMAGE
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("zuckerbites.sweets.png")

# SIDEBAR LOGO STYLING
st.markdown(""" 
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
""", unsafe_allow_html=True)

st.logo("zucker.jpeg", size="large")  # Optional: Rename image to zucker-salzig.png

# st.markdown("""
#     <style>
#     [data-testid="stSidebar"]{
#         background-color: white;
#     }
#     [data-testid="stAppViewContainer"]{
#         background-color: aliceblue;
#     }
#     header{
#         visibility: hidden;
#     }
#     </style>
# """, unsafe_allow_html=True)

# STYLES: BUTTON + SCROLLBARS
# st.markdown("""
# <style>
# /* Main content scrollbar like ChatGPT */
# div[data-testid="stAppViewContainer"] > .main {
#     overflow-y: auto;
#     scroll-behavior: smooth;
#     scrollbar-width: thin;
#     scrollbar-color: transparent transparent;
#     transition: scrollbar-color 0.3s ease;
# }

# div[data-testid="stAppViewContainer"] > .main:hover {
#     scrollbar-color: #999 #f1f1f1;
# }

# div[data-testid="stAppViewContainer"] > .main::-webkit-scrollbar {
#     width: 6px;
#     background: transparent;
# }

# div[data-testid="stAppViewContainer"] > .main::-webkit-scrollbar-thumb {
#     background-color: transparent;
#     border-radius: 6px;
#     transition: background-color 0.3s ease;
# }

# div[data-testid="stAppViewContainer"] > .main:hover::-webkit-scrollbar-thumb {
#     background-color: #999;
# }

# div[data-testid="stAppViewContainer"] > .main::-webkit-scrollbar-thumb:hover {
#     background-color: #666;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <style>
# .stButton > button {
#     border-radius: 6px;
#     border: 1px solid black;
#     text-align: center !important;
#     background-color: aliceblue;
#     color: brown;
#     font-weight: bold;
#     transition: 0.3s ease;
# }
# .stButton > button:hover {
#     background-color: darkgrey;
#     color: aliceblue;
#     border-radius: 8px;
#     transition: 0.3s ease;
# }
# .stButton > button:active {
#     background-color: bisque;
#     color: aliceblue;
#     border-radius: 8px;
#     transition: 0.3s ease;
# }
# .stAlert {
#     border-left: 4px solid grey;
#     border-radius: 6px;
# }
# </style>
# """, unsafe_allow_html=True)

# SIDEBAR UI
st.sidebar.write("Zucker&Salzig bites – The sweet and savoury haven")
quest = st.sidebar.selectbox("How would you like to contact us", ("Email", "Phone"))
if quest == "Email":
    st.sidebar.success("Our email is zuckerundsalzig@gmail.com")
elif quest == "Phone":
    st.sidebar.success("Our phone number is 03xx xxxx xxx")

# MAIN CONTENT
st.title("Zucker&Salzig bites – The sweet and savoury haven")
st.info("""
At Zucker&Salzig bites, we don’t just make chocolate — we craft moments of joy. Each bite is a bold fusion of rich cocoa, playful creativity, and irresistible flavor...
""")

# GIVEAWAY OVERLAY IMAGE
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
    <div class="text">Zucker&Salzig bites Giveaway</div>
  </div>
</div>
""", unsafe_allow_html=True)

# REVIEWS
st.markdown("### 💬 What Our Customers Say")
st.error("“Zucker&Salzig bites are the best thing that happened to my snack life!” – Ibrahim")
st.info("“Love the packaging and the bold flavors. 10/10!” – Abdullah")
st.success("“Best thing that happened to my life. Makes you say WOW” – Fiza")
st.warning("Great chocolates!")

# SIDEBAR REVIEW
st.sidebar.info("Have you tasted Zucker&Salzig bites? What would you rate it?")
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
            "user": st.session_state.user["name"]
        }
        with open(REVIEW_FILE, "r") as f:
            existing_reviews = json.load(f)
        existing_reviews.append(new_entry)
        with open(REVIEW_FILE, "w") as f:
            json.dump(existing_reviews, f, indent=2)
        st.sidebar.success("Thanks for your feedback! 🍬")
    time.sleep(1)
    st.rerun()

# VIDEO LINK AND EMBED
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

# NAVIGATION
if st.button("Shop Zucker&Salzig bites"):
    st.switch_page("pages/Shop.py")

if st.session_state.get("hide"):
    st.sidebar.markdown("")
elif st.sidebar.button("Log in"):
    st.switch_page("pages/log-in.py")

if st.session_state.get("hide"):
    st.sidebar.markdown("")
elif st.sidebar.button("Sign up"):
    st.switch_page("pages/sign-up.py")
