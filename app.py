from flask import Flask, render_template, render_template_string, request, redirect
import plotly
import plotly.graph_objs as go
from geopy import Nominatim
import pandas as pd
import numpy as np
import json
import plotly.express as px
import dill
from plot_street import plot_overview, create_plot,plot_weekday
from datetime import date,timedelta


app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    today=date.today()
    date_list =[today+timedelta(days=i) for i in range(7)]
    date_list = [str(today.month)+'-'+str(today.day) for today in date_list]
    if request.method == 'GET':
        location_name = 'Krupa Grocery'
        daytime = 'daytime'
        weekday=-1
        bar = create_plot(location_name,daytime,weekday)
    else:
        location_name = request.form['location']
        daytime = request.form['daytime']
        weekday = request.form['weekday']
        #print(request.form['parking_type'])
        bar = create_plot(location_name,daytime,weekday)

    return render_template('index.html',\
     plot=bar,location=location_name,\
     daytime=daytime,weekday=weekday,
     date_list = date_list)



if __name__ == '__main__':
    app.run()


