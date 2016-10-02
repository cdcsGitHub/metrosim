from django import forms
from django.shortcuts import render_to_response
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from random import choice
from stations import Station
from trains import Train
from collections import OrderedDict
import pyodbc
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.http import HttpResponse
from django.shortcuts import render
from dajaxice.core import dajaxice_functions
from django.http import HttpResponse, HttpResponseRedirect
import json

def get_line (string_variable):
	return string_variable.split()

def index(request):
	return render(request, 'input.html')

def charts(request):
	lines = ["Blue_Line", "Red_Line", "Orange_Line", "Green_Line", "Yellow_Line"]
	stations = [["Addison Road-Seat Pleasant", 38.886713, -76.893592, "Blue"], ["Anacostia", 38.862072, -76.995648, "Green"], ["Archives", 38.893893,-77.021902, "Green","Yellow"],
	["Arlington Cemetery", 38.884574,-77.063108, "Blue"], ["Ballston-MU", 38.882071,-77.111845, "Orange"], ["Benning Road", 38.890488,-76.938291, "Blue"],
	["Bethesda", 38.984282,-77.094431, "Red"], ["Braddock Road", 38.814009,-77.053763, "Blue", "Yellow"],  ["Branch Ave", 38.826995,-76.912134, "Green"],
	["Brookland-CUA", 38.933234,-76.994544, "Red"], ["Capitol Heights", 38.889757,-76.913382, "Blue"], ["Capitol South", 38.884968,-77.005137, "Blue", "Orange"],
	["Cheverly", 38.916520,-76.915427, "Orange"], ["Clarendon", 38.886373,-77.096963, "Orange"], ["Cleveland Park", 38.934703,-77.058226, "Red"],
	["College Park-U of MD", 38.978523,-76.928432, "Green"], ["Columbia Heights", 38.928672,-77.032775, "Green", "Yellow"], ["Congress Heights", 38.845334,-76.988170, "Green"],
	["Court House", 38.891499,-77.083910, "Orange"], ["Crystal City", 38.857790,-77.050589, "Blue", "Yellow"], ["Deanwood", 38.907734,-76.936177, "Orange"], ["Dunn Loring-Merrifield", 38.883015,-77.228939, "Orange"],
	["Dupont Circle", 38.909499,-77.043620, "Red"], ["East Falls Church", 38.885841,-77.157177, "Orange"], ["Eastern Market", 38.884124,-76.995334, "Blue", "Orange"], ["Eisenhower Avenue", 38.800313,-77.071173, "Yellow"],
	["Farragut North", 38.903192,-77.039766, "Red"], ["Farragut West", 38.901311,-77.039810, "Blue", "Orange"], ["Federal Center SW", 38.884958,-77.015860, "Blue", "Orange"], ["Federal Triangle", 38.893757,-77.028218, "Blue", "Orange"],
	["Foggy Bottom-GWU", 38.900599,-77.050273, "Blue", "Orange"], ["Forest Glen", 39.015413,-77.042953, "Red"], ["Fort Totten", 38.951777,-77.002174,"Green", "Yellow", "Red"],
	["Franconia-Springfield", 38.766129,-77.168797, "Blue"], ["Friendship Heights", 38.960744,-77.085969, "Red"], ["Gallery Pl-Chinatown", 38.898340,-77.021851, "Green", "Yellow", "Red"],
	["Georgia Ave-Petworth", 38.936077,-77.024728, "Green", "Yellow"],["Glenmont", 39.061713,-77.053410, "Red"], ["Greenbelt", 39.011036,-76.911362, "Green"],
	["Grosvenor-Strathmore", 39.029158,-77.104150, "Red"], ["Huntington", 38.793841,-77.075301, "Yellow"], ["Judiciary Square", 38.896084,-77.016643, "Red"], ["King St-Old Town", 38.806474,-77.061115,"Blue","Yellow"],
	["Landover", 38.934411,-76.890988, "Orange"], ["Largo Town Center", 38.900800,-76.844900, "Blue"], ["L'Enfant Plaza", 38.884775,-77.021964, "Blue", "Orange", "Green", "Yellow"],  ["McPherson Square", 38.901316,-77.033652, "Blue", "Orange"],
	["Medical Center", 38.999947,-77.097253, "Red"], ["Metro Center", 38.898303,-77.028099, "Blue", "Orange", "Red"], ["Minnesota Ave", 38.898284,-76.948042, "Orange"], ["Morgan Boulevard", 38.891300,-76.868200, "Blue"],
	["Mt Vernon Sq 7th St-Convention Center", 38.905604,-77.022256, "Green", "Yellow"], ["Navy Yard-Ballpark", 38.876588,-77.005086, "Green"], ["Naylor Road", 38.851187,-76.956565, "Green"], ["New Carrollton", 38.947674,-76.872144, "Orange"],
	["NoMa-Gallaudet U", 38.907407,-77.002961, "Red"], ["Pentagon", 38.869349,-77.054013, "Blue", "Yellow"], ["Pentagon City", 38.863045,-77.059507, "Blue", "Yellow"], ["Potomac Ave", 38.880841,-76.985721, "Blue", "Orange"],
	["Prince George's Plaza", 38.965276,-76.956182, "Green"], ["Rhode Island Ave", 38.920741,-76.995984, "Red"],["Rockville", 39.084215,-77.146424, "Red"], ["Ronald Reagan Washington National", 38.852985,-77.043805, "Blue","Yellow"],
	["Rosslyn", 38.896595,-77.071460, "Blue", "Orange"], ["Shady Grove", 39.119819,-77.164921, "Red"], ["Shaw-Howard U", 38.912919,-77.022194, "Green", "Yellow"], ["Silver Spring", 38.993841,-77.031321, "Red"],
	["Smithsonian", 38.888022,-77.028232, "Blue", "Orange"], ["Southern Avenue", 38.840974,-76.975360, "Green"], ["Stadium-Armory", 38.885940,-76.977485, "Blue", "Orange"], ["Suitland", 38.843891,-76.932022, "Green"],
	["Takoma", 38.975532,-77.017834, "Red"], ["Tenleytown-AU", 38.947808,-77.079615, "Red"], ["Twinbrook", 39.062359,-77.121113, "Red"], ["U Street", 38.916489,-77.028938, "Green", "Yellow"], ["Union Station", 38.897723,-77.006745, "Red"],
	["Van Dorn Street", 38.799193,-77.129407, "Blue"], ["Van Ness-UDC", 38.943620,-77.063511, "Red"], ["Vienna", 38.877693,-77.271562, "Orange"],["Virginia Square-GMU", 38.883310,-77.104267, "Orange"],
	["Waterfront", 38.876221,-77.017491, "Green"], ["West Falls Church", 38.900670,-77.189394, "Orange",], ["West Hyattsville", 38.954931,-76.969881, "Green"], ["Wheaton", 39.038558,-77.051098, "Red"],
	["White Flint", 39.048043,-77.113131, "Red"], ["Woodley Park", 38.924999,-77.052648, "Red"]]
	avg = []
	highest_average_stations = []
	lowest_average_stations = []
	stations_to_sort = {}
	highest_average_stations = sorted(stations_to_sort, key = stations_to_sort.get, reverse = True)[:5]
	lowest_average_stations = sorted(stations_to_sort, key = stations_to_sort.get)[:5]
	for i in highest_average_stations:
		avg.append(i)
		avg.append(stations_to_sort[i])
	for i in lowest_average_stations:
		avg.append(i)
		avg.append(stations_to_sort[i])
	return render(request, 'charts.html', {'array1':avg})

def pathFind(station):
	stationFound = []
	lines = ["Blue_Line", "Red_Line", "Orange_Line", "Green_Line", "Yellow_Line"]
	stations = [["Addison Road-Seat Pleasant", 38.886713, -76.893592, "Blue"], ["Anacostia", 38.862072, -76.995648, "Green"], ["Archives", 38.893893,-77.021902, "Green","Yellow"],
	["Arlington Cemetery", 38.884574,-77.063108, "Blue"], ["Ballston-MU", 38.882071,-77.111845, "Orange"], ["Benning Road", 38.890488,-76.938291, "Blue"],
	["Bethesda", 38.984282,-77.094431, "Red"], ["Braddock Road", 38.814009,-77.053763, "Blue", "Yellow"],  ["Branch Ave", 38.826995,-76.912134, "Green"],
	["Brookland-CUA", 38.933234,-76.994544, "Red"], ["Capitol Heights", 38.889757,-76.913382, "Blue"], ["Capitol South", 38.884968,-77.005137, "Blue", "Orange"],
	["Cheverly", 38.916520,-76.915427, "Orange"], ["Clarendon", 38.886373,-77.096963, "Orange"], ["Cleveland Park", 38.934703,-77.058226, "Red"],
	["College Park-U of MD", 38.978523,-76.928432, "Green"], ["Columbia Heights", 38.928672,-77.032775, "Green", "Yellow"], ["Congress Heights", 38.845334,-76.988170, "Green"],
	["Court House", 38.891499,-77.083910, "Orange"], ["Crystal City", 38.857790,-77.050589, "Blue", "Yellow"], ["Deanwood", 38.907734,-76.936177, "Orange"], ["Dunn Loring-Merrifield", 38.883015,-77.228939, "Orange"],
	["Dupont Circle", 38.909499,-77.043620, "Red"], ["East Falls Church", 38.885841,-77.157177, "Orange"], ["Eastern Market", 38.884124,-76.995334, "Blue", "Orange"], ["Eisenhower Avenue", 38.800313,-77.071173, "Yellow"],
	["Farragut North", 38.903192,-77.039766, "Red"], ["Farragut West", 38.901311,-77.039810, "Blue", "Orange"], ["Federal Center SW", 38.884958,-77.015860, "Blue", "Orange"], ["Federal Triangle", 38.893757,-77.028218, "Blue", "Orange"],
	["Foggy Bottom-GWU", 38.900599,-77.050273, "Blue", "Orange"], ["Forest Glen", 39.015413,-77.042953, "Red"], ["Fort Totten", 38.951777,-77.002174,"Green", "Yellow", "Red"],
	["Franconia-Springfield", 38.766129,-77.168797, "Blue"], ["Friendship Heights", 38.960744,-77.085969, "Red"], ["Gallery Pl-Chinatown", 38.898340,-77.021851, "Green", "Yellow", "Red"],
	["Georgia Ave-Petworth", 38.936077,-77.024728, "Green", "Yellow"],["Glenmont", 39.061713,-77.053410, "Red"], ["Greenbelt", 39.011036,-76.911362, "Green"],
	["Grosvenor-Strathmore", 39.029158,-77.104150, "Red"], ["Huntington", 38.793841,-77.075301, "Yellow"], ["Judiciary Square", 38.896084,-77.016643, "Red"], ["King St-Old Town", 38.806474,-77.061115,"Blue","Yellow"],
	["Landover", 38.934411,-76.890988, "Orange"], ["Largo Town Center", 38.900800,-76.844900, "Blue"], ["L'Enfant Plaza", 38.884775,-77.021964, "Blue", "Orange", "Green", "Yellow"],  ["McPherson Square", 38.901316,-77.033652, "Blue", "Orange"],
	["Medical Center", 38.999947,-77.097253, "Red"], ["Metro Center", 38.898303,-77.028099, "Blue", "Orange", "Red"], ["Minnesota Ave", 38.898284,-76.948042, "Orange"], ["Morgan Boulevard", 38.891300,-76.868200, "Blue"],
	["Mt Vernon Sq 7th St-Convention Center", 38.905604,-77.022256, "Green", "Yellow"], ["Navy Yard-Ballpark", 38.876588,-77.005086, "Green"], ["Naylor Road", 38.851187,-76.956565, "Green"], ["New Carrollton", 38.947674,-76.872144, "Orange"],
	["NoMa-Gallaudet U", 38.907407,-77.002961, "Red"], ["Pentagon", 38.869349,-77.054013, "Blue", "Yellow"], ["Pentagon City", 38.863045,-77.059507, "Blue", "Yellow"], ["Potomac Ave", 38.880841,-76.985721, "Blue", "Orange"],
	["Prince George's Plaza", 38.965276,-76.956182, "Green"], ["Rhode Island Ave", 38.920741,-76.995984, "Red"],["Rockville", 39.084215,-77.146424, "Red"], ["Ronald Reagan Washington National", 38.852985,-77.043805, "Blue","Yellow"],
	["Rosslyn", 38.896595,-77.071460, "Blue", "Orange"], ["Shady Grove", 39.119819,-77.164921, "Red"], ["Shaw-Howard U", 38.912919,-77.022194, "Green", "Yellow"], ["Silver Spring", 38.993841,-77.031321, "Red"],
	["Smithsonian", 38.888022,-77.028232, "Blue", "Orange"], ["Southern Avenue", 38.840974,-76.975360, "Green"], ["Stadium-Armory", 38.885940,-76.977485, "Blue", "Orange"], ["Suitland", 38.843891,-76.932022, "Green"],
	["Takoma", 38.975532,-77.017834, "Red"], ["Tenleytown-AU", 38.947808,-77.079615, "Red"], ["Twinbrook", 39.062359,-77.121113, "Red"], ["U Street", 38.916489,-77.028938, "Green", "Yellow"], ["Union Station", 38.897723,-77.006745, "Red"],
	["Van Dorn Street", 38.799193,-77.129407, "Blue"], ["Van Ness-UDC", 38.943620,-77.063511, "Red"], ["Vienna", 38.877693,-77.271562, "Orange"],["Virginia Square-GMU", 38.883310,-77.104267, "Orange"],
	["Waterfront", 38.876221,-77.017491, "Green"], ["West Falls Church", 38.900670,-77.189394, "Orange",], ["West Hyattsville", 38.954931,-76.969881, "Green"], ["Wheaton", 39.038558,-77.051098, "Red"],
	["White Flint", 39.048043,-77.113131, "Red"], ["Woodley Park", 38.924999,-77.052648, "Red"]]

	for i in stations:
		if(station == i[0]):
			stationFound.append(i)

	return stationFound

def runtrains(request):
	blue_line_left = OrderedDict([('Largo Town Center', 3),('Morgan Boulevard', 3),('Addison Road-Seat Pleasant', 3),('Capitol Heights', 3),
				  ('Benning Road', 4),('Stadium-Armory', 1),('Potomac Ave', 3),('Eastern Market', 3),('Capitol South', 3),
				  ('Federal Center SW', 3),("L'Enfant Plaza", 3),('Smithsonian', 3),('Federal Triangle', 1),('Metro Center', 1),
				  ('McPherson Square', 1),('Farragut West', 3),('Foggy Bottom-GWU', 3),('Rosslyn', 3),('Arlington Cemetery', 3),
				  ('Pentagon', 1),('Pentagon City', 3),('Crystal City', 3),('Ronald Reagan Washington National ', 5),('Braddock Road', 3),
				  ('King St-Old Town', 5),('Van Dorn Street', 6),('Franconia-Springfield', 6)])

	blue_line_right = OrderedDict([('Franconia-Springfield', 6) ,('Van Dorn Street', 6) ,('King St-Old Town', 5) ,('Braddock Road', 3) ,
				   ('Ronald Reagan Washington National ', 5) ,('Crystal City', 3) ,('Pentagon City', 3) ,('Pentagon', 1) ,
				   ('Arlington Cemetery', 3) ,('Rosslyn', 3) ,('Foggy Bottom-GWU', 3) ,('Farragut West', 3) ,('McPherson Square', 1) ,
				   ('Metro Center', 1) ,('Federal Triangle', 1) ,('Smithsonian', 3) ,("L'Enfant Plaza", 3) ,('Federal Center SW', 3) ,
				   ('Capitol South', 3) ,('Eastern Market', 3) ,('Potomac Ave', 3) ,('Stadium-Armory', 1) ,('Benning Road', 4) ,
				   ('Capitol Heights', 3) ,('Addison Road-Seat Pleasant', 3) ,('Morgan Boulevard', 3) ,('Largo Town Center', 3)])

	red_line_left = OrderedDict([('Glenmont', 3), ('Wheaton', 3),('Forest Glen', 3),('Silver Spring', 3),('Takoma', 3),('Fort Totten', 3),
				 ('Brookland-CUA', 3), ('Rhode Island Ave', 3), ('NoMa-Gallaudet U', 3), ('Union Station', 3),('Judiciary Square', 3),
				 ('Gallery Pl-Chinatown', 3),('Metro Center', 3),('Farragut North', 3),('Dupont Circle', 3),('Woodley Park', 3),
				 ('Cleveland Park', 3),('Van Ness-UDC', 3),('Tenleytown-AU', 3),('Friendship Heights', 3),('Bethesda', 3),
				 ('Medical Center', 3),('Grosvenor-Strathmore', 3),('White Flint', 3),('Twinbrook', 3),('Rockville', 3),
				 ('Shady Grove', 3)])

	red_line_right = OrderedDict([('Shady Grove', 3) ,('Rockville', 3) ,('Twinbrook', 3) ,('White Flint', 3) ,('Grosvenor-Strathmore', 3) ,
				  ('Medical Center', 3) ,('Bethesda', 3) ,('Friendship Heights', 3) ,('Tenleytown-AU', 3) ,('Van Ness-UDC', 3) ,
				  ('Cleveland Park', 3) ,('Woodley Park', 3) ,('Dupont Circle', 3) ,('Farragut North', 3) ,('Metro Center', 3) ,
				  ('Gallery Pl-Chinatown', 3) ,('Judiciary Square', 3) ,('Union Station', 3) ,('NoMa-Gallaudet U', 3) ,('Rhode Island Ave', 3) ,('Brookland-CUA', 3) ,
				  ('Fort Totten', 3) ,('Takoma', 3) ,('Silver Spring', 3) ,('Forest Glen', 3) ,('Wheaton', 3) ,('Glenmont', 3)])

	orange_line_left_1 = OrderedDict([('Largo Town Center', 3) ,('Morgan Boulevard', 3) ,('Addison Road-Seat Pleasant', 3) ,('Capitol Heights', 3) ,
					  ('Benning Road', 4) ,('Stadium-Armory', 1) ,('Potomac Ave', 3) ,('Eastern Market', 3) ,('Capitol South', 3) ,
					  ('Federal Center SW', 3) ,("L'Enfant Plaza", 3) ,('Smithsonian', 3) ,('Federal Triangle', 1) ,('Metro Center', 1) ,
					  ('McPherson Square', 1) ,('Farragut West', 3) ,('Foggy Bottom-GWU', 3) ,('Rosslyn', 3) ,('Court House', 3) ,
					  ('Clarendon', 1) ,('Virginia Square-GMU', 3) ,('Ballston-MU', 4) ,('East Falls Church', 3),('West Falls Church', 4),
					  ('Dunn Loring-Merrifield', 4),('Vienna', 4)])

	orange_line_right_1 = OrderedDict([('Vienna', 4),('Dunn Loring-Merrifield', 4),('West Falls Church', 4) ,('East Falls Church', 3) ,('Ballston-MU', 4) ,
					   ('Virginia Square-GMU', 3) ,('Clarendon', 1) ,('Court House', 3) ,('Rosslyn', 3) ,('Foggy Bottom-GWU', 3) ,('Farragut West', 3) ,
					   ('McPherson Square', 1) ,('Metro Center', 1) ,('Federal Triangle', 1) ,('Smithsonian', 3) ,
					   ("L'Enfant Plaza", 3) ,('Federal Center SW', 3) ,('Capitol South', 3) ,('Eastern Market', 3) ,('Potomac Ave', 3) ,('Stadium-Armory', 1) ,('Benning Road', 4) ,
					   ('Capitol Heights', 3) , ('Addison Road-Seat Pleasant', 3) ,('Morgan Boulevard', 3) ,('Largo Town Center', 3)])

	orange_line_left_2 = OrderedDict([('New Carrollton', 3) ,('Landover', 3) ,('Cheverly', 3) ,('Deanwood', 3) ,('Minnesota Ave', 4) ,
					  ('Stadium-Armory', 1) ,('Potomac Ave', 3) ,('Eastern Market', 3) ,('Capitol South', 3) ,('Federal Center SW', 3),
					  ("L'Enfant Plaza", 3) ,('Smithsonian', 3) ,('Federal Triangle', 1) ,('Metro Center', 1) ,('McPherson Square', 1) ,
					  ('Farragut West', 3) ,('Foggy Bottom-GWU', 3) ,('Rosslyn', 3) ,('Court House', 3) ,('Clarendon', 1) ,('Virginia Square-GMU', 3) ,
					  ('Ballston-MU', 4) ,('East Falls Church', 3) ,('West Falls Church', 4),('Dunn Loring-Merrifield', 4),('Vienna', 4)])

	orange_line_right_2 = OrderedDict([('Vienna', 4),('Dunn Loring-Merrifield', 4),('West Falls Church', 4) ,('East Falls Church', 3) ,
					   ('Ballston-MU', 4) ,('Virginia Square-GMU', 1) ,('Clarendon', 1) ,('Court House', 1) ,('Rosslyn', 1) ,
					   ('Foggy Bottom-GWU', 3) ,('Farragut West', 1) ,('McPherson Square', 1) ,('Metro Center', 1) ,
					   ('Federal Triangle', 1) ,('Smithsonian', 1) ,("L'Enfant Plaza", 1) ,('Federal Center SW', 1) ,
					   ('Capitol South', 1) ,('Eastern Market', 1) ,('Potomac Ave', 1) ,('Stadium-Armory', 1) ,('Minnesota Ave', 4) ,
					   ('Deanwood', 1) ,('Cheverly', 1) ,('Landover', 3) ,('New Carrollton', 3)])

	green_line_left = OrderedDict([('Branch Ave', 3) ,('Suitland', 1) ,('Naylor Road', 3) ,('Southern Avenue', 2) ,('Congress Heights', 3) ,
				   ('Anacostia', 1) ,('Navy Yard-Ballpark', 1) ,('Waterfront', 1) ,("L'Enfant Plaza", 1) ,('Archives', 1) ,
				   ('Gallery Pl-Chinatown', 1) ,('Mt Vernon Sq 7th St-Convention Center', 1) ,('Shaw-Howard U', 1), ('U Street', 1) ,('Columbia Heights', 3) ,
				   ('Georgia Ave-Petworth', 3) ,('Fort Totten', 3) ,('West Hyattsville', 3) ,("Prince George's Plaza", 3) ,
				   ('College Park-U of Md', 3) ,('Greenbelt', 3)])

	green_line_right = OrderedDict([('Greenbelt', 3) ,('College Park-U of Md', 3) ,("Prince George's Plaza", 3) ,('West Hyattsville', 3) ,
					('Fort Totten', 3) ,('Georgia Ave-Petworth', 3), ('Columbia Heights', 3) ,('U Street', 1) ,
					('Shaw-Howard U', 1) ,('Mt Vernon Sq 7th St-Convention Center', 1) ,('Gallery Pl-Chinatown', 1) ,('Archives', 1) ,("L'Enfant Plaza", 1) ,
					('Waterfront', 1) ,('Navy Yard-Ballpark', 1) ,('Anacostia', 1) ,('Congress Heights', 3) ,('Southern Avenue', 1) ,
					('Naylor Road', 3) ,('Suitland', 1) ,('Branch Ave', 3)])

	yellow_line_left_1 = OrderedDict([('Franconia-Springfield', 6) ,('Van Dorn Street', 6) ,('King St-Old Town', 5) ,('Braddock Road', 1) ,('Ronald Reagan Washington National', 5) ,
					  ('Crystal City', 1) ,('Pentagon City', 1) ,('Pentagon', 5) ,("L'Enfant Plaza", 1) ,('Archives', 1) ,
					  ('Gallery Pl-Chinatown', 1) ,('Mt Vernon Sq 7th St-Convention Center', 1) ,('Shaw-Howard U', 1) ,('U Street', 1) ,('Columbia Heights', 3) ,
					  ('Georgia Ave-Petworth', 3) ,('Fort Totten', 3) ,('West Hyattsville', 3) ,("Prince George's Plaza", 3) ,
					  ('College Park-U of Md', 3) ,('Greenbelt', 3)])

	yellow_line_right_1 = OrderedDict([('Greenbelt', 3) ,('College Park-U of Md', 3) ,("Prince George's Plaza", 3) ,('West Hyattsville', 3) ,
					   ('Fort Totten', 3) ,('Georgia Ave-Petworth', 3) ,('Columbia Heights', 3) ,('U Street', 1) ,
					   ('Shaw-Howard U', 1) ,('Mt Vernon Sq 7th St-Convention Center', 1) ,('Gallery Pl-Chinatown', 1) ,('Archives', 1) ,("L'Enfant Plaza", 1) ,
					   ('Pentagon', 5) ,('Pentagon City', 1) ,('Crystal City', 1) ,('Ronald Reagan Washington National', 5) ,('Braddock Road', 1) ,
					   ('King St-Old Town', 5) ,('Van Dorn Street', 6) ,('Franconia-Springfield', 6)])

	yellow_line_left_2 = OrderedDict([('Huntington', 1) ,('Eisenhower Ave', 1) ,('King St-Old Town', 5) ,('Braddock Road', 1) ,('Ronald Reagan Washington National', 5) ,
					  ('Crystal City', 1) ,('Pentagon City', 1) ,('Pentagon', 5) ,("L'Enfant Plaza", 1) ,('Archives', 1) ,
					  ('Gallery Pl-Chinatown', 1) ,('Mt Vernon Sq 7th St-Convention Center', 1) ,('Shaw-Howard U', 1) ,('U Street', 1) ,('Columbia Heights', 3) ,
					  ('Georgia Ave-Petworth', 3) ,('Fort Totten', 3) ,('West Hyattsville', 3) ,("Prince George's Plaza", 3) ,
					  ('College Park-U of Md', 3) ,('Greenbelt', 3)])

	yellow_line_right_2 = OrderedDict([('Greenbelt', 3) ,('College Park-U of Md', 3) ,("Prince George's Plaza", 3) ,('West Hyattsville', 3) ,
					   ('Fort Totten', 3) ,('Georgia Ave-Petworth', 3) ,('Columbia Heights', 3) ,('U Street', 1) ,
					   ('Shaw-Howard U', 1) ,('Mt Vernon Sq 7th St-Convention Center', 1) ,('Gallery Pl-Chinatown', 1) ,('Archives', 1) ,("L'Enfant Plaza", 1) ,
					   ('Pentagon', 5) ,('Pentagon City', 1) ,('Crystal City', 1) ,('Ronald Reagan Washington National', 5) ,('Braddock Road', 1) ,
					   ('King St-Old Town', 5) ,('Eisenhower Ave', 1),('Huntington', 1)])

	metro = []

	lines = ["Blue_Line", "Red_Line", "Orange_Line", "Green_Line", "Yellow_Line"]

	train_number = 10
	car_number = 3
	time_of_day = "11AM"
	pass_list = []
	stops = []
	train_list = []
	stations = []
	trains = []
	output = []

	if(train_number > 10):
		print "ERROR: CANNOT EXCEED TEN TRAINS PER LINE IN SIMULATION!"
	if(car_number > 3):
		print "ERROR: CANNOT EXCEED THREE CARS PER TRAIN!"
	metro = [blue_line_left, blue_line_right,red_line_left, red_line_right, orange_line_left_1,
	orange_line_right_1,green_line_left, green_line_right, yellow_line_left_1,
	yellow_line_right_1]

	for i in metro:
		for j in i.iterkeys():
			if(j not in stops):
				stops.append(j)

	for i in range(0, 1):
		curr_pass = []
		first = choice(stops)
		second = choice(stops)

	x = False
	while(x == False):
		if(first == second):
			second = choice(stops)
		else:
			x = True
	third = 0
	curr_pass.append(first)
	curr_pass.append(second)
	curr_pass.append(third)
	pass_list.append(curr_pass)

	for i in range(0, train_number):
		for j in metro:
			train_info = []
			train_info.append(j)
			train_info.append(car_number)
			train_info.append(j.keys()[0])
			train_list.append(train_info)

	for i in stops:
		x = Station(i)
		stations.append(x)

	for j in stations:
		j.fill_station(pass_list)

	for i in train_list:
		y = Train(i[0], i[1], i[2], stations, metro)
		trains.append(y)

	path = []
	counter = 0
	while(len(pass_list) > 0):
		for i in trains:
			for j in i.line.iterkeys():
				temp = i.station_find(j)
				for k in temp.station_capacity:
					if(len(i.train) < i.max_capacity and i.start_line(j, k[1]) == i.line and k[2] == 0 and j != k[1]):
						i.load(k)
						temp.station_unload(k)
				if (temp.station_name() in i.transfers):
					for l in i.train:
						destination_line = i.fastest_line(l[1], j)
						if (destination_line != i.line and i.dest_line_check(i.current_stop(j), destination_line) == True):
							i.unload(l)
							l[2] = l[2] + 1 + i.line[j]
							temp.station_load(l)
					for m in temp.station_capacity:
						if(i.fastest_line(m[1],j) == i.line):
							i.load(m)
							temp.station_unload(m)
				for n in i.train:
					if n[1] == temp.station_name():
						temp.station_load(n)
						i.unload(n)
						n.append(temp.station_name())
					else:
						n[2] = n[2] + 1 + i.line[j]
						n.append(temp.station_name())



		for i in trains:
			reverse_line = i.reverse_current_line(i.line)
			for j in reverse_line.iterkeys():
				temp = i.station_find(j)
				for k in temp.station_capacity:
					if(len(i.train) < i.max_capacity and i.start_line(j, k[1]) == i.line and k[2] == 0 and j != k[1]):
						i.load(k)
						temp.station_unload(k)
				if (temp.station_name() in i.transfers):
					for l in i.train:
						destination_line = i.fastest_line(l[1], j)
						if (destination_line != i.line and i.dest_line_check(i.current_stop(j), destination_line) == True):
							i.unload(l)
							l[2] = l[2] + 1 + i.line[j]
							temp.station_load(l)
					for m in temp.station_capacity:
						if(i.fastest_line(m[1],j) == i.line):
							i.load(m)
							temp.station_unload(m)
				for n in i.train:
					if n[1] == temp.station_name():
						temp.station_load(n)
						i.unload(n)
					else:
						n[2] = n[2] + 1 + reverse_line[j]
		counter = counter + 1
		for i in stations:
			lines = []
			for j in metro:
				if i.station_name() in j:
					lines.append(j)
			for k in pass_list:
				if(i.station_name() == k[1]):
					print k
					for j in range(3, len(k)):
						if(k[j] not in path):
							holder = pathFind(k[j])
							path.append(holder)
					pass_list.remove(k)

	jsonData = [path]
	return render(request, 'metro.html', {'array':jsonData})