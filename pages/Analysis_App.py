# 1. Mapbox
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Property Analysis')
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fedcba;  /* Change this to your desired color */
    }
    </style>""",
    unsafe_allow_html=True
    )
st.title('Analyse Property Features')

new_df = pd.read_csv('datasets/data_viz1.csv')

group_df = new_df.groupby('sector')[[
    'price','price_per_sqft','built_up_area',
    'latitude','longitude']].mean()
st.header('Mapbox')
fig = px.scatter_mapbox(
    group_df, lat='latitude', lon='longitude', size='built_up_area',
    color='price_per_sqft',hover_name=group_df.index,zoom=10,
    color_continuous_scale=px.colors.cyclical.IceFire,
    mapbox_style='open-street-map'
)
st.plotly_chart(fig,use_container_width=True)

# 2. Wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.header('Property Highlights in This Area')
features = pd.read_csv('datasets/properties.csv')
text = str(features['features'].unique())
wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      min_font_size=10).generate(text)
wc = plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
#plt.show()
st.pyplot(wc)

# 3. Scatterplot area vs price
st.header('Scatterplot')
pt = st.selectbox('Property Type',['Flat','House']).lower()
plot_df = new_df[new_df['property_type'] == pt]

sp = px.scatter(plot_df,
                x='built_up_area',y='price',
                color='bedRoom',title=str(pt).title()+' : Area vs Price'
                 )
st.plotly_chart(sp,use_container_width=True)

# 4. Pie chart for bedrooms filtered by sector
st.header('Properties According to Number of Bedrooms')
sect = st.selectbox('Sector',new_df['sector'].unique())
pie_df = new_df[new_df['sector'] == sect]

pie_chart = px.pie(pie_df,
                names = 'bedRoom'
                 )
st.plotly_chart(pie_chart,use_container_width=True)

# 5. Boxplot - Comparison of different bedroom flat prices
st.header('Price Range of Properties According to Number of Bedrooms')
box = px.box(new_df[new_df['bedRoom'] <= 4],x = 'bedRoom', y = 'price')
st.plotly_chart(box,use_container_width=True)

# 6. Distplot - Property Type vs Price
import seaborn as sns
st.header('Distribution of Price for Houses vs Flats')

dist = plt.figure(figsize=(10,5))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='Houses')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'],label='Flats')
plt.legend()
st.pyplot(dist)



