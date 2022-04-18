from numpy import size
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb
sb.set_theme(style="white", palette=None)
import pickle

#https://medium.com/mlearning-ai/explore-make-predictions-and-evaluate-your-ml-models-with-streamlit-and-pipelines-b6c3efeb92ff

class plot_type:
    def __init__(self,data):
        self.data = data
        self.fig=None
        self.update_layout=None

    def bar(self,x,y,color):
        self.fig=px.bar(self.data,x=x,y=y,color=color)

    def pie(self,x,y):
        self.fig = px.pie(self.data,values=x,names=y)

        
    def set_title(self,title):
        
        self.fig.update_layout(
                title=f"{title}",
                    yaxis=dict(tickmode="linear"),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white',size=18))

    def set_title_x(self,title):
        
        self.fig.update_layout(
                title=f"{title}",
                    xaxis=dict(tickmode="linear"),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white',size=18))

    def set_title_pie(self,title):
        self.fig.update_layout(title=title,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white',size=18))
        
    def plot(self):
        st.write(self.fig)

class slide_bar:
    value=4
    def __init__(self,title,x,y):
        self.title = title
        self.x=x
        self.y=y
        self.slide_bar = None
        

    def set(self):
        self.slide_bar = st.slider(self.title,self.x,self.y)
        slide_bar.value=self.slide_bar

class select_box:
    value="tyrion"
    def __init__(self,data):
        self.data=data
        self.box=None
    def place(self,title,key):
        header(title)
        self.box = st.selectbox(str(key),self.data)
        select_box.value=self.box

def title(text,size):
    st.markdown(f'<h1 style="font-weight:bolder;font-size:{size}px;text-align:left;">{text}</h1>',unsafe_allow_html=True)


def header(text):
    st.markdown(f"<p style='font-weight:bolder;font-size:20px'>{text}</p>",unsafe_allow_html=True)


@st.cache(suppress_st_warning=True)
def get_cleaned_data():
    cleaned_data = pd.read_csv("../datasets/google_app_scrap_cleaned.csv")
    return cleaned_data

@st.cache(suppress_st_warning=True)
def get_model():
    model = pickle.load(open('./model/model.pkl', 'rb'))

condition = st.sidebar.selectbox(
    "Select the visualization",
    ("Introduction", "EDA", "Model Prediction", "Model Evaluation")
)

#loading the data and model
df = get_cleaned_data()
model = get_model()

# config css
with open("./styles/styles.css") as f:
    st.markdown(f'<head><style>{f.read()}</style><head>',unsafe_allow_html=True)


google_play_store_img = Image.open('./images/image_google_play-store.webp')

#pages
if condition == 'Introduction':
    st.image(google_play_store_img, caption='Windows 11 introduces support on Google Play')

elif condition == 'EDA':
    st.write(
    '''
        # Exploratory Data Analysis
        
        This is the EDA on apps in the android market
    ''')
    title("Ratings",24,"black")
    
    # chart 1
    fig1, axes =  plt.subplots(1, 2, figsize = (15, 5))
    f = sb.histplot(df, x = "RATING", ax = axes[0])
    ratings = df[['1_STAR_RATINGS','2_STAR_RATINGS','3_STAR_RATINGS','4_STAR_RATINGS','5_STAR_RATINGS']]
    rating_count = pd.DataFrame(ratings.mean(axis=0))
    rating_count.columns = ['Mean']
    rating_count.reset_index(inplace=True)
    
    axes[1] = plt.pie(rating_count['Mean'], labels = rating_count['index'], autopct='%.0f%%', radius = 1.5)
    plt.title("Rating Distribution By Mean",pad=60, fontsize = 15)
    st.write(fig1)
    
    # chart 2
    pass
elif condition == "Model Prediction":
    title("App performance predictor",30)
    st.write("This app predicts if the app will reach 1 Million Downloads in its launch year (first year since app release)")
    
    with st.expander("Features Description"):
        st.markdown(
            """
                | Feature                   | Description          |
                | --------------------------| -------------------- |
                | Game                      | True if app category is game, otherwise false |
                | Content Rating       | Content rating of the app. Can be everyone, teen, or adults     |
                | Free | True if app is game, otherwise false     |
                | Price Band       | Price of the app in USD. Free: 0, Cheap: 0 - 2.99, Normal: 2.99 - 4.99, Expensive: 4.99 - 14.99, Very Expensive: > 14.99  |
                | Ad Supported     |  True if app is ad supported, otherwise false   |
                | Size Band     | Size of the app. Very Small: < 10MB, Small: 10MB - 25MB, Medium: 25MB - 75MB, Large: 75MB - 100MB, Very Large: > 100MB|
                | In App Purchases     | True if app is has in app purchases, otherwise false  |
                | Update period   | Period in which the app will get updated|
                | Review rate     | Review rate of the app, how frequent will the app be reviewed?|
                | Rating rate     | Rating rate of the app, how frequent will the app be rated?|
            """)
   
    header("Please input the features for your app in the fields below")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Get user input for game
        game = st.radio(
        "Game",
        ('True', 'False'))
    with col2:
        # Get user input for ad supported
        ad_supported = st.radio(
        "Ad Supported",
        ('True', 'False'), index=0)
    with col3:
        # Get user input for in app purchases
        in_app_purchases = st.radio(
        "In App Purchases",
        ('True', 'False'))
    with col4:
        # Get user input for free
        free = st.radio(
        "Free",
        ('True', 'False'))
    row2_col1, _, row2_col2, _ ,  row2_col3= st.columns([10,1,10,1,10])
    with row2_col1:
        # Get user input for Price Band
        price_band = st.selectbox(
        'Price Band',
        ('Free', 'Cheap', 'Normal', "Expensive", "Very Expensive"))
    
    with row2_col2:
        # Get user input for Size Band
        size_band = st.selectbox(
        'Size Band',
        ('Very Small', 'Small', 'Medium', "Large", "Very Large"))
    
    with row2_col3:
        # Get user input for content rating
        content_rating = st.selectbox(
            'Content Rating',
            ('Everyone', 'Teen', 'Adults'))
    row3_col1, _ ,  row3_col2, _ ,  row3_col3= st.columns([10,1,10,1,10])
    with row3_col1:
        # Get user input for Update period
        update_period = st.selectbox(
        'Update Period',
        ('Within few days', 'Around a week', 'Within 1 month', "1 to 3 months", "3 to 6 months", "More than 6 months"))
    with row3_col2:
        # Get user input for Review Rate
        review_rate = st.selectbox(
            'Review Rate',
            ('Low', 'Medium', 'High', "More than once per day"))
    with row3_col3:
        # Get user input for Rating Rate
        rating_rate = st.selectbox(
            'Rating Rate',
            ('Low', 'Medium', 'High', "More than 50 per day"))
    
    header("Model Prediction")
    if st.button('Predict data'):
        # data preprocessing
        
        st.write('Havent implemented')
    else:
        pass
    
    
elif condition == "Model Evaluation":
    pass