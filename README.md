# App Performance Predictor

Predicting an app performance using Data Science.

## About The Project

This is the mini project for SC1015 (Intro to Data Science and AI) which focuses on android market analysis and app perfomance predictor. For the entire walkthrough of the project, please view the notebooks in this order:

1. [Data Cleaning](https://github.com/limivann/app-rating-predictor/blob/main/data_cleaning.ipynb)
2. [Exploratory Data Analysis and Visualization](https://github.com/limivann/app-rating-predictor/blob/main/EDA.ipynb)
3. [Model Building](https://github.com/limivann/app-rating-predictor/blob/main/model_building.ipynb)
4. [Machine Learning](https://github.com/limivann/app-rating-predictor/blob/main/machine_learning.ipynb)

## Project Folder Structure

> Folder structure of our project

```terminal
.
├── datasets                          # csv files
├── google-play-scrapper              # web scraper for data preparation
├── presentation                      # presentation ppt
├── streamlit-app                     # website for model simulation
├── data_cleaning.ipynb               # notebook for data cleaning
├── EDA.ipynb                         # notebook for eda
├── machine_learning.ipynb            # notebook for machine learning
├── model_building.ipynb              # notebook for model building
└── README.md
```

## Problem Definition

- How different features of an app affect its popularity?
- Would an app exceed one million installs in a year after its release?

## Models Used

1. Decision Trees
2. Random Forest Classifier

## Key takeways from our primary EDA

1. More than half of the apps have 100K-100M installs.
2. The average rating of an app is 4.16
3. Apps with more than 10M installs have a higher chance to be chosen as Editor's Choice.
4. 99% of apps with more than 10M installs are free.
5. 77% of apps with more than 10M installs are ad-supported and has in-app purchases.
6. Apps with more than 10M installs are frequently updated, at most within a month.
7. Size has a strong linear relationship with install count.

## Streamlit Web App

For model simulation and visualization purposes, we have created a web app for this project. The link to the website is [here](https://app-performance-predictor.herokuapp.com/).

## Conclusion

1. Oversampling the data did not improved model performance due to overfitting.
2. We are able to achieve over 80% accuracy in predicting if an app would exceed one million installs in a year.
3. Strategies to increase the number of installs of an app may include:
   - Making the app free of charge
   - Increase the rating count of the app
   - Increase the review count if the app
4. The number of installs of an app does not depends entirely on its feature. It might depend on qualitative features such as reviews. Hence one thing that we could improve upon is to do sentimental analysis on the reviews using NLP.

## Contributors

- @limivann - Web Scraper, Model Building / Machine Learning, Streamlit Web App
- @lordAaron0121 - Data Cleaning, EDA and visualization
- @serphyshio - Data Cleaning, EDA and visualization

## References

- https://buildfire.com/app-statistics/
- https://www.npmjs.com/package/google-play-scraper
- https://developers.google.com/maps/documentation/places/web-service/overview
- http://shakedzy.xyz/dython/
- https://seaborn.pydata.org/api.html
- https://plotly.com/python/plotly-express/
- https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/
- https://www.kaggle.com/code/sociopath00/random-forest-using-gridsearchcv/notebook
- https://towardsdatascience.com/accuracy-precision-recall-or-f1-331fb37c5cb9
