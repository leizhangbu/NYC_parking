from flask import Flask, render_template, render_template_string, request, redirect
import plotly
import plotly.graph_objs as go
from geopy import Nominatim
import pandas as pd
import numpy as np
import json
import plotly.express as px
import dill

dict_average = dill.load(open('data/dict_average.pkd','rb'))
df_street = dill.load(open('data/df_street.pkd', 'rb'))
street_code_dic = dill.load(open('data/streetcode_dic_full.pkd', 'rb'))
geolocator = Nominatim(user_agent="lz-application")


def nearby_locations(Street_str,df_street,size =0.015):
    location = geolocator.geocode(Street_str+' NYC')
    if not location:
        return []
    else:
        #df_street['distance'] = np.sqrt((df_street.location_x-location.latitude)**2+(df_street.location_y-location.longitude)**2)
        df_street=df_street[(df_street.location_x<(location.latitude+size))& (df_street.location_x>(location.latitude-size))\
                           &(df_street.location_y<(location.longitude+size))&(df_street.location_y>(location.longitude-size))]
        return df_street, location

def get_fig(location, streets_code,dict_average):
    fig = go.Figure(data=[go.Scattermapbox(lat=[location.latitude], lon=[location.longitude])])
    #fig.add_annotation(text='Your Destination')
    layer_list=[]
    for street_code in streets_code:
        if street_code in dict_average:
            N_v = dict_average[street_code]
        else:
            N_v=0
        if N_v >300:
            color = 'red'
        elif N_v >200:
            color = 'orange'
        elif N_v >100:
            color = 'yellow'
        else:
            color = 'green'
        for geo in street_code_dic[str(street_code)]:
            layer_list.append({
                        'sourcetype': 'geojson',
                        'source': geo,#['geojson'],
                        'type': 'line',
                        'color':color,
                        'opacity':0.6,
                        'line':dict(width=6,)
                    })
    mapbox_access_token='pk.eyJ1IjoiZ2ZlbGl4IiwiYSI6ImNrZTNsbnYzMTBraG0zMnFuZXNjOWZhdDgifQ.5sMKH7NQ6_oVyU4oJlcBUw'
    fig.update_layout(
        autosize=False,
        width=800,
        height=400,
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            style="open-street-map", 
            zoom=15, 
            center_lat =location.latitude,
            center_lon = location.longitude,
            layers=layer_list
        )
    )
    return fig

def create_plot(location_name,daytime):
    if daytime=='daytime':
        dict_average = dill.load(open('data/dict_average.pkd','rb'))
    elif daytime=='Morning':
        dict_average = dill.load(open('data/dict_morning_average.pkd','rb'))
    elif daytime=='Noon':
        dict_average = dill.load(open('data/dict_noon_average.pkd','rb'))
    elif daytime=='Afternoon':
        dict_average = dill.load(open('data/dict_aft_average.pkd','rb'))
    elif daytime=='Evening':
        dict_average = dill.load(open('data/dict_eve_average.pkd','rb'))

    Street_str = location_name#'Krupa Grocery'
    #print(location_name)
    street_nearby,location = nearby_locations(Street_str,df_street)
    streets_code = street_nearby.street.values
    streets_code = streets_code.astype(int)
    fig = get_fig(location, streets_code,dict_average)

    div = fig.to_html(full_html=False)

    return render_template_string('''
                                <head>
                                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
                                </head>
                                <body>
                                {{ div_placeholder|safe }}
                                </body>''', div_placeholder=div)


def plot_overview():
    df= pd.read_csv('data/precinct_violation.csv')
    policemap = json.load(open("data/police_precincts.geojson"))
    fig = px.choropleth_mapbox(df,
                            geojson=policemap,
                            locations="Precinct",
                            featureidkey="properties.Precinct",
                            color="Number of Violation",
                            color_continuous_scale='Hot',
                            range_color=(0, 5000),
                            mapbox_style="carto-positron",
                            zoom=9, center={"lat": 40.7, "lon": -73.9},
                            opacity=0.7,
                            hover_name="Info",
                            width=800, height=600
                            )
    fig.update_layout(coloraxis_showscale=False)
    div = fig.to_html(full_html=False)
    bar = render_template_string('''
                        <head>
                        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
                        </head>
                        <body>
                        {{ div_placeholder|safe }}
                        </body>''', div_placeholder=div)
    return bar

def plot_weekday(DoW):
    map_wd={'Mon':0,'Tue':1,'Wed':2,'Thu':3,'Fri':4,'Sat':5,'Sun':6}
    df= pd.read_csv('data/precinct_wd_violation.csv')
    df = df[df.weekday==map_wd[DoW]][['Precinct','Number of Violation','Info']]
    policemap = json.load(open("data/police_precincts.geojson"))
    fig = px.choropleth_mapbox(df,
                            geojson=policemap,
                            locations="Precinct",
                            featureidkey="properties.Precinct",
                            color="Number of Violation",
                            color_continuous_scale='Hot',
                            mapbox_style="carto-positron",
                            range_color=(0, 5000),
                            zoom=9, center={"lat": 40.7, "lon": -73.9},
                            opacity=0.7,
                            hover_name="Info",
                            width=800, height=600
                            )
    fig.update_layout(coloraxis_showscale=False)
    div = fig.to_html(full_html=False)
    bar = render_template_string('''
                        <head>
                        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
                        </head>
                        <body>
                        {{ div_placeholder|safe }}
                        </body>''', div_placeholder=div)
    return bar