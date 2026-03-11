import streamlit as st
import numpy as np
import pickle

# Load model
model = pickle.load(open('bigmart_model.pkl', 'rb'))

st.set_page_config(page_title="Big Mart Sales Predictor", layout="wide")

# -------------------- PREMIUM CSS --------------------
st.markdown("""
<style>

/* Full app background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}


/* Remove top white space */
header {visibility: hidden;}

/* Glass card style */
.glass {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 20px;
}

/* Section titles */
.section-title {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 15px;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white;
    font-size: 22px;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    border: none;
    transition: 0.3s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(45deg, #ff4b2b, #ff416c);
}

/* Prediction result card */
.result-box {
    background: linear-gradient(45deg, #00b09b, #96c93d);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
}

h1 {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 28px;
    margin-bottom: 30px;
    opacity: 0.8;
}


</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("<h1>🛒 Big Mart Sales Prediction</h1>", unsafe_allow_html=True)


# -------------------- LAYOUT --------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📦 Product Details</div>", unsafe_allow_html=True)

    Item_Weight = st.number_input("Item Weight", min_value=0.0)
    Item_Visibility = st.number_input("Item Visibility", min_value=0.0)
    Item_MRP = st.number_input("Item MRP", min_value=0.0)

    Item_Fat_Content = st.selectbox("Item Fat Content", ["Low Fat", "Regular"])

    Item_Type = st.selectbox("Item Type", [
        "Dairy", "Soft Drinks", "Meat", "Fruits and Vegetables",
        "Household", "Baking Goods", "Snack Foods",
        "Frozen Foods", "Breakfast", "Health and Hygiene",
        "Hard Drinks", "Canned", "Breads",
        "Starchy Foods", "Others"
    ])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🏪 Outlet Details</div>", unsafe_allow_html=True)

    Outlet_Establishment_Year = st.number_input("Outlet Establishment Year", min_value=1900)
    Outlet_Size = st.selectbox("Outlet Size", ["Small", "Medium", "High"])
    Outlet_Location_Type = st.selectbox("Outlet Location Type", ["Tier 1", "Tier 2", "Tier 3"])
    Outlet_Type = st.selectbox("Outlet Type", [
        "Grocery Store", "Supermarket Type1",
        "Supermarket Type2", "Supermarket Type3"
    ])
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Encoding --------------------
fat_map = {"Low Fat": 0, "Regular": 1}

type_map = {name: idx for idx, name in enumerate([
    "Dairy", "Soft Drinks", "Meat", "Fruits and Vegetables",
    "Household", "Baking Goods", "Snack Foods",
    "Frozen Foods", "Breakfast", "Health and Hygiene",
    "Hard Drinks", "Canned", "Breads",
    "Starchy Foods", "Others"
])}

size_map = {"Small": 0, "Medium": 1, "High": 2}
location_map = {"Tier 1": 0, "Tier 2": 1, "Tier 3": 2}
outlet_type_map = {
    "Grocery Store": 0,
    "Supermarket Type1": 1,
    "Supermarket Type2": 2,
    "Supermarket Type3": 3
}

Item_Identifier = 0
Outlet_Identifier = 0

# -------------------- Prediction --------------------
if st.button("🔮 Predict Sales"):

    input_data = np.array([[
        Item_Identifier,
        Item_Weight,
        fat_map[Item_Fat_Content],
        Item_Visibility,
        type_map[Item_Type],
        Item_MRP,
        Outlet_Identifier,
        Outlet_Establishment_Year,
        size_map[Outlet_Size],
        location_map[Outlet_Location_Type],
        outlet_type_map[Outlet_Type]
    ]])

    prediction = model.predict(input_data)

    st.markdown(
        f"<div class='result-box'>💰 Predicted Sales: ₹ {prediction[0]:,.2f}</div>",
        unsafe_allow_html=True
    )

