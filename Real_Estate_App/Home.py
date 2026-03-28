import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Gurgaon Real Estate",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("Gurgaon Real Estate Analytics")
st.write("Smart insights • Price prediction • Location intelligence")

st.write("---")

# ---------------- NAVIGATION ----------------
col1, col2, col3 = st.columns(3)

# -------- Price Predictor --------
with col1:
    st.subheader(" Price Predictor")
    st.write("Predict property prices using ML model")
    if st.button("Open Price Predictor"):
        st.switch_page("pages/Price_predictor.py")   # ✅ FIXED

# -------- Analysis --------
with col2:
    st.subheader(" Analysis App")
    st.write("Explore trends & insights")
    if st.button("Open Analysis"):
        st.switch_page("pages/Analysis_App.py")      # ✅ FIXED

# -------- Recommendation --------
with col3:
    st.subheader(" Recommendation")
    st.write("Find best properties")
    if st.button("Open Recommendation"):
        st.switch_page("pages/Recommendation.py")    # ✅ FIXED

st.write("---")

st.success("Use buttons or sidebar to navigate")

st.markdown(
    "<center>Made with ❤️ by <b>Team-Propeak</b></center>",
    unsafe_allow_html=True
)