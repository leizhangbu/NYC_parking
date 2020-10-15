from flask import Flask, render_template_string
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def stats():
    lat = [19.368894, 19.378639, 19.356536,
           19.352141, 19.376943, 19.351838,
           19.377563, 19.340928, 19.319919,
           19.308241, 19.351663, 19.336423,
           19.350884]

    lon = [-99.005523, -99.107726, -99.101254,
           -99.041698, -99.058977, -99.091929,
           -99.071414, -99.061082, -99.119510,
           -99.066347, -99.010367, -99.050018,
           -98.996826]

    territoriales = ['ACATITLA-ZARAGOZA', 'ACULCO', 'ATLALILCO-AXOMULCO',
                     'AZTAHUACAN', 'CABEZA DE JUAREZ', 'ESTRELLA-HUIZACHEPETL',
                     'LEYES DE REFORMA', 'LOS ANGELES-AGRARISTA', 'LOS CULHUACANES',
                     'SAN LORENZO TEZONCO', 'SANTA CATARINA', 'SANTA CRUZ-QUETZALCOATL',
                     'TEOTONGO-ACAHUALTEPEC']

    dict_map = {'territorial': territoriales, 'lat': lat, 'lon': lon}
    geopd = pd.DataFrame.from_dict(dict_map)
    #print(geopd.head())

    px.set_mapbox_access_token('pk.eyJ1IjoiZ2ZlbGl4IiwiYSI6ImNrZTNsbnYzMTBraG0zMnFuZXNjOWZhdDgifQ.5sMKH7NQ6_oVyU4oJlcBUw')

    fig = px.scatter_mapbox(geopd, lat="lat", lon="lon", zoom=11, width=500, height=300,
                            text="territorial", center={'lat': 19.340928, 'lon': -99.061082})

    fig.update_layout(mapbox_style='outdoors', margin={"r": 0, "t": 0, "l": 0, "b": 0})

    div = fig.to_html(full_html=False)

    return render_template_string('''
<head>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
</head>
<body>
{{ div_placeholder|safe }}
</body>''', div_placeholder=div)

if __name__ == '__main__':
    app.run(debug=True) 