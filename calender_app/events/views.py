from asyncio import events
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
import calendar
import csv
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue

# Import User Model From Django
from django.contrib.auth.models import User

from .forms import VenueForm, EventForm, EventFormAdmin
from django.contrib import messages

#PDF Import
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator


# Venue CRUD Functions...
def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            Venue.owner = request.user.id # Logged in User
            venue.save()
            #form.save()
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


def list_venues(request):
    #venue_list = Venue.objects.all().order_by('name')
    venue_list = Venue.objects.all()

    # Set up pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    return render(request, 
        "events/venues.html", 
        {
            "venue_list": venue_list,
            "venues": venues,
            "nums": nums,
        })


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')
    return render(request, 
        "events/update_venue.html", 
        {
            "venue": venue,
            "form": form,
        })


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 
        "events/show_venue.html", 
        {
            "venue": venue,
            "venue_owner": venue_owner,
        })


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


# Eventes CRUD Functions....
def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                Event.manager = request.user # Logged in User
                event.save()
                #form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just going to Page...
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 
        "events/add_event.html", 
        {
            'form': form,
            'submitted': submitted
        })


def all_events(request):
    event_list = Event.objects.all().order_by('name')
    return render(request, 
        "events/event_list.html", 
        {
            "event_list": event_list
        })


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 
        "events/update_event.html", 
        {
            "event": event,
            "form": form,
        })


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted Successfully!!!"))
        return redirect('list-events')
    else:
        messages.success(request, ("Your aren't Authorized Person to Delete it!!"))
        return redirect('list-events')


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, "events/my_events.html", {
            "events": events
        })
    else:
        messages.success(request, ("Your aren't Authorized Person to View this Event!!"))
        return redirect('home')


# Generate Text file Venue List.....
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a Canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some line on text
    # lines = [
    #     "This is line 1",
    #     "This is line 1",
    #     "This is line 1",
    # ]

    # Designate the Model
    venues = Venue.objects.all()

    # Create Blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    # Loop the lines
    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


# Generate Text file Venue List.....
def venue_csv(request):
    response = HttpResponse(content_type='text/csc')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    
    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    venues = Venue.objects.all()

    # Add Column Heading
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Mobile No', 'Web Address', 'Email ID'])
   
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
    return response


# Generate Text file Venue List....
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate the Model
    venues = Venue.objects.all()

    # Loop Through and Output
    lines = []
    for venue in venues:
        lines.append(f'Venue Name: {venue.name}\nAddress: {venue.address}\nZipCode: {venue.zip_code}\nMobile No: {venue.phone}\nWeb Site: {venue.web}\nEmail ID: {venue.email_address}\n\n\n')

    response.writelines(lines)
    return response


# Home Page Function......
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

