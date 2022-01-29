from asyncio import events
from time import time
from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, User, Venue


def all_events(request):
    event_list = Event.objects.all()
    return render(request, 
        "events/event_list.html", 
        {
            "event_list": event_list
        })


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Raj"
    month = month.capitalize()
    # Convert Month name to Number
    month_no = list(calendar.month_name).index(month)
    month_no = int(month_no)

    #Create Calendar
    cal = HTMLCalendar().formatmonth(year, month_no)

    #Get current year
    now = datetime.now()
    current_year = now.year

    #Get current time
    time = now.strftime("%H:%M %p")

    return render(request, 
        'events/home.html', 
        {
            "name": name,
            "month": month,
            "year": year,
            "month_no": month_no,
            "cal": cal,
            "current_year": current_year,
            "time": time,
        })