
import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon="🏡",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0e1117, #111827);
    color: white;
}

.title {
    font-size: 55px;
    font-weight: 800;
    background: linear-gradient(90deg, #00d4ff, #00ffa6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 20px;
    color: #cfcfcf;
    margin-bottom: 30px;
}

.card {
    background: linear-gradient(145deg, #1c1f26, #111);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    transition: 0.4s;
    border: 1px solid #2a2f3a;
}

.card:hover {
    transform: translateY(-10px) scale(1.03);
    box-shadow: 0px 10px 30px rgba(0,212,255,0.2);
}

.card h3 {
    margin-bottom: 10px;
}

.btn {
    display: inline-block;
    margin-top: 10px;
    padding: 8px 15px;
    border-radius: 10px;
    background-color: #00d4ff;
    color: black;
    font-weight: 600;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown('<p class="title">Gurgaon Real Estate Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Smart insights • Price prediction • Location intelligence</p>', unsafe_allow_html=True)

st.write("")

# ---------------- FEATURE CARDS (MATCH SIDEBAR) ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>Price Predictor</h3>
        <p>Predict property prices using ML model</p>
        <p style="color:#00d4ff;">Go to sidebar → Price Predictor</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3> Analysis App</h3>
        <p>Explore trends, charts & sector insights</p>
        <p style="color:#00d4ff;">Go to sidebar → Analysis App</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3> Recommendation</h3>
        <p>Find best properties based on preferences</p>
        <p style="color:#00d4ff;">Go to sidebar → Recommendation</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- CTA ----------------
st.markdown("###  Get Started")
st.success("Use the sidebar to navigate between modules")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("##  Navigation")
st.sidebar.info("Select a page to begin")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ by <b>Team-Propeak</b></center>",
    unsafe_allow_html=True
)

