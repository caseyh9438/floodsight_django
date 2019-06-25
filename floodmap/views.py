from django.shortcuts import render
from .forms import AddMarkerForm
from .models import AddMarker

import json
import datetime

from django_pandas.io import read_frame
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect

def map(request):
    events = AddMarker.objects.all()
    ##request.GET used to filter events
    #form = QueryForm(request.GET or None)
    #paramDict = request.GET

    #events = filter_events(events, paramDict)

    # This takes the first event query an reformats the data so it can be read
    # by the map script on the frontend.

    ##Turns Django Query Set to Data Frame and iterates through AddEvent model and formats Location input into Lat and Log to map
    # qs = AddEvent.objects.all()
    # Every_Event = read_frame(qs, fieldnames=[ 'City', 'Name_of_Organization', 'Name_of_Event', 'Date_time', 'Description', 'Registration_Link'])
    # rows = next(Every_Event.iteritems())[1]

    # geolocator = Nominatim(user_agent="HD GEM")

    # geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0)
    # location = Every_Event['City'].apply(geocode)
    # point = location.apply(lambda loc: tuple(loc.point) if loc else None)
    # point = point.tolist()
    # lat, lon, nop = zip(*point)
    # lat= str(lat).strip('()')
    # lat = lat.split(",")
    # lat = list(lat)
    # lat = [float(i) for i in lat]
    # lat = { i : lat[i] for i in range(0, len(lat) ) }
    # lon= str(lon).strip('()')
    # lon = lon.split(",")
    # lon = list(lon)
    # lon = [float(i) for i in lon]
    # lon = { i : lon[i] for i in range(0, len(lon) ) }



    ##
    map_events = [{'loc':[float(AddEvent.lat), float(AddEvent.lon)],
                   'title':AddEvent.users_name,
                   'location_':AddEvent.location,
                   'descriptions':AddEvent.description} for AddEvent in events]

    ##This convertes 'date' into a JSON serializable string##
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
    ##
    form = AddMarkerForm()

    context = {
        'events':events,
        # Here, we apply `json.dumps`, `escapejs` and `marksafe` for security
        # and proper formatting
        'map_events': mark_safe(escapejs(json.dumps(map_events, default = myconverter))),
        'form': form
    }

    # ##Removing oudated markers
    # all_dates = AddMarker.objects.values('Date_time')
    # all_dates = read_frame(all_dates)
    # all_dates = all_dates.values.tolist()
    #
    # for date in all_dates:
    #     date_string = str(date).strip('[]').strip('datetime.date').strip('()')
    #     date_list2 = date_string.split(",")
    #     date_list1 = [x.strip(' ') for x in date_list2]
    #     date_list1.insert(1, '-')
    #     date_list1.insert(3, '-')
    #
    #     if len(date_list1[4]) == 1 and len(date_list1[2]) == 1:
    #         date_list3 = [x.strip(' ') for x in date_list2]
    #         date_list3.insert(1, '-')
    #         date_list3.insert(3, '-')
    #         date_list3.insert(4, '0')
    #         date_list3.insert(2, '0')
    #         date_string = ''.join(date_list3)
    #
    #         if date_string < str(datetime.datetime.today()):
    #             AddMarker.objects.filter(Date_time=date_string).delete()
    #
    #     if len(date_list1[2]) == 1:
    #         date_list4 = [x.strip(' ') for x in date_list2]
    #         date_list4.insert(1, '-')
    #         date_list4.insert(3, '-')
    #         date_list4.insert(2, '0')
    #         date_string = ''.join(date_list4)
    #
    #         if date_string < str(datetime.datetime.today()):
    #             AddMarker.objects.filter(Date_time=date_string).delete()
    #
    #     if len(date_list1[4]) == 1:
    #         date_list5 = [x.strip(' ') for x in date_list2]
    #         date_list5.insert(1, '-')
    #         date_list5.insert(3, '-')
    #         date_list5.insert(4, '0')
    #         date_string = ''.join(date_list5)
    #
    #         if date_string < str(datetime.datetime.today()):
    #             AddMarker.objects.filter(Date_time=date_string).delete()



    if request.GET.get('approved'):
        form = AddMarkerForm(data=request.POST)
        form.save()


    if request.method == 'POST':
        form = AddMarkerForm(data=request.POST)
        if form.is_valid():#request.POST.get('Name of Organization') and request.POST.get('Event Name') and request.POST.get('Registration Link') and request.POST.get('Event Description'):
            new_event = form.save()
            new_event.set_coordinates()
            # email = send_mail(
            #     "New submit form submission",
            #     'Test email',#"<html><body>{% form %}<form action='www.hdgem.org/eventmap' method='GET'><button name='approved' value='Approved'>Approve</button><br><button value='Deny'>Deny</button></form></body></html>",
            #     "HD GEM" + ' New Event Added',
            #     ['caseyh9438@gmail.com'],
            #     fail_silently=False
            # )
            # email

            #If given a bad location, lat and lon defaults to 32.076179, -81.088379
            #Default lat exsists to avoid map crash, but I don't want them to post on map
            #Deleting entries with the default lat so they do not post on Map
            x = str(AddMarker.objects.filter(lat=42.076179))
            if 'AddEvent object' in x:
                q1 = AddMarker.objects.get(lat=42.076179)
                q1.delete()

        return HttpResponseRedirect('', context)

    else:
        return render(request, 'index.html', context)