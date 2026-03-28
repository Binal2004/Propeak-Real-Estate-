import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Propeak Real Estate | Gurgaon",
    page_icon="🏠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    /* Let streamlit handle the main background color */
    .stApp {
        background-color: transparent;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border: none;
        color: white;
        transform: translateY(-2px);
    }
    /* Cards that look good in both light and dark mode */
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: rgba(128, 128, 128, 0.1); /* Translucent gray */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-top: 5px solid #007bff;
        border-left: 1px solid rgba(128, 128, 128, 0.2);
        border-right: 1px solid rgba(128, 128, 128, 0.2);
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }
    /* Standard titles that adapt to theme */
    h1 {
        font-weight: 800;
    }
    .subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🏙️ Propeak Real Estate Analytics")
st.markdown('<p class="subtitle">Smart insights • Price prediction • Location intelligence for Gurgaon Real Estate</p>', unsafe_allow_html=True)

st.divider()

# ---------------- NAVIGATION ----------------
col1, col2, col3 = st.columns(3)

# -------- Price Predictor --------
with col1:
    st.markdown("""
        <div class="card">
            <h3>💰 Price Predictor</h3>
            <p>Get accurate price estimates for any property in Gurgaon using our advanced Machine Learning models.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Launch Predictor", key="btn_predictor"):
        st.switch_page("pages/Price_predictor.py")

# -------- Analysis --------
with col2:
    st.markdown("""
        <div class="card">
            <h3>📊 Market Analysis</h3>
            <p>Explore real-time market trends, sector-wise comparisons, and interactive geodata visualizations.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Analytics", key="btn_analysis"):
        st.switch_page("pages/Analysis_App.py")

# -------- Recommendation --------
with col3:
    st.markdown("""
        <div class="card">
            <h3>🏠 Recommendations</h3>
            <p>Find your perfect home with our similarity-based recommendation engine tailored to your needs.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Get Recommendations", key="btn_reco"):
        st.switch_page("pages/Recommendation.py")

st.divider()

# ---------------- FOOTER ----------------
cols = st.columns([1, 2, 1])
with cols[1]:
    st.info("💡 **Tip:** Use the interactive maps in the Analysis section to explore specific sectors by clicking on them.")

st.markdown(
    "<br><center>Made with ❤️ by <b>Team Propeak</b> | © 2026 Gurgaon Real Estate Analytics</center>",
    unsafe_allow_html=True
)