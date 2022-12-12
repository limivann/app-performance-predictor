from re import M
from pathlib import Path
from st_aggrid import AgGrid
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb
sb.set_theme(style="white", palette=None)
import pickle

#https://medium.com/mlearning-ai/explore-make-predictions-and-evaluate-your-ml-models-with-streamlit-and-pipelines-b6c3efeb92ff

st.markdown(
        f"""
<style>
    .appview-container .main .block-container{{
        min-width: 60%;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

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
    data_path = Path(__file__).parents[1] / 'streamlit-app/data/streamlit_eda.csv'
    cleaned_data = pd.read_csv(data_path)
    return cleaned_data[['RATING', 'INSTALLS_GROUP', 'RATING_RATE', 'CATEGORY', 'REVIEW_RATE', 'FREE', 'PRICEBAND', 'SIZEBAND', 'CONTENT_RATING', 'AD_SUPPORTED', 'COUNTRY', 'IN_APP_PURCHASES', 'EDITORS_CHOICE', 'DAYS_SINCE_UPDATE_RANGE', 'DAYS_SINCE_RELEASED_RANGE']]

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_model():
    model_path = Path(__file__).parents[1] / "streamlit-app/model/model.pkl"
    model = pickle.load(open(model_path, 'rb'))
    return model

condition = st.sidebar.selectbox(
    "Select the visualization",
    ("Introduction", "EDA", "Model Prediction", "Model Evaluation")
) 
if condition == "Introduction" or condition =="Model Prediction" or condition == "Model Evaluation":
    st.markdown(
        f"""
        <style>
            .appview-container .main .block-container{{
                min-width: 50%;
                padding-top: 1rem;
                padding-right: 1rem;
                padding-left: 1rem;
                padding-bottom: 1rem;
            }}
        </style>
        """,unsafe_allow_html=True,
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

# get images
google_play_store_img_path = Path(__file__).parents[1] / "images/image_google_play-store.webp"
google_play_store_img = Image.open(google_play_store_img_path)

heatmap_img_path = Path(__file__).parents[1] / "streamlit-app/figures/heatmap_all.png"
heatmap_img = Image.open(heatmap_img_path)

treemap_html_path = Path(__file__).parents[1] / "streamlit-app/figures/treemap_all.html"
treemap_html = open(treemap_html_path, 'r', encoding='utf-8').read()

dist_installs_img_path = Path(__file__).parents[1] / "streamlit-app/figures/distribution_installs.png"
dist_installs_img = Image.open(dist_installs_img_path)

installs_grp_rating_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_rating.png"
installs_grp_rating_img = Image.open(installs_grp_rating_img_path)

installs_grp_ec_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_editors_choice.png"
installs_grp_ec_img = Image.open(installs_grp_ec_img_path)

installs_grp_ads_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_ad_supported.png"
installs_grp_ads_img = Image.open(installs_grp_ads_img_path)

installs_grp_free_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_free.png"
installs_grp_free_img = Image.open(installs_grp_free_img_path)

installs_grp_iap_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_iap.png"
installs_grp_iap_img = Image.open(installs_grp_iap_img_path)

installs_grp_cr_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_cr.png"
installs_grp_cr_img = Image.open(installs_grp_cr_img_path)

installs_grp_dsu_html_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_dsu.html"
installs_grp_dsu_html = open(installs_grp_dsu_html_path, 'r', encoding='utf-8').read()

installs_grp_dsu_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_dsu.png"
installs_grp_dsu_img = Image.open(installs_grp_dsu_img_path)

installs_grp_rc_html_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_review_count.html"
installs_grp_rc_html = open(installs_grp_rc_html_path, 'r', encoding='utf-8').read()

installs_grp_rr_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_rr.png"
installs_grp_rr_img = Image.open(installs_grp_rr_img_path)

installs_grp_size_html_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_size.html"
installs_grp_size_html = open(installs_grp_size_html_path, 'r', encoding='utf-8').read()

installs_grp_cat_html_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_category.html"
installs_grp_cat_html = open(installs_grp_cat_html_path, 'r', encoding='utf-8').read()

installs_grp_cat_free_img_path = Path(__file__).parents[1] / "streamlit-app/figures/installs_group_cat_free.png"
installs_grp_cat_free_img = Image.open(installs_grp_cat_free_img_path)

#pages
if condition == 'Introduction':
    st.image(google_play_store_img, caption='Windows 11 introduces support on Google Play')
    st.write("""
             In today's world, apps has been playing an important role in every one's daily life. 
             From Ecommerce apps, to social media apps to entertainment mobile apps, it is nearly impossible for us to stay away from any apps in our life.
             """)
    st.write("In this project, we analyse the Android Market and try to predict if a newly lanuched app can reach 1 Million downloads after 1 year of its release date.")
    st.markdown("[Project Link](https://github.com/limivann/app-performance-predictor)")
    st.text("")
    st.text("")
    st.text("")
    st.markdown("<p style='font-size:12px;text-align:right;'>Contributors: Ivan, Aaron, Yifei</p>",unsafe_allow_html=True)
elif condition == 'EDA':
    st.sidebar.write("Close this sidebar for full experience")
    title("Exploratory Data Analysis",30)
    st.write("This is the EDA on apps in google play store")
    header("Sample data after cleaning (100 apps)")
    AgGrid(df)
    title("Basic EDA",28)
    # chart 1
    header("Heatmap corelation between selected features")
    st.image(heatmap_img)
    
    # chart 2
    header("Tree map")
    components.html(treemap_html, height=450)
    
    # chart 3
    title("Installs group EDA",28)
    header("Distribution of installs group")
    chart3_col1, chart3_col2, chart3_col3 = st.columns([1,2,1])
    with chart3_col2:
        st.image(dist_installs_img, use_column_width="always")
    st.markdown("<p style='text-align:center'>Almost half the number of apps have installs between 100,000 and 10,000,000.</p>", unsafe_allow_html=True)
        
    # chart 4
    header("Installs group vs ratings")
    chart4_col1, chart4_col2, chart4_col3 = st.columns([1,2,1])
    with chart4_col2:
        st.image(installs_grp_rating_img, use_column_width="always")
    st.markdown("<p style='text-align:center'>Paid apps with more than 10M of installs are most likely to be rated higher and it's less spread out in the y-axis.</p>", unsafe_allow_html=True)

    # chart 5
    header("Installs group vs editors choice")
    chart5_col1, chart5_col2, chart5_col3, chart5_col4 = st.columns([1,4,2,1])
    with chart5_col2:
        st.image(installs_grp_ec_img, use_column_width="always")
    with chart5_col3:
        st.markdown("<p style='font-size:14px;padding-top:40%;font-weight:bold'>Percentage of apps that are awarded Editors's Choice in each install group:</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Between 100K and 10M : 1.02 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Less than 100K : 0.10 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>More than 10M : 4.93 %</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Most of the app are not awarded with 'Editor's Choice'. But there's a slight increase in the likeliness of an app being an 'Editor's Choice' app if they have more installs.</p>", unsafe_allow_html=True)

    # chart 6
    header("Installs group vs free")
    chart6_col1, chart6_col2, chart6_col3, chart6_col4 = st.columns([1,4,2,1])
    with chart6_col2:
        st.image(installs_grp_free_img, use_column_width="always")
    with chart6_col3:
        st.markdown("<p style='font-size:14px;padding-top:40%;font-weight:bold'>Percentage of apps that are free in each install group:</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Between 100K and 10M : 91.76 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Less than 100K : 44.08 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>More than 10M : 99.91 %</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Apps that has more than 100K of installs are more likely to be free. Apps that has less installs are less likely to be free because the majority of players don't play paid games. If an app is paid, it's more likely to have less than 100K of installs.</p>", unsafe_allow_html=True)

    # chart 7
    header("Installs group vs ad supported")
    chart7_col1, chart7_col2, chart7_col3, chart7_col4 = st.columns([1,4,2,1])
    with chart7_col2:
        st.image(installs_grp_ads_img, use_column_width="always")
    with chart7_col3:
        st.markdown("<p style='font-size:14px;padding-top:40%;font-weight:bold'>Percentage of apps that have advertisement in each install group:</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Between 100K and 10M : 55.23 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Less than 100K : 20.53 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>More than 10M : 76.58 %</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Apps that has more than 100K of installs are more likely to be ad-supported as the developer company might need a source of income to maintain the company and game. </p>", unsafe_allow_html=True)

    # chart 8
    header("Installs group vs in app purchases")
    chart8_col1, chart8_col2, chart8_col3, chart8_col4 = st.columns([1,4,2,1])
    with chart8_col2:
        st.image(installs_grp_iap_img, use_column_width="always")
    with chart8_col3:
        st.markdown("<p style='font-size:14px;padding-top:40%;font-weight:bold'>Percentage of apps that have in app purchases in each install group:</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Between 100K and 10M : 63.11 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>Less than 100K : 36.37 %</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px;'>More than 10M : 76.56 %</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>It's quite common to have in-app purchases for games that are popular. Apps with higher traction (more installs) will plan to make profit through in app purchases. </p>", unsafe_allow_html=True)


    # chart 9
    header("Installs group vs content rating")
    chart9_col1, chart9_col2, chart9_col3 = st.columns([1,2,1])
    with chart9_col2:
        st.image(installs_grp_cr_img, use_column_width="always")
    st.markdown("<p style='text-align:center'>Most of the app in this dataset are for everyone. And 'Adults' apps are significantly low in all install groups, especially for apps more than 10M of installs.</p>", unsafe_allow_html=True)

    # chart 10
    header("Installs group vs days since update")
    chart10_col1, chart10_col2, chart10_col3 = st.columns([1,6,1])
    with chart10_col2:
        components.html(installs_grp_dsu_html, height=500)
    st.markdown("<p style='text-align:center'>Most of the apps are updated more than 6 months ago or within 1 month. This are the polar opposites, which means good apps are more likely to be updated 1-3 months. But poor apps are not that frequently updated.</p>", unsafe_allow_html=True)

    # chart 11
    chart11_col1, chart11_col2, chart11_col3 = st.columns([1,2,1])
    with chart11_col2:
        st.image(installs_grp_dsu_img, use_column_width="always")
    st.markdown("<p style='text-align:center'>Apps with less than 100K of installs typically are less updated. As the last update is like more than 6 months ago. For apps with more than 100K installs, it's more frequently updated. Especially for apps more than 10M of installs, they are updated few days ago, or at most within 1 month ago.</p>", unsafe_allow_html=True)

    # chart 12
    header("Installs group vs review count")
    chart12_col1, chart12_col2, chart12_col3 = st.columns([1,20,1])
    with chart12_col2:
        components.html(installs_grp_rc_html, height=800)
    st.markdown("<p style='text-align:center'>There's a significant increase in installs as the apps get more review count. For apps with more than 10M installs have extreme amount of review count. But the distribution is quite even compared to the other 2 groups because the majority of the apps with 10M installs are dispersed in 1000 to 4000 reviews. This is considered a wide gap compared to apps with less than 100K installs.</p>", unsafe_allow_html=True)

    # chart 13
    header("Installs group vs rating rate")
    chart13_col1, chart13_col2, chart13_col3 = st.columns([1,2,1])
    with chart13_col2:
        st.image(installs_grp_rr_img, use_column_width="always")
    st.markdown("<p style='text-align:center'>Apps with less then 100K installs have low rating counts as well as low rating rates. As the installation count increases, the rating rate is increasing as well. (High rating rate means less than 50 and more than 10)</p>", unsafe_allow_html=True)

    # chart 14
    header("Installs group vs rating rate")
    chart14_col1, chart14_col2, chart14_col3 = st.columns([1,20,1])
    with chart14_col2:
        components.html(installs_grp_size_html, height=800)
    st.markdown("<p style='text-align:center'>Before removing outliers, the figure squeezed on the left side (positively skewed). After removing outliers, we can observe the size distribution better.</p>", unsafe_allow_html=True)

    # chart 15
    header("Installs group vs category")
    components.html(installs_grp_cat_html, height=600)
    st.markdown("<p style='text-align:center'>Game is highly saturated in this dataset.</p>", unsafe_allow_html=True)
    
    # chart 16
    chart16_col1, chart16_col2, chart16_col3 = st.columns([1,10,1])
    with chart16_col2:
        st.image(installs_grp_cat_free_img, use_column_width="always")
        
    st.text("")
    st.text("")
    st.markdown("<span style='font-weight:bold'>For more visualizations and eda, please refer to our project repo - </span>[link](https://github.com/limivann/app-performance-predictor)", unsafe_allow_html=True)

    
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
    