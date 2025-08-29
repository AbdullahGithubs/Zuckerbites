import streamlit as st # type: ignore
import base64
import time

st.set_page_config(
page_title="Shop",
page_icon="🍪",
initial_sidebar_state="expanded",
layout="wide"
)

def toast(x):
    st.markdown(f"""
    <style>
    .toast {{
    position: fixed;
    top: 80px; /* below the top navbar */
    right: 20px; /* aligned to the right */
    width: auto;
    max-width: 400px;
    padding: 16px 24px;
    background-color: #4CAF50;
    color: white;
    font-weight: 500;
    font-size: 16px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 9999;
    animation: fadeout 3s ease-in-out forwards;
    }}
    @keyframes fadeout {{
        0%   {{ opacity: 1; }}
        85%  {{ opacity: 1; }}
        100% {{ opacity: 0; }}
    }}
    </style>

    <div class="toast">{x}</div>
    """, unsafe_allow_html=True)


initial_status = False

st.markdown("""
<style>
.stButton > button {
    border-radius: 6px;
    border: 1px solid black;
    text-align: center !important;
    background-color: aliceblue;
    color: brown;
    font-weight: bold;
    transition: 0.3s ease;
}
.stButton > button:hover {
    background-color: darkgrey;
    color: aliceblue;
    border-radius: 8px;
    transition: 0.3s ease;
}
.stButton > button:active {
    background-color: bisque;
    color: aliceblue;
    border-radius: 8px;
    transition: 0.3s ease;
}
.stAlert {
    border-left: 4px solid grey;
    border-radius: 6px;
}

</style>
""", unsafe_allow_html=True)

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

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "cart_confirmed" not in st.session_state:
    st.session_state.cart_confirmed = False

products = [
    {
        "id": "oreo",
        "data": get_base64_image("rite.png"),
        "title": "Chocolate Oreo Sandwich",
        "description": "Rich Chocolate Oreo Sandwich With Vanilla Cream",
        "price": 250
    },
    {
        "id": "date",
        "data": get_base64_image("date.png"),
        "title": "Chocolate Glazed Dates",
        "description": "Chocolate Wrapped Delicious Date, With White Chocolate Topping",
        "price": 300
    },
    {
        "id": "shell",
        "data": get_base64_image("shell.png"),
        "title": "Shell Shaped Delights",
        "description": "Beautiful Shell Shaped Dark Chocolate With Luxurious Taste",
        "price": 220
    },
    {
        "id": "coconut",
        "data": get_base64_image("coconut.png"),
        "title": "Cocnut glazed Dates",
        "description": "Rich Soft Brown Chocolate With Exquisite Taste, Littered With Grazed Coconut",
        "price": 280
    },
    {
        "id": "easteregg",
        "data": get_base64_image("easteregg.png"),
        "title": "Easteregg of chocolate",
        "description": "A choco egg packed with colorful Smarties inside — crack it, crunch it, love it",
        "price": 280
    },
    {
        "id": "oreocoated",
        "data": get_base64_image("oreocoated.png"),
        "title": "Coated vanilla sandwich",
        "description": "Rich vanilla cream sandwich coated with dark and white chocolate, perfect for any parties",
        "price": 280
    },
    {
        "id": "nuts",
        "data": get_base64_image("nuts'n'dryfruits.png"),
        "title": "Nuts and dryfruits giftpack",
        "description": "A bag of dryfruits and crunchy nuts readymade",
        "price": 280
    },
    {
        "id": "heart",
        "data": get_base64_image("heart.png"),
        "title": "Heart Chocolate",
        "description": "Soft brown chocolate in the shape of a heart. Delightfully smooth and irresistibly indulgent.",
        "price": 280
    },
    {
        "id": "wal'nut'",
        "data": get_base64_image("wal'nut'.png"),
        "title": "Walnut tarts",
        "description": "Golden tarts filled with roasted walnuts, offering a rich, nutty flavor",
        "price": 280
    },
    {
        "id": "chapli",
        "data": get_base64_image("chaplia.png"),
        "title": "Beef chapli kabab burger",
        "description": "Well seasoned beef chapli kabab burger with a side of fries, coleslaw and a sweetbowl",
        "price": 280
    },
    {
        "id": "biscuits'",
        "data": get_base64_image("chapli.png"),
        "title": "Coffee'n'Walnut biscuits",
        "description": "Heavenly biscuits filled with a mix of coffee and walnuts",
        "price": 280
    },
]

st.markdown("""
<style>
.container {
  position: relative;
  width: 50%;
  margin: 20px auto;
  padding-bottom: 20px;
  border-bottom: 1px solid #ccc;
}
.image {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.6);
  opacity: 0;
  transition: 0.3s ease;
  border-radius: 8px;
}
.container:hover .overlay {
  opacity: 1;
}
.text {
  color: white;
  font-size: 16px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.details {
  margin-top: 10px;
  text-align: center;
}
.price {
  color: #27ae60;
  font-weight: bold;
  margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🛒 Your Cart")
if st.session_state.cart:
    total = 0
    for item in st.session_state.cart:
        st.sidebar.write(f"{item['title']} - Rs. {item['price']}")
        total += item['price']
    st.sidebar.markdown(f"**Total: Rs. {total}**")
    if st.sidebar.button("🧹Clear Cart"):
        initial_status = True
        st.session_state.cart = []
        st.session_state.cart_confirmed = False
else:
    st.sidebar.write("Your cart is empty.")

for product in products:
    st.markdown(f"""
    <div class="container">
        <img src="data:image/png;base64,{product['data']}" class="image">
        <div class="overlay">
            <div class="text">{product['description']}</div>
        </div>
        <div class="details">
            <h4>{product['title']}</h4>
            <div class="price">Rs. {product['price']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    col = st.columns([1])[0]
    with col2:
        button_key = f"add_{product['id']}"
        add_clicked = st.button("Add to Cart", key=button_key)
        
        if add_clicked:
            if st.session_state.cart_confirmed:
                with col:
                    st.error("Cart has already been confirmed — you cannot add more items.")
            else:
                st.session_state.cart.append({
                    "id": product["id"],
                    "title": product["title"],
                    "price": product["price"]
                })
                initial_status = True
                toast(f"Adding {product['title']} to cart")

confirm_clicked = st.button("✅ Confirm Cart")
if confirm_clicked:
    if st.session_state.cart:
        st.session_state.cart_confirmed = True
        toast("Cart confirmed!")
    else:
        st.warning("Your cart is empty. Please add items before confirming.")

if st.session_state.cart_confirmed:
    st.page_link("pages/Checkout.py", label="🧾 Go to Checkout")
else:
    st.warning("✅ Please confirm your cart before proceeding to checkout.")

if initial_status:
    time.sleep(1)
    st.rerun()
