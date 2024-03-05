# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:08:44 2024

@author: saketh
"""

import pandas as pd
import joblib
import streamlit as st
from PIL import Image
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load the preprocessed training data
train_data = pd.read_csv("updated_X.csv")

# Instantiate OneHotEncoder
one_hot = OneHotEncoder()
categorical_values = ['OverallQual', 'GarageCars', 'TotRmsAbvGrd', 'Neighborhood', 'FullBath', 'GarageType']
transformer = ColumnTransformer([('one_hot', one_hot, categorical_values)],
                                  remainder='passthrough')
transformer.fit(train_data)

# Function to transform input data
def transform_data(transformer, data):
    transform_X = transformer.transform(data).toarray()
    transformed_df = pd.DataFrame(transform_X)
    return transformed_df

# Load the trained model
loaded_model = joblib.load("best_model.sav")

# Function to predict house prices
def house_price_prediction(input_data):
    transformed_data = transform_data(transformer, input_data)
    predictions = loaded_model.predict(transformed_data)
    return predictions

# Define meaningful labels for categorical options
options_names = {
    'OverallQual': {
        10: 'Very Excellent',
        9: 'Excellent',
        8: 'Very Good',
        7: 'Good',
        6: 'Above Average',
        5: 'Average',
        4: 'Below Average',
        3: 'Fair',
        2: 'Poor',
        1: 'Very Poor'
    },
    'GarageCars': {
        0: '0 cars',
        1: '1 car',
        2: '2 cars',
        3: '3 cars',
        4: '4 cars'
    },
    'TotRmsAbvGrd': {
        2: '2 rooms',
        3: '3 rooms',
        4: '4 rooms',
        5: '5 rooms',
        6: '6 rooms',
        7: '7 rooms',
        8: '8 rooms',
        9: '9 rooms',
        10: '10 rooms',
        11: '11 rooms',
        12: '12 rooms',
        13: '13 rooms',
        14: '14 rooms'
    },
    'Neighborhood': {
        'NAmes': 'North Ames',
        'CollgCr': 'College Creek',
        'OldTown': 'Old Town',
        'Edwards': 'Edwards',
        'Somerst': 'Somerset',
        'Gilbert': 'Gilbert',
        'NridgHt': 'Northridge Heights',
        'Sawyer': 'Sawyer',
        'NWAmes': 'Northwest Ames',
        'SawyerW': 'Sawyer West',
        'BrkSide': 'Brookside',
        'Crawfor': 'Crawford',
        'Mitchel': 'Mitchell',
        'NoRidge': 'Northridge',
        'Timber': 'Timberland',
        'IDOTRR': 'Iowa DOT and Rail Road',
        'ClearCr': 'Clear Creek',
        'StoneBr': 'Stone Brook',
        'SWISU': 'South & West of Iowa State University',
        'MeadowV': 'Meadow Village',
        'Blmngtn': 'Bloomington Heights',
        'BrDale': 'Briardale',
        'Veenker': 'Veenker',
        'NPkVill': 'Northpark Villa',
        'Blueste': 'Bluestem'
    },
    'FullBath': {
        0: '0 bathrooms',
        1: '1 bathroom',
        2: '2 bathrooms',
        3: '3 bathrooms'
    },
    'GarageType': {
        '2Types': 'More than one type',
        'Attchd': 'Attached',
        'Basment': 'Basement',
        'BuiltIn': 'Built-In',
        'CarPort': 'Car Port',
        'Detchd': 'Detached',
        'missing': 'No Garage'
    }
}

# Streamlit interface
def main():
    st.markdown(
        """
        <style>
        .stApp {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<h1>House Price Prediction</h1>", unsafe_allow_html=True)
    st.write("**By Saketh Yalamanchili**  \n[GitHub](https://github.com/sakethyalamanchili) | [LinkedIn](https://www.linkedin.com/in/saketh05/)")
    st.markdown("##### **Welcome to the House Price Prediction App.**")
    
    # Preload the image
    image = Image.open("houses_image.jpg")

    # Display the image with centered alignment
    st.image(image)
    
    st.sidebar.header("House Details")

    features = {
        'OverallQual': 'Overall Quality',
        'GrLivArea': 'Above Ground Living Area (sqft)',
        'TotalBsmtSF': 'Total Basement Area (sqft)',
        '2ndFlrSF': 'Second Floor Area (sqft)',
        'BsmtFinSF1': 'Basement Finished Area (sqft)',
        '1stFlrSF': 'First Floor Area (sqft)',
        'GarageCars': 'Number of Garage Cars',
        'GarageArea': 'Garage Area (sqft)',
        'LotArea': 'Lot Area (sqft)',
        'TotRmsAbvGrd': 'Total Rooms Above Ground',
        'Age': 'Age of House',
        'Neighborhood': 'Neighborhood',
        'YearRemodAdd': 'Year of Remodeling',
        'MasVnrArea': 'Masonry Veneer Area',
        'BsmtUnfSF': 'Unfinished Basement Area (sqft)',
        'FullBath': 'Number of Full Bathrooms',
        'LotFrontage': 'Lot Frontage (ft)',
        'WoodDeckSF': 'Wood Deck Area (sqft)',
        'GarageYrBlt': 'Year Garage Built',
        'GarageType': 'Garage Type'
    }

    input_data = {}
    for feature, label in features.items():
        if feature == 'OverallQual':
            sorted_options = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            input_data[feature] = st.sidebar.selectbox(f"{label}:", sorted_options, format_func=lambda x: options_names[feature][x])
        elif feature in ['GarageCars', 'TotRmsAbvGrd', 'FullBath']:
            input_data[feature] = st.sidebar.selectbox(f"{label}:", sorted(train_data[feature].unique()), format_func=lambda x: options_names[feature][x])
        elif feature == 'Neighborhood':
            input_data[feature] = st.sidebar.selectbox(f"{label}:", sorted(train_data[feature].unique()), format_func=lambda x: options_names[feature][x])
        elif feature == 'GarageType':
            input_data[feature] = st.sidebar.selectbox(f"{label}:", sorted(train_data[feature].unique()), format_func=lambda x: options_names[feature].get(x, x))
        else:
            input_data[feature] = st.sidebar.number_input(f"{label}:", min_value=0.0, value=0.0)

    input_df = pd.DataFrame([input_data])

    if st.sidebar.button("Calculate Estimated Price"):
        predicted_price = house_price_prediction(input_df)
        st.write("### Estimated House Price: $", round(predicted_price[0], 2))
        

if __name__ == "__main__":
    main()
