# SmartPark: Intelligent Parking Space Detection using Computer Vision 🚗

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smartpark-nrvrwzydpfjsmdrbsyksud.streamlit.app/)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SmartPark is a production-ready, cloud-deployable computer vision application built on Streamlit. It monitors parking space utilization in real time from video feeds using OpenCV and provides an interactive web dashboard for monitoring occupancy statistics and exportable reports.

---

## 🔗 Live Demo

Experience the live deployed application on Streamlit Community Cloud:  
👉 **[https://smartpark-nrvrwzydpfjsmdrbsyksud.streamlit.app/](https://smartpark-nrvrwzydpfjsmdrbsyksud.streamlit.app/)**

---

## ✨ Features

- **Parking Space Occupancy Detection**: Leverages an OpenCV-based image processing pipeline to dynamically detect slot occupancy.
- **Video Upload Support**: Processes uploaded parking lot video files (.mp4, .avi, .mov, etc.).
- **Parking Layout (.pkl) Upload**: Allows importing custom coordinate bounding boxes.
- **Layout Verification Preview**: Overlays slot bounds onto the first frame of the video to verify alignment before starting calculations.
- **Real-Time Parking Metrics**: Displays total monitored spots, current occupied spots, and free spots.
- **Occupancy Percentage Calculation**: Real-time statistics tracking utility rate.
- **Parking Health Indicator**: Shows a colored badge system (🟢 Healthy, 🟡 Normal, 🟠 Alert, 🔴 Capacity warning) based on overall utilization.
- **Rule-Based Parking Summary**: Generates rule-based summaries and management recommendations offline.
- **CSV Export**: Downloads a complete timestamped log of the occupancy tracking history.
- **Fully Offline Operation**: Performs all analytics and processing locally without relying on external cloud machine learning APIs.
- **Streamlit Web Interface**: A clean, fully responsive, user-friendly modern dashboard.

---

## 🛠️ Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web application framework.
- **OpenCV**: Open-source computer vision library for image thresholding and processing.
- **NumPy**: Matrix computations and mathematical operations.
- **Pandas**: Structured statistical timeline data tracking and CSV exporting.
- **Pillow**: Frontend image loading and format utilities.

---

## 📁 Project Structure

```
SmartPark-AI/ (Workspace Root)
├── app.py              # Main dashboard frontend and real-time processing loop
├── detector.py         # OpenCV video thresholding and space annotations
├── utils.py            # Bounding box coordinates loading and CSV utilities
├── sample_layout.pkl   # Pre-configured grid of 12 spaces for demo purposes
├── requirements.txt    # Production-ready package dependency declarations
├── .gitignore          # Git exclusion guidelines
└── README.md           # This document
```

---

## 💻 Installation

### 1. Prerequisites
Ensure you have **Python 3.11+** installed on your system.

### 2. Navigate to the Directory
Navigate to the project workspace directory:
```bash
cd SmartPark-AI
```

### 3. Install Dependencies
Install all package requirements (uses `opencv-python-headless` for headless server compatibility):
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Launch the local Streamlit development server:
```bash
streamlit run app.py
```
Open a browser and navigate to `http://localhost:8501`.

---

## 📖 Usage

1. **Upload Parking Layout**: Upload a `.pkl` layout configuration file in the sidebar. If none is uploaded, the dashboard initializes the pre-packaged **12-slot default grid** automatically.
2. **Upload Parking Video**: Upload the security camera feed video file in the sidebar.
3. **Verify Layout Preview**: Look at the **Verification Preview** box on the main panel to make sure the bounding boxes align correctly over the parking spaces.
4. **Start Processing**: Click **Start Processing** in the sidebar. The video will play showing red boxes for occupied slots and green boxes for empty slots.
5. **View Parking Metrics**: Monitor real-time counts, utilization rates, and the visual **Parking Health** panel.
6. **Download CSV Report**: Once processing completes, click **Download CSV Report** in the lower left to download the statistics history.

---

## 🚀 Deployment

This application is publicly deployed and hosted on **Streamlit Community Cloud** at the following address:  
🔗 **[https://smartpark-nrvrwzydpfjsmdrbsyksud.streamlit.app/](https://smartpark-nrvrwzydpfjsmdrbsyksud.streamlit.app/)**

Deploying your own version:
1. Push the codebase to a public GitHub repository.
2. Link your GitHub account to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New App**, select your repository, and set the entry file to `SmartPark-AI/app.py`.
4. Click **Deploy**!

---

## 🔮 Future Improvements

- **Automatic Parking Slot Detection**: Incorporate deep learning (e.g. YOLO/R-CNN) to automatically detect slots without needing manually pre-drawn `.pkl` files.
- **Multi-Camera Support**: Monitor multiple cameras simultaneously on a single unified dashboard.
- **Historical Analytics**: Integrate database storage (SQLite/PostgreSQL) to store analytics history for monthly/weekly dashboard graphs.
- **License Plate Recognition (ALPR)**: Identify specific vehicles entering and exiting each slot.
- **Mobile-Friendly Interface**: Create a lightweight mobile progressive web app (PWA) version for parking lot operators on the go.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) details below.

```
MIT License

Copyright (c) 2026 Harshal Ninawe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
<img width="1916" height="1013" alt="Screenshot 2026-07-14 125331" src="https://github.com/user-attachments/assets/7c4e2cd6-bb40-4cc5-a42e-5b1960d3d291" />
<img width="1917" height="970" alt="Screenshot 2026-07-14 125432" src="https://github.com/user-attachments/assets/8efc7c37-9ff8-4adb-a617-b97c7435ce20" />
<img width="1901" height="848" alt="Screenshot 2026-07-14 125518" src="https://github.com/user-attachments/assets/c324faae-02eb-476f-808e-e27ba0436197" />

