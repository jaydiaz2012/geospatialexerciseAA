import streamlit as st
import datetime
import time
from pystac_client import Client
from shapely.geometry import Point
import folium
from streamlit_folium import st_folium

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Satellite Imagery Search",
    layout="centered"
)

st.title("Sentinel-2 Satellite Imagery Finder")

def normalise_longitude(lon: float) -> float:
    """
    Normalise longitude to [-180, 180]
    """
    return ((lon + 180) % 360) - 180


def clamp_latitude(lat: float) -> float:
    """
    Clamp latitude to [-90, 90]
    """
    return max(min(lat, 90), -90)
    
# --------------------------------------------------
# Initialise session state (SINGLE SOURCE OF TRUTH)
# --------------------------------------------------
if "lat" not in st.session_state:
    st.session_state.lat = 16.412538689090894
    st.session_state.lon = 120.59368070367955
    
if "start_date" not in st.session_state:
    st.session_state.start_date = datetime.date(2025, 12, 1)

if "end_date" not in st.session_state:
    st.session_state.end_date = datetime.date(2025, 12, 31)

if "location_name" not in st.session_state:
    st.session_state.location_name = "Selected location"

if "last_click" not in st.session_state:
    st.session_state.last_click = None

if "last_search_time" not in st.session_state:
    st.session_state.last_search_time = 0

# Rate-limit in seconds
SEARCH_COOLDOWN = 5

# --------------------------------------------------
# Map selector
# --------------------------------------------------
st.subheader("Select location on map (zoom + click)")

map_center = [st.session_state.lat, st.session_state.lon]

m = folium.Map(
    location=map_center,
    zoom_start=12,
    tiles="OpenStreetMap"
)

folium.Marker(
    map_center,
    tooltip="Selected location"
).add_to(m)

map_data = st_folium(m, height=450, width=700)

# --------------------------------------------------
# Handle map click → auto search trigger
# --------------------------------------------------
trigger_search = False

if map_data and map_data.get("last_clicked"):
    click = map_data["last_clicked"]

    if st.session_state.last_click != click:
        st.session_state.last_click = click
        st.session_state.lat = clamp_latitude (click["lat"])
        st.session_state.lon = normalise_longitude(click["lng"])

        now = time.time()
        if now - st.session_state.last_search_time > SEARCH_COOLDOWN:
            trigger_search = True
            st.session_state.last_search_time = now

        st.success(
            f"Selected coordinates: "
            f"{st.session_state.lat:.6f}, {st.session_state.lon:.6f}"
        )

        st.session_state.lat = clamp_latitude(st.session_state.lat)
        st.session_state.lon = normalise_longitude(st.session_state.lon)

lat = st.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=st.session_state.lat,
    format="%.6f"
)

lon = st.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=st.session_state.lon,
    format="%.6f"
)

# --------------------------------------------------
# Controls
# --------------------------------------------------
st.subheader("Search parameters")

st.session_state.start_date = st.date_input(
    "Start date",
    value=st.session_state.start_date
)

st.session_state.end_date = st.date_input(
    "End date",
    value=st.session_state.end_date
)

# --------------------------------------------------
# Satellite search function
# --------------------------------------------------
def search_satellite_imagery():
    st.subheader(f"Searching imagery for selected location")

    st.write(
        f"Coordinates: {st.session_state.lat}, {st.session_state.lon}"
    )
    st.write(
        f"Date range: {st.session_state.start_date} to {st.session_state.end_date}"
    )
    
    api_url = "https://earth-search.aws.element84.com/v1"
    client = Client.open(api_url)
    
    point = Point( st.session_state.lon, st.session_state.lat)

    search = client.search(
        collections=["sentinel-2-l2a"],
        intersects=point.__geo_interface__,
        datetime=f"{st.session_state.start_date}/{st.session_state.end_date}",
        query={"eo:cloud_cover": {"lt": 15}}
    )

    items = list(search.get_items())
    st.write(f"Found {len(items)} matching scenes")

    if not items:
        st.warning("No images found.")
        return

    best_item = sorted(
        items,
        key=lambda x: x.properties.get("eo:cloud_cover", 100)
    )[0]

    st.success("Best available image")
    st.write(f"Scene ID: {best_item.id}")
    st.write(f"Acquisition time: {best_item.datetime}")
    st.write(f"Cloud cover: {best_item.properties['eo:cloud_cover']:.2f}%")

    if "thumbnail" in best_item.assets:
        st.image(
            best_item.assets["thumbnail"].href,
            caption="Sentinel Thumbnail"
        )

st.info(
    f"Searching at "
    f"Lat {lat:.6f}, Lon {lon:.6f} (normalised)"
)

# --------------------------------------------------
# AUTO-RUN SEARCH (SAFE + RATE-LIMITED)
# --------------------------------------------------
if trigger_search:
    with st.spinner("Searching Sentinel-2 imagery..."):
        search_satellite_imagery()

# --------------------------------------------------
# Manual fallback button (recommended)
# --------------------------------------------------
if st.button("Run search manually"):
    with st.spinner("Searching Sentinel-2 imagery..."):
        search_satellite_imagery()
