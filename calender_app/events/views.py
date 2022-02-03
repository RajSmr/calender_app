from asyncio import events
from os import name
from re import search
from time import time
from django.shortcuts import render
from django.http import HttpResponseRedirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, User, Venue
from .forms import VenueForm


def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 
        "events/search_venues.html", 
        {
            'searched': searched,
            'venues': venues
        })
    else:
        return render(request, 
            "events/search_venues.html", 
            {
            
            })


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 
        "events/show_venue.html", 
        {
            "venue": venue
        })


def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 
        "events/venues.html", 
        {
            "venue_list": venue_list
        })



def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 
        "events/add_venue.html", 
        {
            'form': form,
            'submitted': submitted
        })



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