import streamlit as st
import pandas as pd
from PIL import Image

#https://medium.com/mlearning-ai/explore-make-predictions-and-evaluate-your-ml-models-with-streamlit-and-pipelines-b6c3efeb92ff

@st.cache
def get_raw_data():
    """
    This function returns a pandas DataFrame with the raw data.
    """

    raw_data = pd.read_csv("datasets/google_app_scrap.csv")
    return raw_data

@st.cache
def get_cleaned_data():
    """
    This function returns a pandas DataFrame with the cleaned data.
    """

    cleaned_data = pd.read_csv("../datasets/google_app_scrap_cleaned.csv")
    return cleaned_data

condition = st.sidebar.selectbox(
    "Select the visualization",
    ("Introduction", "EDA", "Model Prediction", "Model Evaluation")
)

google_play_store_img = Image.open('./images/image_google_play-store.webp')

#pages

if condition == 'Introduction':
    st.image(google_play_store_img, caption='Windows 11 introduces support on Google Play')
    st.write(
    '''
        # Android Market Analysis
        Analysis of the Android market using app data from Google Play Store

        Team Members: Aaron, Ivan, Yifei
    ''')
elif condition == 'EDA':
    st.write(
    '''
        # Google Scraped Data
    ''')
    st.dataframe(data=get_cleaned_data(), width=None, height=None)
    pass
elif condition == "Model Prediction":
    pass
elif condition == "Model Evaluation":
    pass