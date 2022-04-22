from re import M

from st_aggrid import AgGrid
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb
sb.set_theme(style="white", palette=None)
import pickle
from dython import nominal

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
    cleaned_data = pd.read_csv("./data/streamlit_eda.csv")
    return cleaned_data[["APP_NAME", 'RATING', 'INSTALLS_GROUP', 'MAX_INSTALLS', 'RATING_RATE', 'CATEGORY', 'REVIEW_RATE', 'FREE', 'PRICEBAND', 'PRICE', 'SIZEBAND', 'SIZE', 'CONTENT_RATING', 'AD_SUPPORTED', 'COUNTRY', 'IN_APP_PURCHASES', 'EDITORS_CHOICE', 'DAYS_SINCE_UPDATE_RANGE', 'DAYS_SINCE_RELEASED_RANGE']]

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_model():
    model = pickle.load(open('./model/model.pkl', 'rb'))
    return model

condition = st.sidebar.selectbox(
    "Select the visualization",
    ("Introduction", "EDA", "Model Prediction", "Model Evaluation")
)

#loading the data and model
df = get_cleaned_data()
model = get_model()

# draw heatmap
def draw_heatmap(heatmap, format=".0f"):
    fig, ax = plt.subplots()
    hmap = sb.heatmap(heatmap, annot=True, fmt=format, ax=ax)
    st.write(fig)
    
def draw_heatmap_corr(heatmap, format=".0f"):
    fig, ax = plt.subplots()
    hmap = sb.heatmap(heatmap, annot=True, fmt=format, ax=ax, annot_kws={"size":7} ,cbar=False)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=6)
    st.write(fig)

# config css
with open("./styles/styles.css") as f:
    st.markdown(f'<head><style>{f.read()}</style><head>',unsafe_allow_html=True)

google_play_store_img = Image.open('./images/image_google_play-store.webp')

#pages
if condition == 'Introduction':
    st.image(google_play_store_img, caption='Windows 11 introduces support on Google Play')
    st.write("""
             In today's world, apps has been playing an important role in every one's daily life. 
             From Ecommerce apps, to social media apps to entertainment mobile apps, it is nearly impossible for us to stay away from any apps in our life.
             """)
    st.write("In this project, we analyse the Android Market and try to predict if a newly lanuched app can reach 1 Million downloads after 1 year of its release date.")
    st.text("")
    st.text("")
    st.text("")
    st.markdown("<p style='font-size:12px;text-align:right;'>Contributors: Ivan, Aaron, Yifei</p>",unsafe_allow_html=True)
elif condition == 'EDA':
    title("Exploratory Data Analysis",30)
    st.write("This is the EDA on apps in the android market")
    header("Scraped data (after cleaning)")
    AgGrid(df)
    # chart 1
    header("Heatmap corelation between selected features")
    jointDf = df[['RATING', 'INSTALLS_GROUP', 'RATING_RATE', 'CATEGORY', 'REVIEW_RATE', 'FREE', 'PRICEBAND', 'SIZEBAND', 'CONTENT_RATING', 'AD_SUPPORTED', 'IN_APP_PURCHASES', 'EDITORS_CHOICE', 'DAYS_SINCE_UPDATE_RANGE']]
    corr = nominal.associations(jointDf);
    draw_heatmap_corr(corr["corr"], format=".2f")
    
    title("Installs group EDA",28)
    # chart 2
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        label = df['INSTALLS_GROUP'].value_counts().index.tolist()
        fig2, ax = plt.subplots(figsize = (10, 10))
        plt.pie(x = df['INSTALLS_GROUP'].value_counts().to_frame().INSTALLS_GROUP, labels = label)
        my_circle=plt.Circle((0,0), 0.7, color='white')
        p=plt.gcf()
        p.gca().add_artist(my_circle)
        plt.title("Distribution of Installs Group", size =20)
        st.write(fig2)
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
    st.write("Input")
    user_input_data = {"Game": game,
                       "Ad Supported": ad_supported,
                       "In App Purchases": in_app_purchases,
                       "Free": free,
                       "Price Band": price_band,
                       "Size Band": size_band,
                       "Content Rating": content_rating,
                       "Update Period": update_period,
                       "Review Rate": review_rate,
                       "Rating Rate": rating_rate}
    input_x = pd.DataFrame(data=user_input_data, index=[0])
    st.table(input_x)
    if st.button('Predict data'):
        # data preprocessing
        X_test = {"CATEGORY_Game": 1 if game == "True" else 0,
                  "CATEGORY_Non Game": 0 if game == "True" else 1,
                  "CONTENT_RATING_Adults": 1 if content_rating == "Adults" else 0,
                  "CONTENT_RATING_Teen": 1 if content_rating == "Teen" else 0,
                  "CONTENT_RATING_Everyone": 1 if content_rating == "Everyone" else 0,
                  "FREE": 1 if free == "True" else 0,
                  "AD_SUPPORTED": 1 if ad_supported == "True" else 0,
                  "IN_APP_PURCHASES": 1 if in_app_purchases == "True" else 0,
                  "PRICEBAND": None,
                  "SIZEBAND": None,
                  "DAYS_SINCE_UPDATE_RANGE": None,
                  "REVIEW_RATE": None,
                  "RATING_RATE": None}
        # label encoding
        pb_mapping = {"Free": 0, "Cheap": 1, "Normal": 2, "Expensive": 3, "Very Expensive": 4}
        sb_mapping = {"Very Small": 0, "Small": 1, "Medium": 2, "Large": 3, "Very Large": 4}
        dsu_mapping = {"Within few days": 0, "Around a week": 1, "Within 1 month": 2, "1 to 3 months": 3, "3 to 6 months": 4, "More than 6 months": 5}
        revr_mapping = {"Low": 0, "Medium": 1, "High": 2, "More than once per day": 3}
        ratr_mapping = {"Low": 0, "Medium": 1, "High": 2, "More than 50 per day": 3}
        X_test["PRICEBAND"] = pb_mapping[price_band]
        X_test["SIZEBAND"] = sb_mapping[size_band]
        X_test["DAYS_SINCE_UPDATE_RANGE"] = dsu_mapping[update_period]
        X_test["REVIEW_RATE"] = revr_mapping[review_rate]
        X_test["RATING_RATE"] = ratr_mapping[rating_rate]
        input_x_test = pd.DataFrame(data=X_test, index=[0])
        y_test = model.predict(input_x_test)
        if (y_test == 1):
            result = "After Launch Year: More than 1 Million Downloads :)"
            st.balloons()
            st.success(result)
        else:
            result = "After Launch Year: Less than 1 Million Downloads :("
            st.error(result)
    else:
        pass
    
elif condition == "Model Evaluation":
    title("Model Evaluation",30)
    header("Model Parameters: ")
    st.write("Decision Tree, Max Depth = 6")
    col1, col2 = st.columns(2)
    train_matrix = [[1422, 149], [153, 511]]
    test_matrix = [[462, 58], [60, 166]]
    with col1:
        draw_heatmap(train_matrix)
    with col2:
        draw_heatmap(test_matrix)
    
    col1_score, col2_score = st.columns(2)
    with col1_score:
        tn, fp, fn, tp = train_matrix[0][0], train_matrix[0][1], train_matrix[1][0], train_matrix[1][1]
        header("Train data")
        accuracy = (tn + tp)/ (tn+tp+fp+fn)
        precision = (tp)/ (tp + fp)
        recall = (tp / (tp + fn))
        f1_score = 2* (precision* recall)/(precision + recall)
        st.write("Accuracy: {:.1f}%".format(accuracy * 100))
        st.write("Precision: {:.1f}%".format(precision * 100))
        st.write("Recall: {:.1f}%".format(recall * 100))
        st.write("F1-score: {:.1f}%".format(f1_score * 100))  
    with col2_score:
        tn, fp, fn, tp = test_matrix[0][0], test_matrix[0][1], test_matrix[1][0], test_matrix[1][1]
        header("Test data")
        accuracy = (tn + tp)/ (tn+tp+fp+fn)
        precision = (tp)/ (tp + fp)
        recall = (tp / (tp + fn))
        f1_score = 2* (precision* recall)/(precision + recall)
        st.write("Accuracy: {:.1f}%".format(accuracy * 100))
        st.write("Precision: {:.1f}%".format(precision * 100))
        st.write("Recall: {:.1f}%".format(recall * 100))
        st.write("F1-score: {:.1f}%".format(f1_score * 100))    
    