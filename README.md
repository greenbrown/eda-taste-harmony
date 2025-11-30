# 🍷 Taste Harmony --- Wine & Food Pairing Explorer

Exploratory Data Analysis (EDA) & Interactive Streamlit App

Taste Harmony is a data exploration project and interactive application
designed to analyze wine reviews and food pairings using a public Kaggle
dataset. The app helps users explore wine characteristics, suitable food
pairings, and top 3 insights based on selected filters.

## Features

### EDA (Exploratory Data Analysis)

-   Wine price distribution
-   Points (rating) distribution
-   Top wine-producing countries
-   Most frequent words in wine descriptions
-   Relationship between price and rating

### Streamlit App

[https://wine-taste-harmony.streamlit.app/](https://wine-taste-harmony.streamlit.app/)
-   Filters: Wine 
-   Interactive visualizations using Plotly
-   Automatic Top 3 Insight Summary based on active filters
-   Clean sidebar layout with static footer
-   Responsive UI design

## Project Structure

    eda-taste-harmony/
    │
    ├── app.py
    ├── data/
    │   └── wine_reviews.csv
    ├── notebooks/
    │   └── eda_wine.ipynb
    ├── requirements.txt
    └── README.md

## Dataset

Dataset source: Kaggle (Wine Reviews)

Contains: - Price - Variety - Country - Winery - Descriptions - Points
(ratings)

## How to Run Locally

### 1. Clone Repository

    git clone https://github.com/greenbrown/eda-taste-harmony.git
    cd eda-taste-harmony

### 2. Create Virtual Environment

    python3 -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate    # Windows

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Run the Streamlit App

    streamlit run app.py

## EDA Notebook

Located in:

    notebooks/eda_wine.ipynb

Includes: - Missing value analysis - Statistical summaries - Wordcloud
visualization - Price distribution - Correlation heatmaps

## Insight Summary (Top 3)

The app automatically generates Top 3 insights based on user filters: -
Most popular variety - Highest-rated wine - Most common price range

## Tech Stack

-   Python 3.10+
-   Pandas, NumPy
-   Plotly
-   Streamlit
-   Scikit-learn
-   Jupyter Notebook

## Future Improvements

-   RAG integration for wine recommendation
-   Clustering based on flavor profiles
-   Food-topic classification model
-   Multi-page Streamlit layout

## Author

Lidya\
Wine & Food Enthusiast • Data Explorer 

Repository: https://github.com/greenbrown/eda-taste-harmony/
