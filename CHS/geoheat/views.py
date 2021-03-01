from django.shortcuts import render, get_object_or_404
# from .models import Measurement
# from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_zoom
import folium
import sqlite3
import pandas as pd
from folium.plugins import HeatMap

# Create your views here.
def calculate_heatmap_view(request):   
    db = sqlite3.connect('') # put name of database in here
    data = pd.read_sql_query("Select * from users",db)

    ip = '72.14.207.99' # get_ip_address(request)
    lat, lon = get_geo(ip)

    # location coordinates
    l_lat = lat
    l_lon = lon

    m = folium.Map(width=800, height=500, location=[l_lat, l_lon], zoom_start=8)
    folium.Marker([l_lat, l_lon], tooltip='click here for more',
                    icon=folium.Icon(color='purple')).add_to(m)
    
    heat_data = [ [row["lat"],row["long"]] for index,row in data]
    HeatMap(heat_data).add_to(m)
    m = m._repr_html_()

    context = {
        'map': m,
    }

    return render(request, 'geoheat.html', context)