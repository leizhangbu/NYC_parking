


## This is a project in TDI( The Data Incubator, Fall 2020)
## Requirements:
### 1. Business Objective

The project is to help drivers find better street parking locations with less risk of parking tickets. The product is a web app https://nyc-parking-map.herokuapp.com/. User can type in a location in NYC, select a time and date this user want to park, then the app will return a local map where streets' parking risk plotted in color. 


### 2. Data Source
1. Parking Tickets  from NYC Department of Finance.
2. Boundaries of Police Precincts from DATA.GOV.
4. NYC Street Centerline geometry data from NYC open data.
5. Address location from Openstreetmap API.

### 3. Visualization
The major and most important visualization is a interactive map with streets plotted in color.


### 4a. Machine learning
I employ a tree regression model ( light gbm) to build a model and analyze feature importance. The training with processed data is shown in part 1 of file Training_process.ipynb. The processing of data for training and prediction is illustrated in the second part.
### 4c. Interactive Website
The interactive website is in https://nyc-parking-map.herokuapp.com/
where user can type in location choose time and date up to seven days.



### Install

	$ python3 -m venv venv && source venv/bin/activate
	$ pip install -r requirements.txt


### Run 

	$ python app.py
	# browse to http://127.0.0.1:5000/

