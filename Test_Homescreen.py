import csv
from guizero import App, Text, PushButton, Window, TextBox, Slider

def slider_changed(slider_value):
	degree_input.value = slider_value

def open_window0():
	panel_window.show()
def open_window1():
	loadtesting_window.show()
def open_window2():
	suntracking_window.show()
def open_window3():
	weather_window.show()
def open_window4():
	location_window.show()

def close_window0():
	panel_window.hide()
def close_window1():
	loadtesting_window.hide()
def close_window2():
	suntracking_window.hide()
def close_window3():
	weather_window.hide()
def close_window4():
	location_window.hide()

app = App(layout="auto",title="Solar Panel Controller Homescreen")
instructions = Text(app, text="Select what you would like to view or adjust")

#Defining the different diagnostic windows along with their parameters
panel_window = Window(app, title="Panel Adjustments")
panel_instructions = Text(panel_window, text="Panel Adjustments allows user to modify panel positioning manually")
degree_text = Text(panel_window, text="Use slider to adjust panel position in degree rotation")
degree_slider = Slider(panel_window, command=slider_changed)
degree_input = TextBox(panel_window)
swivel_text = Text(panel_window, text="")
panel_window.hide()

loadtesting_window = Window(app, title="Load Testing")
load_instructions = Text(loadtesting_window, text="Load Testing allows user to view and test power output through a connected load or appliance")
loadtesting_window.hide()

suntracking_window = Window(app, title="Sun Tracking")
tracking_instructions = Text(suntracking_window, text="Sun Tracking allows user to track sun movement detected automatically by the panel")
suntracking_window.hide()

weather_window = Window(app, title="Weather")
weather_instructions = Text(weather_window, text="Weather window allows user to view weather information important for panel protection and adjustment")
weather_window.hide()

location_window = Window(app, title="Location")
location_instructions = Text(location_window, text="Location window allows user to modify their location")
location_window.hide()

#Defining the buttons that will open and close each window for each diagnostic 
panel_button = PushButton(app, text="Panel Adjustments", command=open_window0)
closepanel_button = PushButton(panel_window, text="Close", align="bottom", command=close_window0)

load_button = PushButton(app, text="Load Testing", command=open_window1)
closeload_button = PushButton(loadtesting_window, text="Close", align="bottom", command=close_window1)

sun_button = PushButton(app, text="Sun Tracking", command=open_window2)
closesun_button = PushButton(suntracking_window, text="Close", align="bottom", command=close_window2)

weather_button = PushButton(app, text="Weather Tracking", command=open_window3)
closeweather_button = PushButton(weather_window, text="Close", align="bottom", command=close_window3)

location_button = PushButton(app, text="Location", command=open_window4)
closelocation_button = PushButton(location_window, text="Close", align="bottom", command=close_window4)



#Send outputs for LOCATION onto a CSV file****

app.display()