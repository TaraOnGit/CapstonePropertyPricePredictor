import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title='predict_page')
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fedcba;  /* Change this to your desired color */
    }
    </style>""",
    unsafe_allow_html=True
    )

st.title('Predict Property Price')

with open('df.pkl','rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl','rb') as file:
    pipe = pickle.load(file)

st.header('Enter the Property Features')
#'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
 #      'agePossession', 'built_up_area', 'servant room', 'store room',
  #     'furnishing_type', 'luxury_category', 'floor_category'


property_type = st.selectbox('Property Type',['Flat','House'])
sector = st.selectbox('Sector',sorted(df['sector'].astype(int).unique()))
bedroom = st.selectbox('No. of Bedrooms',sorted(df['bedRoom'].unique()))
bathroom = st.selectbox('No. of Bathrooms',sorted(df['bathroom'].unique()))
balcony = st.selectbox('No. of Balconies',sorted(df['balcony'].astype(int).unique()))
age_p = st.selectbox('Age of Property',sorted(df['agePossession'].unique()))
built_up_area = float(st.number_input('Built Up Area'))
servant_room = st.selectbox('Servant Rooms',sorted(df['servant room'].unique()))
store_room = st.selectbox('Store Rooms',sorted(df['store room'].unique()))
#fur_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique()))
fur_type = st.selectbox('Furnishing Type',['Furnished','Semi Furnished','Unfurnished'])
if fur_type == 'Furnished':
    fur_type = 2
elif fur_type == 'Semi Furnished':
    fur_type = 1
else:
    fur_type = 0

#lux_cat = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique()))
lux_cat = st.selectbox('Luxury Category',['Luxury','Semi Luxury','Budget'])
if lux_cat == 'Luxury':
    lux_cat = 2
elif lux_cat == 'Semi Luxury':
    lux_cat = 1
else:
    lux_cat = 0

#floor_cat = st.selectbox('Floor Category',sorted(df['floor_category'].unique()))
floor_cat = st.selectbox('Floor Category',['Low Rise','Mid Rise','High Rise'])
if floor_cat == 'High Rise':
    floor_cat = 2
elif floor_cat == 'Mid Rise':
    floor_cat = 1
else:
    floor_cat = 0

if st.button('Predict Price'):

    # form dataframe
    data = [[property_type,sector,bedroom,bathroom,balcony,age_p,
             built_up_area,servant_room,store_room,fur_type,lux_cat,floor_cat]]

    # predict
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)
    one_df['Unnamed: 0'] = 0
    pred = np.expm1(pipe.predict(one_df))



    # display
    st.text('The price for the requested property according to market trends could range between')
    st.text('{} Crores to {} Crores'.format(np.round(pred[0] - 0.22,2), np.round(pred[0] + 0.22,2)))