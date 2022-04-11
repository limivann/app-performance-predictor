import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb
sb.set_theme(style="white", palette=None)

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

def title(text,size,color):
    st.markdown(f'<h1 style="font-weight:bolder;font-size:{size}px;color:{color};text-align:left;">{text}</h1>',unsafe_allow_html=True)

def header(text):
    st.markdown(f"<p style='color:white;'>{text}</p>",unsafe_allow_html=True)



@st.cache(persist=True,suppress_st_warning=True)
def get_cleaned_data():
    cleaned_data = pd.read_csv("../datasets/google_app_scrap_cleaned.csv")
    return cleaned_data

condition = st.sidebar.selectbox(
    "Select the visualization",
    ("Introduction", "EDA", "Model Prediction", "Model Evaluation")
)

#loading the data
df = get_cleaned_data()

# config css
with open("./styles/styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)


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
        # Exploratory Data Analysis
        
        This is the EDA on apps in the android market
    ''')
    title("Ratings",24,"black")
    
    fig1, axes =  plt.subplots(1, 2, figsize = (15, 5))
    f = sb.histplot(df, x = "RATING", ax = axes[0])
    ratings = df[['1_STAR_RATINGS','2_STAR_RATINGS','3_STAR_RATINGS','4_STAR_RATINGS','5_STAR_RATINGS']]
    rating_count = pd.DataFrame(ratings.mean(axis=0))
    rating_count.columns = ['Mean']
    rating_count.reset_index(inplace=True)
    
    axes[1] = plt.pie(rating_count['Mean'], labels = rating_count['index'], autopct='%.0f%%', radius = 1.5)
    plt.title("Rating Distribution By Mean",pad=60, fontsize = 15)
    st.write(fig1)
    pass
elif condition == "Model Prediction":
    pass
elif condition == "Model Evaluation":
    pass