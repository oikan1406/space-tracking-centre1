import streamlit as st
from streamlit_folium import st_folium
from folium import Map, Marker, PolyLine, FeatureGroup, Icon
from skyfield.api import load,Loader, EarthSatellite, Topos, wgs84
from datetime import datetime, timezone, timedelta
from dateutil.parser import isoparse
from streamlit_autorefresh import st_autorefresh
from geopy.geocoders import Nominatim


#Sets up page
st.set_page_config(layout="wide", page_title="Real-Time ISS Tracker")
st.title("ISS Tracker ")
st.caption("Click the refresh button to update ISS location.")

#Gives option to change th espace station
option=st.selectbox("Select Space Station:",['ISS (ZARYA)','CSS (TIANHE)',
        'ISS (NAUKA)','FREGAT DEB','CSS (WENTIAN)','CSS (MENGTIAN)',
        'PROGRESS-MS 30','CREW DRAGON 10','SOYUZ-MS 27','SHENZHOU-20 (SZ-20)',
        'PROGRESS-MS 31','TIANZHOU-9','CZ-7 R/B','CZ-7 DEB','CZ-7 DEB'])


#Gets TLE file
file="http://celestrak.org/NORAD/elements/stations.txt"

#Returns the selected space station
def get_satellite():
    sats = load.tle_file(file)
    return {sat.name: sat for sat in sats}[option]


#Runs the function
satellite = get_satellite()


#Doesnt show the location on first opening
if "show_iss" not in st.session_state:
    st.session_state.show_iss = False

#Initial Conditions
groundtrack=False
observation=False
timerange=0
times=[]
event=[]
e=[]
x=0
city='New Delhi'
lat_c=0
lon_c=0
tr1=False
tr2=False
city='New Delhi' 
timescale=load.timescale()
no=10
satellite = get_satellite()
observer = wgs84.latlon(lat_c, lon_c)
coords=[]
manual=False
precity=False
Mark=False
Cityy=''

#Refreshes the location   
if st.button("🔄 Refresh Position"):
    
    #Gets space station
    satellite = get_satellite()
    
    #Gets time
    timescale = load.timescale()
    t = timescale.now()
    
    #Gets space station's location
    subpoint = satellite.at(t).subpoint()
    
    #Displays information
    st.session_state.last_refresh_time = t.utc_datetime().isoformat()
    st.session_state.lat = subpoint.latitude.degrees
    st.session_state.lon = subpoint.longitude.degrees
    st.session_state.alt = subpoint.elevation.km
    st.session_state.timestamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
    st.session_state.show_iss = True


#Normalises the longitude befor infinite longitude
def normalize_longitudes(lons):
    return [((lon + 180) % 360) - 180 for lon in lons]


#COmputes the ground track
def compute_ground_track(_sat,_now, minute):
    
    #Gets timerange of track
    times = [timescale.utc((_now.utc_datetime() + timedelta(minutes=i))) for i in range(0, minute+1)]
    
    #Gets location
    subpoints = [_sat.at(t).subpoint() for t in times]
    lats = [p.latitude.degrees for p in subpoints]
    lons = [p.longitude.degrees for p in subpoints]

    return lats, lons


#Repeats the longotudes for infinite view
def repeat_segments(lats, lons,i):
    x=[(lats, lons)]
    
    #Adds same longitudes every 360deg
    for j in range(1,i+1):
        x.append((lats, [lon - (j*360) for lon in lons]))
        x.append((lats, [lon + (j*360) for lon in lons]))
    
    return x

#Repeats the locations for infinite view
def repeat_positions(lat, lon,i):
    return [(lat, lon + 360 * i) for i in range(-i, i)]


#Cached list of cities
city_list={"New Delhi": (28.6139, 77.2090),
"Mumbai": (19.0760, 72.8777),
"Bangalore": (12.9716, 77.5946),
"Kolkata": (22.5726, 88.3639),
"Hyderabad": (17.3850, 78.4867),
"Chennai": (13.0827, 80.2707),
"Agartala": (23.8315,91.2868)}


#Gets coordinates of city
def get_coordinates(city):

    #Checks if the given city is already cached or not
    if city in city_list:
        return city_list[city]

    #Locates ISS's path
    geolocator = Nominatim(user_agent="iss_tracker", timeout=10)
    
    #Checks city position on the ISS path
    location = geolocator.geocode(city)
    
    #Returns city coordinate if on the ISS path
    if location:
        return location.latitude, location.longitude
    
    #Returns none if found nothing
    else:
        return None,None

#Adds checkbox for times and positions of events
if st.checkbox('Observation mode'):
    st.write('Shows Time of Rise, Culminate or Set of Station from the city')
    
    #Adds manual input of city
    mode=st.selectbox("Select City Selction Mode:",['Manual Input',"Given Cities"])
        
    #Gives location of input city
    if mode=='Manual Input':

        #Changes condition
        manual=True

        #Takes manual city input
        Cityy=st.text_input("Enter City:")
        
        #Checks if city exists
        if Cityy=='':
            pass
        else:
            coords = get_coordinates(Cityy)
            if coords:
                pass
            elif coords==None:
                st.write(f"Could not find coordinates for '{Cityy}'. Please check the spelling.")
             
    #Gives hardcoded cities
    else:
        precity=True
        #Gives option to select observation city
        option=st.selectbox('Select City:',["New Delhi","Mumbai","Bangalore",
        "Kolkata","Hyderabad","Chennai","Agartala"])
    
    #Changes condition
    tr1=True
    observation=True

    #Adds events to be viewed
    e=[]

    #Adds checkbox for each event
    if st.checkbox('Rise'):
        e.append(0)
    if st.checkbox('Culminate'):
        e.append(1)
    if st.checkbox('Set'):
        e.append(2)


#Adds checkbox tom show ground track
if st.checkbox('Ground Track'):
    st.write('Shows the Ground Track of the Space Station')
    
    #Changes condition
    tr2=True
    groundtrack=True

#Adds timeslider only when conditions are met
if tr1==True or tr2==True:
    timerange=st.slider('Select Timerange (Min)',0,1440,step=30)
    if timerange==0:
            st.write("Select time range.")

#Shows map and data
if st.session_state.show_iss:
    
    #Shows updated time
    st.success(f"Updated at {st.session_state.timestamp} UTC")

    #Displays datas in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Latitude", f"{st.session_state.lat:.2f}°")
    col2.metric("Longitude", f"{st.session_state.lon:.2f}°")
    col3.metric("Altitude", f"{st.session_state.alt:.2f} km")

    #Creates the map
    m = Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=2, tiles="cartodb positron")
    
    #Adds infinte space station position
    for lat, lon in repeat_positions(st.session_state.lat, st.session_state.lon,5):
        Marker([lat, lon], tooltip="🚁 ISS Current Position").add_to(m)
                
    #Adds groundtrack if checked
    if groundtrack == True:

        #Gets latest time
        if "last_refresh_time" in st.session_state:
            dt = isoparse(st.session_state.last_refresh_time)
        else:
            dt = datetime.now(timezone.utc)
        time_str = timescale.utc(dt)

        #Gets ground track
        lats, lons = compute_ground_track(satellite, time_str, timerange)
        
        #Normalizes original longitudes
        lons = normalize_longitudes(lons)

        #Repeats longitudes for infinite ground track
        for lat_set, lon_set in repeat_segments(lats, lons,no):
            
            #Stores extended locations
            segments = []
            segment = [(lat_set[0], lon_set[0])]

            #Extends the ground track
            for i in range(1, len(lat_set)):
                if abs(lon_set[i] - lon_set[i - 1]) > 180:
                    segments.append(segment)
                    segment = []
                segment.append((lat_set[i], lon_set[i]))

            segments.append(segment)
            
            #Adds the ground track
            for seg in segments:
                PolyLine(seg, color="blue", weight=2.5, opacity=0.8).add_to(m)

    #Shows events details if checked
    if observation==True:
        
        #Adds manual cities
        if manual==True:
            if coords:

                #Gets location of manual city
                lat_c=coords[0]
                lon_c = coords[1]

                #Adds infinite city
                for lat, lon in repeat_positions(lat_c, lon_c,no):
                    Marker([lat, lon], tooltip=f"📍 {Cityy}", icon=Icon(color='green')).add_to(m)

        #Adds hardcoded cities 
        if precity==True:
            selected_city = option
           
            #Adds loaction of city
            if selected_city in city_list:
                
                #Gets city location
                lat_c, lon_c = city_list[selected_city]
                
                #Adds infinite city
                for lat, lon in repeat_positions(lat_c, lon_c,no):
                    Marker([lat, lon], tooltip=f"📍 {selected_city}", icon=Icon(color='green')).add_to(m)
            else:
                lat_c, lon_C = get_coordinates(city_list[selected_city])
                Marker([lat, lon], tooltip=f"📍 {selected_city}", icon=Icon(color='green')).add_to(m)
        
        #Changes condition
        if manual==True:
            if coords==None:
                Mark=False
            else:
                Mark=True
        if precity==True:
            Mark=True

        #Adds events
        if Mark==True:
            #Adds observer perspective
            observer = wgs84.latlon(lat_c, lon_c)
            
            #Changes time range to avoid getting error
            if timerange==0:
                pass

            else:
                #Creates timerange for viewing
                if "last_refresh_time" in st.session_state:
                    dt = isoparse(st.session_state.last_refresh_time)
                else:
                    dt = datetime.now(timezone.utc)
                t = timescale.utc(dt)
                t24 = timescale.utc(t.utc_datetime() + timedelta(minutes=timerange))

                #Computes pass events for rise, culminate and set
                times, events = satellite.find_events(observer, t, t24, altitude_degrees=0)


                #Converts event number to corresponding event: Rise=0, Culminate=1, Set=2
                x=len(events)/3
                event=[]
                for i in events:
                    if i==0:
                        event.append("Rise")
                    elif i==1:
                        event.append("Culminate")
                    elif i==2:
                        event.append("Set")
                color=('yellow',"lightred",'beige')
                
                #Adds the event location
                if len(e)>0:
                    for i in range(int(x)):
                        for j in e:
                            
                            #Gets event location
                            sub = satellite.at(times[(3*i)+j]).subpoint()
                            
                            for lat, lon in repeat_positions(sub.latitude.degrees, sub.longitude.degrees,no):

                                #Adds infinite location of events        
                                Marker([lat, lon], tooltip=f"{event[3*i+j]}{i+1}", icon=Icon(color=color[j])).add_to(m)
                else:
                    st.write('Choose event.')

    #Creates map
    map_key = f"map_gt_{groundtrack}_{timerange if groundtrack else 0}"
    st_folium(m, width=700, height=500, key=map_key)

    #Adds viewing times and details
    if observation==True:
        if Mark==True:
            if timerange==0:
                pass

            else:
                
                #Changes city variable for manual selection
                if manual==True:
                    city=Cityy
                if precity==True:
                    city=selected_city

                #Writes selected details
                st.write(f"Next ISS Pass Over: {city} ({lat_c},{lon_c}) for next {(timerange/60):.2f} hrs\n")

                #Converts the epoch to UTC time
                time=[]
                for i in times:
                    time.append(i.utc_strftime('%d/%m/%y %I:%M:%S %p UTC'))

                #Displays the details
                if len(e)>0:
                    for i in range(int(x)):
                        
                        #Gives duration of pass over
                        st.write(f'{i+1}.Duration: {((times[3*i+2].utc_datetime()-times[3*i].utc_datetime()).total_seconds()/60):.1f} mins')
                        
                        for j in e:

                            #Gets altitudinal and azimuthal angle
                            alt, az, _ = (satellite - observer).at(times[3*i+j]).altaz()
                            
                            #Writes the details
                            st.write(f"  {event[3*i+j]}: {time[3*i+j]}  |  Alt: {alt.degrees:.1f}°  |  Az: {az.degrees:.1f}°")
                    
                        st.write('\n')
else:
    st.info("Press the button above to load ISS position.")


    

