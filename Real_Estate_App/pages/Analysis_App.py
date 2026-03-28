import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Real Estate Analytics | Propeak", page_icon="📊", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .metric-card {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #007bff;
    }
    .stPlotlyChart {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Let streamlit handle heading colors for theme compatibility */
    h1, h2, h3 {
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('📊 Gurgaon Real Estate Analytics')
st.markdown("---")

# ---------------- BASE PATH ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ---------------- LOAD DATA ----------------
csv_path = os.path.join(BASE_DIR, "datasets", "data_viz1.csv")
pkl_path = os.path.join(BASE_DIR, "datasets", "feature_text.pkl")

# Load safely
new_df = pd.read_csv(csv_path)
feature_text = pickle.load(open(pkl_path, "rb"))

# ---------------- DATA CLEANING ----------------
cols = ['price','price_per_sqft','built_up_area','latitude','longitude']
new_df[cols] = new_df[cols].apply(pd.to_numeric, errors='coerce')
new_df = new_df.dropna(subset=cols)

# ---------------- GROUPING ----------------
group_df = new_df.groupby('sector')[cols].mean().reset_index()

# ---------------- MAP ----------------
st.header('Sector Price per Sqft Geomap')

fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size='built_up_area',
    hover_name="sector",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    height=700
)

# Use plotly_chart and capture selected points if possible
try:
    selected_points = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
except TypeError:
    # Fallback for older streamlit versions that don't support on_select
    st.plotly_chart(fig, use_container_width=True)
    selected_points = None

# Initialize selected sector
selected_sector = "overall"

# Check if a point was clicked on the map
if selected_points is not None and isinstance(selected_points, dict) and 'selection' in selected_points:
    points = selected_points.get('selection', {}).get('points', [])
    if len(points) > 0:
        selected_sector = points[0].get('hovertext', "overall")
        st.info(f"Selected Sector from Map: **{selected_sector}**")

# Fallback selection box
sector_options = sorted(new_df['sector'].unique().tolist())
sector_options.insert(0, 'overall')

if selected_sector != 'overall' and selected_sector in sector_options:
    index = sector_options.index(selected_sector)
else:
    index = 0

selected_sector = st.selectbox('Select Sector for detailed analysis', sector_options, index=index)

# ---------------- SECTOR ANALYSIS BOX ----------------
if selected_sector != 'overall':
    st.info(f"### Analysis for {selected_sector}")
    
    sector_df = new_df[new_df['sector'] == selected_sector]
    
    # Summary Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Avg Price", f"₹ {round(sector_df['price'].mean(), 2)} Cr")
    with m2:
        st.metric("Avg Price/Sqft", f"₹ {round(sector_df['price_per_sqft'].mean(), 0)}")
    with m3:
        st.metric("Properties", f"{len(sector_df)}")

    # Specific charts for this sector
    col1, col2 = st.columns(2)
    
    with col1:
        # BHK Distribution in this sector
        fig_bhk = px.pie(sector_df, names='bedRoom', title=f"BHK Distribution in {selected_sector}")
        st.plotly_chart(fig_bhk, use_container_width=True)
        
    with col2:
        # Price vs Area in this sector
        fig_price_area = px.scatter(sector_df, x="built_up_area", y="price", 
                                    color="property_type", hover_data=['bedRoom'],
                                    title=f"Price vs Area in {selected_sector}")
        st.plotly_chart(fig_price_area, use_container_width=True)
    
    # Show more details in an expander
    with st.expander("View all properties in this sector"):
        st.dataframe(sector_df[['property_type', 'price', 'built_up_area', 'bedRoom', 'bathroom', 'balcony']])
else:
    st.write("💡 *Click on a point on the map or select a sector from the dropdown above to see detailed insights here.*")

# ---------------- WORDCLOUD ----------------
st.header('Features Wordcloud')

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='black',
    stopwords=set(['s']),
    min_font_size=10
).generate(feature_text)

fig_wc, ax_wc = plt.subplots(figsize=(8,8))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis("off")
st.pyplot(fig_wc)

# ---------------- AREA VS PRICE ----------------
st.header('Area vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'], key='prop_type_select')
filtered_df = new_df[new_df['property_type'] == property_type]

# Include more columns for the detail box
fig1 = px.scatter(
    filtered_df,
    x="built_up_area",
    y="price",
    color="bedRoom",
    hover_name="sector",
    hover_data=['bathroom', 'balcony', 'price_per_sqft'],
    title=f"{property_type.capitalize()} Area vs Price"
)

# Use on_select to capture clicks
try:
    selected_prop = st.plotly_chart(fig1, use_container_width=True, on_select="rerun")
except TypeError:
    # Fallback for older streamlit versions
    st.plotly_chart(fig1, use_container_width=True)
    selected_prop = None

# ---------------- PROPERTY DETAILS BOX ----------------
if selected_prop is not None and isinstance(selected_prop, dict) and 'selection' in selected_prop:
    points = selected_prop.get('selection', {}).get('points', [])
    if len(points) > 0:
        point = points[0]
        # Get data from the clicked point
        # The indices in filtered_df might not match Plotly's pointIndex if sorted, 
        # so we rely on the hover data provided by Plotly.
        
        st.info("### Selected Property Details")
        d1, d2, d3, d4 = st.columns(4)
        
        with d1:
            st.metric("Price", f"₹ {point.get('y')} Cr")
        with d2:
            st.metric("Area", f"{point.get('x')} sqft")
        with d3:
            st.metric("Sector", point.get('hovertext'))
        with d4:
            st.metric("BHK", point.get('color'))
        
        # Additional data from hover_data
        custom_data = point.get('customdata', [])
        if len(custom_data) >= 3:
            st.write(f"**Bathrooms:** {custom_data[0]} | **Balconies:** {custom_data[1]} | **Price/Sqft:** ₹ {round(float(custom_data[2]), 0)}")
    else:
        st.write("💡 *Click on a point in the chart above to see property details here.*")
else:
    st.write("💡 *Click on a point in the chart above to see property details here.*")

# ---------------- BOX PLOT ----------------
st.header('BHK Price Comparison')

bhk_df = new_df[new_df['bedRoom'] <= 4]

fig3 = px.box(
    bhk_df,
    x='bedRoom',
    y='price',
    title='BHK Price Range',
    color='bedRoom'
)

# Use on_select to capture box clicks
try:
    selected_bhk_data = st.plotly_chart(fig3, use_container_width=True, on_select="rerun")
except TypeError:
    st.plotly_chart(fig3, use_container_width=True)
    selected_bhk_data = None

# ---------------- BHK DETAILS BOX ----------------
if selected_bhk_data is not None and isinstance(selected_bhk_data, dict) and 'selection' in selected_bhk_data:
    points = selected_bhk_data.get('selection', {}).get('points', [])
    if len(points) > 0:
        # For box plots, x is usually the category (BHK)
        clicked_bhk = points[0].get('x')
        
        if clicked_bhk is not None:
            st.info(f"### Analysis for {int(clicked_bhk)} BHK Properties")
            
            bhk_stats_df = bhk_df[bhk_df['bedRoom'] == clicked_bhk]
            
            s1, s2, s3, s4 = st.columns(4)
            with s1:
                st.metric("Avg Price", f"₹ {round(bhk_stats_df['price'].mean(), 2)} Cr")
            with s2:
                st.metric("Median Price", f"₹ {round(bhk_stats_df['price'].median(), 2)} Cr")
            with s3:
                st.metric("Max Price", f"₹ {round(bhk_stats_df['price'].max(), 2)} Cr")
            with s4:
                st.metric("Total Units", f"{len(bhk_stats_df)}")
            
            # Show price distribution for this BHK in an expander
            with st.expander(f"View details for {int(clicked_bhk)} BHK"):
                st.write(f"In this category, the price ranges from **₹ {round(bhk_stats_df['price'].min(), 2)} Cr** to **₹ {round(bhk_stats_df['price'].max(), 2)} Cr**.")
                st.dataframe(bhk_stats_df[['sector', 'property_type', 'price', 'built_up_area', 'price_per_sqft']])
    else:
        st.write("💡 *Click on a box in the chart above to see BHK-wise details here.*")
else:
    st.write("💡 *Click on a box in the chart above to see BHK-wise details here.*")

# ---------------- DISTRIBUTION PLOT ----------------
st.header('Price Distribution: Flat vs House')

fig4, ax4 = plt.subplots(figsize=(10, 4))

sns.kdeplot(
    new_df[new_df['property_type'] == 'house']['price'],
    label='House',
    fill=True,
    ax=ax4
)

sns.kdeplot(
    new_df[new_df['property_type'] == 'flat']['price'],
    label='Flat',
    fill=True,
    ax=ax4
)

ax4.legend()
st.pyplot(fig4)