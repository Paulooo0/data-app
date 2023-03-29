import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly.express as px
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(layout='wide')
st.cache(allow_output_mutation=True)

def main():
    data_overview()
    statistics()
    commercial_attributes()
    portfolio_density()

def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    return data

# Get data
path = 'C:/Data/dataset/kc_house_data.csv'
data = get_data(path)

# Add new features
data['price_m2'] = data['price'] / data['sqft_lot']

# Copy the dataframe
def data_copy():
    copy = data.copy()
    return copy


# Create buttons on side bar
f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
f_zipcode = st.sidebar.multiselect('Enter zipcode',
                                data['zipcode'].unique())

# Filters
st.sidebar.title('Commercial Options')

min_yr_built = int(data['yr_built'].min())
max_yr_built = int(data['yr_built'].max())

st.sidebar.subheader('Select max year built')
f_yr_built = st.sidebar.slider('Year Built', min_yr_built,
                                max_yr_built,
                                min_yr_built)

#======================
# Data Overview
#======================

def data_overview():
    data1 = data_copy()
    st.title('Data overview')
    if (f_zipcode != []) and (f_attributes != []):
        data1 = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

    elif (f_zipcode != []) and (f_attributes == []):
        data1 = data.loc[data['zipcode'].isin(f_zipcode), :]

    elif (f_zipcode == []) and (f_attributes != []):
        data1 = data.loc[:, f_attributes]

    else:
        data1 = data.copy() 
    st.dataframe(data1)
        
    
data2 = data_copy()
      
#======================
# Average values and descriptive analysis
#======================
def statistics():
    # ------------- Average values
    df1 = data2[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data2[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data2[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data2[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    st.title('Statistics')
    # Create 2 columns
    c1, c2 = st.columns((1, 1))
    
    # Merge
    m1 = pd.merge(df1,df2, on='zipcode', how='inner')
    m2 = pd.merge(m1,df3, on='zipcode', how='inner')
    df = pd.merge(m2,df4, on='zipcode', how='inner')

    df.columns = ['zipcode', 'total houses',
                'price', 'sqft living', 'price/m2']

    c1.header('Average values')
    if (f_zipcode != []):
        df = df.loc[df['zipcode'].isin(f_zipcode)]
    c1.dataframe(df, height=600, width=600)

    # ------------- Descriptive analysis
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    mean = pd.DataFrame(num_attributes.apply(np.mean))
    median = pd.DataFrame(num_attributes.apply(np.median))
    min_ = pd.DataFrame(num_attributes.apply(np.min))
    max_ = pd.DataFrame(num_attributes.apply(np.max))
    std = pd.DataFrame(num_attributes.apply(np.std))

    df1 = pd.concat([max_, min_, mean, median, std], axis=1).reset_index()

    df1.columns = ['attributes', 'max', 'min', 'mean', 'meadian', 'std' ]

    c2.header('Descriptive analysis')
    c2.dataframe(df1, height=600, width=800)

#======================
# Portfolio density
#======================
def portfolio_density():
    st.title('Region Overview')
    st.header('Portfolio Density')

    df = data.sample(1000)

    # ------------- Base map - Folium
    density_map = folium.Map(location=[data['lat'].mean(),
                            data['long'].mean()],
                            default_zoom_start=15
                            )
    marker_cluster = MarkerCluster().add_to(density_map)
    for _, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                    popup= 'Price US{0} on: {1}. Features {2} sqft, {3} bedrooms, {4}'
                    'bathrooms, year built: {5}'.format(row['price'],
                                                        row['date'],
                                                        row['sqft_living'],
                                                        row['bedrooms'],
                                                        row['bathrooms'],
                                                        row['yr_built'])
                    ).add_to(marker_cluster)

    
    folium_static(density_map)

#==============================================
# House distribution per commercial categories
#==============================================
def commercial_attributes():
    # ------------- Average price by year
    st.title('Commercial Attributes')
    st.header('Average price per year built')

    # Data selection
    df = data.loc[data['yr_built']  < f_yr_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # Plot figure
    fig = px.line(df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    # ------------- Averege price by day
    df = data[['date', 'price']].groupby('date').mean().reset_index()
    fig = px.line(df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()