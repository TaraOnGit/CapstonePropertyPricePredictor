import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title='property_suggestions_page')
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fedcba;  /* Change this to your desired color */
    }
    </style>""",
    unsafe_allow_html=True
    )

st.title('Property Suggestions')
location_df = pickle.load(open('datasets/location_distance.pkl','rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl','rb'))


def recommend_properties_with_scores(property_name, top_n=247):
    cosine_sim_matrix = 30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3
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

    return recommendations_df.head(5)

prp = st.selectbox('Property Like :  ',sorted(location_df.index))
if st.button('Generate Matching Properties'):
    st.dataframe(recommend_properties_with_scores(prp, top_n=247))

