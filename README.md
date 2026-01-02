# Sentinel-2 Satellite Image Explorer (Streamlit)

An interactive **Streamlit web application** that allows users to select any location on a map and **automatically fetch Sentinel-2 satellite imagery** using STAC APIs.

Users can click directly on a map, zoom in or out to verify location, and instantly retrieve the most recent satellite image available for the selected coordinates.

---

## 🚀 Features

- 🗺️ **Interactive map selection**
  - Click anywhere on the map to select latitude and longitude
  - Zoom in and out to visually validate the location before image retrieval

- 🛰️ **Automatic Sentinel-2 search**
  - Satellite imagery search runs immediately after a map click
  - No manual “Search” button required

- 🌍 **Sentinel-2 imagery via STAC**
  - Queries Sentinel-2 L2A imagery using a STAC API
  - Retrieves cloud-optimised GeoTIFF (COG) assets

- 📍 **Coordinate sanitisation**
  - Latitude clamped to valid range (-90° to 90°)
  - Longitude normalised (-180° to 180°)
  - Prevents invalid API calls

- 📊 **Session-based coordinate logging**
  - Logs corrected or rejected coordinates for debugging and UX insights
  - Stored safely in Streamlit session state

- ⚡ **Fast and lightweight**
  - No heavy GIS libraries required
  - Designed for rapid prototyping and demos

---

## 🧠 How It Works

1. User clicks on the interactive map  
2. Coordinates are validated and normalised  
3. Sentinel-2 imagery search triggers automatically  
4. The most recent matching satellite image is fetched  
5. The image is displayed directly in the app  

This creates a smooth, exploratory workflow for satellite data discovery.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – web application framework
- **pystac-client** – STAC API interaction
- **Shapely** – geographic point handling
- **Requests** – HTTP requests

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/sentinel2-streamlit-explorer.git
cd sentinel2-streamlit-explorer
