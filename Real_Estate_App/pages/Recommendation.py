import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Propeak Recommendations", page_icon="🏠", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .stSelectbox, .stNumberInput {
        margin-bottom: 10px;
    }
    .reco-card {
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(128, 128, 128, 0.1);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #28a745;
    }
    .stButton>button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #218838;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏠 Smart Property Recommendations")
st.markdown("---")

#  Path fix (ONLY change)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

location_df = pickle.load(open(os.path.join(BASE_DIR,'datasets/location_distance.pkl'),'rb'))

cosine_sim1 = pickle.load(open(os.path.join(BASE_DIR,'datasets/cosine_sim1.pkl'),'rb'))
cosine_sim2 = pickle.load(open(os.path.join(BASE_DIR,'datasets/cosine_sim2.pkl'),'rb'))
cosine_sim3 = pickle.load(open(os.path.join(BASE_DIR,'datasets/cosine_sim3.pkl'),'rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


# Test the recommender function using a property name
recommend_properties_with_scores('DLF The Camellias')


st.title('Select Location and Radius')

selected_location = st.selectbox('Location',sorted(location_df.columns.to_list()))

radius = st.number_input('Radius in Kms')

if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

    for key, value in result_ser.items():
        st.text(str(key) + " " + str(round(value/1000)) + ' kms')


st.title('Recommend Appartments')

selected_appartment = st.selectbox('Select an appartment',sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)

    st.dataframe(recommendation_df)