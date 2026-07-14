# SmartPark: Intelligent Parking Space Detection using Computer Vision 🚗

SmartPark is a production-ready, cloud-deployable computer vision application built on Streamlit. It detects parking slot occupancy from video feeds using OpenCV and generates rule-based occupancy summary reports and parking health updates.

## Features

- **Real-Time Bounding Box Overlays**: OpenCV pipeline processes video streams to draw green outlines for empty spots and red outlines for occupied spots.
- **Verification Preview**: Renders the first frame of the uploaded video with the layout slots overlaid so users can verify alignment before running.
- **Live Metrics Dashboard**: Real-time summary statistics tracking Total Slots, Occupied Slots, Free Slots, and Occupancy Rate.
- **Local Analytics Reporting**: Calculates final session metrics (Average Occupancy Rate, Peak Occupancy Rate) and classifies the parking lot state.
- **Parking Health Visual Indicator**: Provides intuitive status badges (🟢 Low, 🟡 Moderate, 🟠 High, 🔴 Nearly Full) with specific operational recommendations.
- **CSV Data Exporter**: Download the detailed timeline history of parking occupancy rates.
- **Zero Configuration Demo**: Automatically creates and loads a default demonstration layout (`sample_layout.pkl`) if no layout is uploaded.

---

## Project Structure

```
SmartPark-AI/
├── app.py              # Streamlit frontend layout and video processing loop
├── detector.py         # OpenCV image processing and space-checking logic
├── utils.py            # Layout loading and CSV generation helpers
├── sample_layout.pkl   # Auto-generated grid of 12 slots for testing
├── requirements.txt    # Minimal dependencies for cloud host compatibility
├── .gitignore          # Excludes caches and uploaded media
└── README.md           # This project guide
```

---

## Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.11+** installed on your system.

### 2. Navigate to the Directory
Open a terminal and navigate to the project directory:
```bash
cd SmartPark-AI
```

### 3. Install Dependencies
Install all required libraries (using `opencv-python-headless` to ensure headless cloud server compatibility):
```bash
pip install -r requirements.txt
```

---

## How to Run Locally

Start the application by running:
```bash
streamlit run app.py
```
This will open the application in a new browser window (usually at `http://localhost:8501`).

---

## Usage Guide

1. **Parking Layout File (.pkl)**: Upload a layout file containing space coordinates. If none is uploaded, the app automatically initializes a standard **12-slot demo grid**.
2. **Parking Video**: Upload a security camera feed or parking lot video file (.mp4, .avi, etc.).
3. **Layout Verification**: Once uploaded, review the **Verification Preview** on the screen to check if the boxes match the parking spaces. If they don't, adjust the layout or the camera position.
4. **Processing**: Click **Start Processing**. Watch the CV pipeline run in real-time.
5. **Analytics and Exports**:
   - Download the generated **CSV Report** detailing timeline data.
   - Read the local **Parking Summary & Health** report containing occupancy summaries and suggestions.

---

## Deployment to Streamlit Community Cloud

This application is optimized for deployment directly to the **Streamlit Community Cloud** with zero modifications.

1. Push this codebase to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **New App**, select your repository, branch, and set the main file path to `SmartPark-AI/app.py`.
4. Click **Deploy** and the application is live!
