
import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Price Predictor", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.title {
    font-size: 45px;
    font-weight: 800;
    background: linear-gradient(90deg, #00d4ff, #00ffa6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.section {
    background: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #2a2f3a;
}

.result {
    background: linear-gradient(135deg, #00d4ff, #00ffa6);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: black;
    font-weight: bold;
}

button[kind="primary"] {
    background-color: #00d4ff;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
with open('df.pkl','rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)

# ---------------- HEADER ----------------
st.markdown('<p class="title"> Property Price Predictor</p>', unsafe_allow_html=True)
st.write("### Fill property details below")

# ---------------- SECTION 1 ----------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Basic Details")

col1, col2, col3 = st.columns(3)

with col1:
    property_type = st.selectbox('Property Type',['flat','house'])
    sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

with col2:
    bedrooms = float(st.selectbox('Bedrooms',sorted(df['bedRoom'].unique().tolist())))
    bathroom = float(st.selectbox('Bathrooms',sorted(df['bathroom'].unique().tolist())))

with col3:
    balcony = st.selectbox('Balconies',sorted(df['balcony'].unique().tolist()))
    property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SECTION 2 ----------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Area & Rooms")

col4, col5, col6 = st.columns(3)

with col4:
    built_up_area = float(st.number_input('Built Up Area (sqft)', min_value=200.0))

with col5:
    servant_room = float(st.selectbox('Servant Room',[0.0, 1.0]))

with col6:
    store_room = float(st.selectbox('Store Room',[0.0, 1.0]))

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SECTION 3 ----------------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader(" Additional Features")

col7, col8, col9 = st.columns(3)

with col7:
    furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

with col8:
    luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

with col9:
    floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- BUTTON ----------------
if st.button(' Predict Price'):

    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area,
             servant_room, store_room, furnishing_type, luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)

    # prediction
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # ---------------- RESULT ----------------
    st.markdown("---")

    st.markdown(f"""
    <div class="result">
        <h2>💰 Estimated Price</h2>
        <h1>₹ {round(base_price,2)} Cr</h1>
        <p>Range: ₹ {round(low,2)} Cr - ₹ {round(high,2)} Cr</p>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

