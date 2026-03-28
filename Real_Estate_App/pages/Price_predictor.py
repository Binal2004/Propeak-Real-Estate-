import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Price Predictor", layout="wide")

st.title("Real Estate Price Predictor")

# ---------------- DOWNLOAD MODEL FROM DRIVE ----------------
file_id = "1hQQFW6g7eM4Vqa6XUuZCTO_Ae_nfhq5v"
url = f"https://drive.google.com/uc?id={file_id}"

model_path = "pipeline.pkl"

if not os.path.exists(model_path):
    with st.spinner("Downloading model..."):
        gdown.download(url, model_path, quiet=False)

# ---------------- LOAD MODEL ----------------
try:
    with open(model_path, 'rb') as file:
        pipeline = pickle.load(file)
except:
    st.error("Model loading failed")
    st.stop()

# ---------------- LOAD DF ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
df_path = os.path.join(BASE_DIR, "df.pkl")

try:
    with open(df_path, 'rb') as file:
        df = pickle.load(file)
except:
    st.error("df.pkl not found")
    st.stop()

# ---------------- UI ----------------
st.header('Enter your inputs')

property_type = st.selectbox('Property Type',['flat','house'])

sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['bedRoom'].unique().tolist())))

bathroom = float(st.selectbox('Number of Bathrooms',sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies',sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area'))

servant_room = float(st.selectbox('Servant Room',[0.0, 1.0]))
store_room = float(st.selectbox('Store Room',[0.0, 1.0]))

furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))

# ---------------- PREDICTION ----------------
if st.button('Predict'):

    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age,
             built_up_area, servant_room, store_room,
             furnishing_type, luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)

    try:
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22

        st.subheader("Predicted Price Range")
        st.success(f"{round(low,2)} Cr - {round(high,2)} Cr")

    except:
        st.error("Prediction failed. Check inputs.")