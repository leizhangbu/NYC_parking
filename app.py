from flask import Flask, render_template, render_template_string, request, redirect
import plotly
import plotly.graph_objs as go
from geopy import Nominatim
import pandas as pd
import numpy as np
import json
import plotly.express as px
import dill
from plot_street import plot_overview, create_plot

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        bar = plot_overview()
        return render_template('index.html',plot=bar)
    else:
        location_name = request.form['location']
        bar = create_plot(location_name)
        return render_template('index.html', plot=bar)
        #tz_list = ['All','Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        #return render_template('explore.html',tz_list=tz_list)

@app.route('/Explore_more', methods=['GET', 'POST'])
def dropdown():
    bar = plot_overview()
    if request.method == "POST":
        DoW = request.form.get("DoW", None)
        if DoW!=None:
            print(DoW)
            return render_template("test.html", week_day = DoW,plot=bar)
    return render_template("test.html",plot=bar)


if __name__ == '__main__':
    app.run()


