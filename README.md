<h1 align="center">Data App</h1>

# Summary

* [Project Description](#Project-Description)
* [Functionalities and Demonstration](#Functionalities-and-Demonstration)
* [Project Access](#Project-Access)
* [Utilized Technologies ](#Utilized-Technologies)
* [Project Developer](#Project-Developer)
* [License](#License)
* [Conclusion](#Conclusion)

# Project Description

This project is a dashboard of the kc_data_house.csv dataset, using the streamlit to make the GUI and streamlit cloud to create a web application for this project. That can be accessed by this link: https://paulooo0-data-app-streamlit-app-cikoxf.streamlit.app.


# Functionalities and Demonstration

`Feature 1` - Data Overview

* Shows you all the elements in this dataframe, that can be filtered by the 2 buttons on side bar, which I will talk about soon.


`Feature 2` - Statistics

* Average values: based on the zipcodes, shows you the average data, referent each zipcode. And can be filtered by the zipcode button on side bar.
* Descriptive analysis: shows the statistics of each attribute on dataframe.


`Feature 3` - Side bar

* Have 2 buttons, one can filter by the zipcode, and another can filter by column name. Also have a slide bar that can filter by the maximum year built.

`Feature 4` - Portfolio density

* Shows an interactive map, in each point on the map can be seen the attributes of each property.

`Feature 5` - Commercial attributes

* Average price by year built: shows a line graph (price x yr_built) that can be filtered by a slider bar.
* Average price by day: shows a line graph referent the medium price per day in a certain period (05/2014-05/2015).
