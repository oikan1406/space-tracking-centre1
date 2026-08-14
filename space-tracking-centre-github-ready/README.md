# Space Tracking Centre — Real-Time ISS Tracker

A Streamlit-based Space Tracking Centre project for monitoring the position and ground track of space stations, and finding ISS pass events over selected cities.

## Features

- Real-time latitude, longitude and altitude of a selected space station.
- Space-station selection from the CelesTrak station TLE catalogue.
- Interactive Folium map.
- Ground-track visualization for a selectable time range.
- Observation mode for a selected city.
- Supports predefined cities: New Delhi, Mumbai, Bangalore, Kolkata, Hyderabad, Chennai and Agartala.
- Manual city search using OpenStreetMap/Nominatim through GeoPy.
- ISS pass-event information:
  - Rise
  - Culminate
  - Set
  - Pass duration
  - UTC time
  - Altitude angle
  - Azimuth angle
- Includes project CSV datasets containing city coordinates and ISS pass-over observations.

## Project Structure

```text
space-tracking-centre/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    ├── City_ISS_PassOver_data.csv
    └── city_coordinate_data.csv
```

## How the project works

The application uses satellite Two-Line Element (TLE) data from CelesTrak and the Skyfield library to calculate the satellite position.

The Streamlit interface lets the user:

1. Select a space station.
2. Press **Refresh Position** to load its current position.
3. Enable **Ground Track** and choose a time range to display the projected track.
4. Enable **Observation mode**.
5. Select a predefined city or enter a city manually.
6. Select Rise, Culminate and/or Set events.
7. View the predicted pass time, duration, altitude and azimuth on the map and below it.

## Important note about the CSV files

The CSV files are included as project data/reference outputs. The current `app.py` calculates live satellite information from TLE data; it does **not** load the CSV files to generate the live map.

## Run locally

### 1. Install Python

Use Python 3.9+.

### 2. Open the project folder

```bash
cd space-tracking-centre
```

### 3. Create a virtual environment (recommended)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the Streamlit app

```bash
streamlit run app.py
```

A browser window should open automatically. If it does not, Streamlit will show a local URL such as:

```text
http://localhost:8501
```

## GitHub upload

### Option A — easiest: GitHub website

1. Go to GitHub and sign in.
2. Click **New repository**.
3. Repository name:
   `space-tracking-centre`
4. Add a short description such as:
   `Real-time ISS and space-station tracking using Streamlit, Skyfield and Folium.`
5. Choose Public if you want the project visible on your resume.
6. Create the repository.
7. Open **Add file → Upload files**.
8. Upload:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - the complete `data` folder with both CSV files
9. Click **Commit changes**.

## GitHub upload using Git

From inside the project folder:

```bash
git init
git add .
git commit -m "Initial commit - Space Tracking Centre"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your own GitHub repository.

## How to get the live output from GitHub

GitHub stores the code but does not run the Streamlit application by itself.

For a live web output, deploy the repository using **Streamlit Community Cloud**:

1. Push the complete project to GitHub.
2. Open Streamlit Community Cloud.
3. Sign in with GitHub.
4. Create a new app.
5. Select your repository:
   `space-tracking-centre`
6. Select the `main` branch.
7. Set the main file to:
   `app.py`
8. Deploy the app.
9. Streamlit installs the packages from `requirements.txt` and starts the application.
10. You receive a public web link that can be placed in your resume/GitHub project description.

## Internet requirement

The live tracking portion requires internet access because the application downloads current station TLE data from CelesTrak. Manual city lookup can also use the Nominatim geocoding service.

## Suggested GitHub repository description

> Real-time Space Tracking Centre built with Python, Streamlit, Skyfield and Folium. Provides live space-station positioning, interactive ground tracks and ISS pass predictions for selected cities.

## Suggested resume project title

**Space Tracking Centre — Real-Time ISS & Satellite Tracker**

**Tech:** Python, Streamlit, Skyfield, Folium, GeoPy, CelesTrak TLE, Pandas/CSV

## Project output

The deployed application provides:

- Current space-station position
- Latitude / longitude / altitude
- Interactive world map
- Ground track
- City marker
- Rise / Culminate / Set markers
- Pass duration
- UTC event times
- Altitude and azimuth angles
