from django.db import models
from geopy.geocoders import Nominatim, ArcGIS
from django_pandas.io import read_frame
from geopy.extra.rate_limiter import RateLimiter
import datetime

# Create your models here.


class AddMarker(models.Model):
    users_name = models.CharField(max_length=120)
    # Name_of_Event = models.CharField(max_length=200)
    location = models.CharField(max_length=500)
    # Date_time = models.DateField(default=datetime.datetime.today().strftime('%Y-%m-%d'), auto_now=False, auto_now_add=False, null=True)
    # Registration_Link = models.URLField(max_length=200)
    description = models.TextField(max_length=10000)
    lat = models.DecimalField(decimal_places=6, max_digits=20, null=True, default=32.076179)
    lon = models.DecimalField(decimal_places=6, max_digits=20, null=True, default=-81.088379)
    # Authorization_token = models.CharField(max_length=20)

    def set_coordinates(self):
        coordinates_updated = False
        Every_Event = read_frame(AddMarker.objects.filter(id=self.id), fieldnames=[ 'location', 'users_name', 'description'])
        geolocator = Nominatim(user_agent="HD GEM")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0)
        location = Every_Event['location'].apply(geocode)
        point = location.apply(lambda loc: tuple(loc.point) if loc else None)
        point = point.tolist()
        if point == [None]:
            point = [(32.076179), (-81.088379), (0)]
            lat, lon, nop = point[0], point[1], point[-1]
            lat= str(lat).strip('()').strip(',')
            lat = float(lat)
            if lat and self.lat != lat:
                self.lat = lat
                coordinates_updated = True
            #lat = lat.split(",")
            # lat = list(lat)
            # lat = [float(i) for i in lat]
            # lat = { i : lat[i] for i in range(0, len(lat) ) }
            lon= str(lon).strip('()').strip(',')
            lon = float(lon)
            if lon and self.lon != lon:
                self.lon = lon
                coordinates_updated = True
        # lon = lon.split(",")
        # lon = list(lon)
        # lon = [float(i) for i in lon]
        # lon = { i : lon[i] for i in range(0, len(lon) ) }
            if coordinates_updated:
                self.save()

        else:
            lat, lon, nop = zip(*point)
            lat= str(lat).strip('()').strip(',')
            lat = float(lat)
            if lat and self.lat != lat:
                self.lat = lat
                coordinates_updated = True
            #lat = lat.split(",")
            # lat = list(lat)
            # lat = [float(i) for i in lat]
            # lat = { i : lat[i] for i in range(0, len(lat) ) }
            lon= str(lon).strip('()').strip(',')
            lon = float(lon)
            if lon and self.lon != lon:
                self.lon = lon
                coordinates_updated = True
        # lon = lon.split(",")
        # lon = list(lon)
        # lon = [float(i) for i in lon]
        # lon = { i : lon[i] for i in range(0, len(lon) ) }
            if coordinates_updated:
                self.save()

        return self.lat, self.lon

    def get_coordinates(self, force_reset=False):
        lat = self.lat
        lon = self.lon
        if not lat or not lon or force_reset:
            lat, lon = self.set_coordinates()

        return lat, lon