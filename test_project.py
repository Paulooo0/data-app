from project import get_data, statistics, commercial_attributes
import pandas as pd  # It's necessary import pandas to test the dataset
import numpy as np # It's necessary import numpy to test statistics function


path = 'dataset/kc_house_data.csv'
def test_get_data():
    data = get_data(path)
    assert (data.loc[1, 'price'])    == 538000.0
    assert (data.loc[1, 'bedrooms']) == 3
    assert (data.loc[1, 'floors'])   == 2.0
    assert (data.loc[1, 'yr_built']) == 1951


def test_statistics():
    data = pd.read_csv(path)
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    mean = pd.DataFrame(num_attributes.apply(np.mean))
    median = pd.DataFrame(num_attributes.apply(np.median))
    min_ = pd.DataFrame(num_attributes.apply(np.min))
    max_ = pd.DataFrame(num_attributes.apply(np.max))
    std = pd.DataFrame(num_attributes.apply(np.std))
    df1 = pd.concat([max_, min_, mean, median, std], axis=1).reset_index()
    df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std' ]
    
    assert (df1.loc[1, 'attributes']) == 'price'
    assert (df1.loc[1, 'max'])        == 7700000.0
    assert (df1.loc[1, 'min'])        == 75000.0
    assert (df1.loc[1, 'mean'])       == 540088.1417665294
    assert (df1.loc[1, 'median'])    == 450000.0
    assert (df1.loc[1, 'std'])        == 367118.7031813723


def test_commercial_attributes():
    data = get_data(path)
    groupby = data[['yr_built', 'price']].groupby('yr_built').mean()
    assert groupby.size == 116
    assert groupby.columns[0] == 'price'