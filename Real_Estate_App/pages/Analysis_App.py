
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Real Estate Analytics", layout="wide")

st.title('Real Estate Analytics Dashboard')

# ---------------- LOAD DATA ----------------
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))

# ---------------- DATA CLEANING ----------------
# Convert columns to numeric
cols = ['price','price_per_sqft','built_up_area','latitude','longitude']
new_df[cols] = new_df[cols].apply(pd.to_numeric, errors='coerce')

# Drop missing values
new_df = new_df.dropna(subset=cols)

# ---------------- GROUPING ----------------
group_df = new_df.groupby('sector')[cols].mean().reset_index()

# ---------------- MAP ----------------
st.header(' Sector Price per Sqft Geomap')

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

st.plotly_chart(fig, use_container_width=True)

# ---------------- WORDCLOUD ----------------
st.header(' Features Wordcloud')

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='black',
    stopwords=set(['s']),
    min_font_size=10
).generate(feature_text)

fig_wc = plt.figure(figsize=(8,8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

st.pyplot(fig_wc)

# ---------------- AREA VS PRICE ----------------
st.header('Area vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])

filtered_df = new_df[new_df['property_type'] == property_type]

fig1 = px.scatter(
    filtered_df,
    x="built_up_area",
    y="price",
    color="bedRoom",
    title=f"{property_type.capitalize()} Area vs Price"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- PIE CHART ----------------
st.header(' BHK Distribution')

sector_options = new_df['sector'].dropna().unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':
    pie_df = new_df
else:
    pie_df = new_df[new_df['sector'] == selected_sector]

fig2 = px.pie(pie_df, names='bedRoom', title="BHK Distribution")

st.plotly_chart(fig2, use_container_width=True)

# ---------------- BOX PLOT ----------------
st.header('BHK Price Comparison')

fig3 = px.box(
    new_df[new_df['bedRoom'] <= 4],
    x='bedRoom',
    y='price',
    title='BHK Price Range'
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- DISTRIBUTION PLOT ----------------
st.header('Price Distribution: Flat vs House')

fig4 = plt.figure(figsize=(10, 4))

sns.kdeplot(
    new_df[new_df['property_type'] == 'house']['price'],
    label='House',
    fill=True
)

sns.kdeplot(
    new_df[new_df['property_type'] == 'flat']['price'],
    label='Flat',
    fill=True
)

plt.legend()

st.pyplot(fig4)

