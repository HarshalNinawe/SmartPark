import streamlit as st
import cv2
import tempfile
import os
import time
from datetime import datetime
from PIL import Image

# Import local modules
from detector import process_video_frame, check_parking_space
from utils import load_parking_positions, generate_csv, create_default_layout

# Initialize page configuration
st.set_page_config(
    page_title="SmartPark - Parking Space Detection Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom Styling -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .title-container {
        padding: 1.5rem 0rem;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .title-main {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    .title-sub {
        font-size: 1.1rem;
        font-weight: 300;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .section-header {
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
        color: #1F2937;
    }
</style>
""", unsafe_allow_html=True)

# Ensure default demonstration layout file exists in the repository
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LAYOUT_PATH = os.path.join(APP_DIR, "sample_layout.pkl")
if not os.path.exists(DEFAULT_LAYOUT_PATH):
    create_default_layout(DEFAULT_LAYOUT_PATH)

# Initialize Session State variables
if 'history_log' not in st.session_state:
    st.session_state.history_log = []
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False
if 'final_stats' not in st.session_state:
    st.session_state.final_stats = None

# ----------------- Title Header -----------------
st.markdown("""
<div class="title-container">
    <div class="title-main">🚗 SmartPark</div>
    <div class="title-sub">Intelligent Parking Space Detection Dashboard</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Welcome to **SmartPark**, a modern computer vision application designed to monitor parking slot utilization in real time. 
This dashboard utilizes OpenCV to process live video feeds, overlay parking slot statuses (Occupied vs. Free), and generates rule-based occupancy summary reports and parking health updates.
""")

# ----------------- Sidebar Inputs -----------------
st.sidebar.header("🔧 Configuration Panel")

# Upload Files
uploaded_layout = st.sidebar.file_uploader("Upload Parking Layout (.pkl)", type=["pkl"])
uploaded_video = st.sidebar.file_uploader("Upload Parking Video", type=["mp4", "avi", "mov", "mkv"])

st.sidebar.markdown("---")

# Parameters
threshold_factor = st.sidebar.slider(
    "Occupancy Threshold", 
    min_value=0.05, 
    max_value=0.50, 
    value=0.15, 
    step=0.01,
    help="Adjust occupancy detection sensitivity. Lower values detect more occupied slots."
)

# Trigger
start_btn = st.sidebar.button(
    "🚀 Start Processing", 
    disabled=(uploaded_video is None),
    use_container_width=True
)

# ----------------- Layout & File Setup -----------------
pos_list = []

if uploaded_layout is not None:
    try:
        pos_list = load_parking_positions(uploaded_layout)
        st.sidebar.success("✅ Custom layout file loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading custom layout: {e}")
        pos_list = []
else:
    # Use default layout
    try:
        pos_list = load_parking_positions(DEFAULT_LAYOUT_PATH)
        st.sidebar.info("ℹ️ Using default demonstration layout (`sample_layout.pkl`). Upload a custom `.pkl` layout for custom bounding boxes.")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading default layout: {e}")

# Warn user if no positions could be resolved
if not pos_list:
    st.error("⚠️ A valid parking layout (.pkl) is required to start detection. Please check the sidebar options.")

# ----------------- Video Handlers & Preview -----------------
if uploaded_video is not None and pos_list:
    # Write uploaded video stream to a temporary local file to play via OpenCV
    try:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_video.read())
        temp_video_path = tfile.name
        tfile.close()  # Close the file handle
        
        # Verify alignment using the first frame of the video
        cap = cv2.VideoCapture(temp_video_path)
        success, first_frame = cap.read()
        cap.release()
        
        if success:
            if not st.session_state.processing_done and not start_btn:
                st.markdown("<h3 class='section-header'>👀 Verification Preview</h3>", unsafe_allow_html=True)
                # Compute overlays on the first frame
                img_pro = process_video_frame(first_frame)
                free_spaces, slot_status, annotated_preview = check_parking_space(
                    img_pro, first_frame, pos_list, threshold_factor
                )
                
                # Convert BGR preview frame to RGB for Streamlit rendering
                preview_rgb = cv2.cvtColor(annotated_preview, cv2.COLOR_BGR2RGB)
                st.image(
                    preview_rgb, 
                    caption="Layout Verification (Verifying Slot Bounding Box Alignment on First Frame)", 
                    use_container_width=True
                )
                st.success("🎉 First frame preview loaded! Please verify that the parking boundary boxes align correctly with the physical slots. Click 'Start Processing' in the sidebar to start analytics.")
        else:
            st.error("❌ Failed to read the first frame of the uploaded video. Please verify the video format.")
            
    except Exception as e:
        st.error(f"❌ Error setting up video preview: {e}")
        temp_video_path = None
else:
    temp_video_path = None
    if uploaded_video is None:
        st.warning("👈 Please upload a parking lot video in the sidebar to begin.")

# ----------------- Video Processing Loop -----------------
if start_btn and temp_video_path and pos_list:
    st.session_state.processing_done = False
    st.session_state.history_log = []
    st.session_state.final_stats = None
    
    st.markdown("<h3 class='section-header'>📺 Live Detection & Processing</h3>", unsafe_allow_html=True)
    
    # Setup layout grids for processing feeds
    col_orig, col_proc = st.columns(2)
    with col_orig:
        st.markdown("#### Annotated Video Feed")
        orig_placeholder = st.empty()
    with col_proc:
        st.markdown("#### Binary Dilation Feed (Computer Vision Threshold)")
        proc_placeholder = st.empty()
        
    metric_placeholder = st.empty()
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        cap = cv2.VideoCapture(temp_video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        frame_idx = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            frame_idx += 1
            
            # Process frames at intervals to optimize UI performance
            if frame_idx % 3 != 0 and frame_idx < total_frames - 5:
                continue
                
            # Compute thresholds and dilate edges
            img_pro = process_video_frame(frame)
            
            # Check slot occupancy
            free_spaces, slot_status, annotated_frame = check_parking_space(
                img_pro, frame, pos_list, threshold_factor
            )
            
            total_slots = len(pos_list)
            occupied_slots = total_slots - free_spaces
            occ_percentage = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
            
            # Record analytics history
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.history_log.append({
                "Timestamp": timestamp,
                "Total Slots": total_slots,
                "Occupied Slots": occupied_slots,
                "Free Slots": free_spaces,
                "Occupancy Percentage": round(occ_percentage, 2)
            })
            
            # Render feeds
            annotated_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            orig_placeholder.image(annotated_rgb, use_container_width=True)
            proc_placeholder.image(img_pro, use_container_width=True)
            
            # Render metric cards
            with metric_placeholder.container():
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                m_col1.metric("Total Slots", total_slots)
                m_col2.metric("Occupied Slots", occupied_slots)
                m_col3.metric("Free Slots", free_spaces)
                m_col4.metric("Occupancy Percentage", f"{occ_percentage:.1f}%")
                
            # Update progress bar
            progress_pct = min(1.0, float(frame_idx) / max(1, total_frames))
            progress_bar.progress(progress_pct)
            status_text.text(f"Processing frame {frame_idx}/{total_frames} ({int(progress_pct * 100)}%)")
            
            # Prevent thread lockup
            time.sleep(0.01)
            
        cap.release()
        st.session_state.processing_done = True
        status_text.text("Processing Complete! Saving final report data...")
        
        # Calculate summary metrics
        log_entries = st.session_state.history_log
        if log_entries:
            avg_occ = sum(entry["Occupancy Percentage"] for entry in log_entries) / len(log_entries)
            peak_occ = max(entry["Occupancy Percentage"] for entry in log_entries)
        else:
            avg_occ = occ_percentage
            peak_occ = occ_percentage
            
        st.session_state.final_stats = {
            "total_slots": total_slots,
            "average_occupancy": avg_occ,
            "peak_occupancy": peak_occ,
            "free_slots_final": free_spaces,
            "occupied_slots_final": occupied_slots
        }
        
    except Exception as e:
        st.error(f"❌ An error occurred during video processing: {e}")
    finally:
        # Clean up temporary video file safely
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                os.unlink(temp_video_path)
            except Exception:
                pass

# ----------------- Post Processing Reports & Analysis -----------------
if st.session_state.processing_done and st.session_state.final_stats:
    st.markdown("<h3 class='section-header'>📊 Session Summary & Analytics</h3>", unsafe_allow_html=True)
    
    # Display Static Metric Dashboard for complete session
    stats = st.session_state.final_stats
    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    res_col1.metric("Total Monitored Slots", stats["total_slots"])
    res_col2.metric("Average Occupancy Rate", f"{stats['average_occupancy']:.1f}%")
    res_col3.metric("Peak Occupancy Rate", f"{stats['peak_occupancy']:.1f}%")
    res_col4.metric("Remaining Free Slots", stats["free_slots_final"])
    
    st.markdown("---")
    
    col_csv, col_summary = st.columns(2)
    
    with col_csv:
        st.subheader("💾 Export Report Data")
        st.write("Generate and download a CSV report containing the detailed timeline logs of the parking statistics.")
        
        csv_data = generate_csv(st.session_state.history_log)
        st.download_button(
            label="📥 Download CSV Report",
            data=csv_data,
            file_name=f"parking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with col_summary:
        st.subheader("📋 Parking Summary & Health")
        
        # Calculate rule-based occupancy level and recommendations
        avg_occ = stats["average_occupancy"]
        
        if avg_occ <= 40.0:
            status_label = "Low Occupancy"
            health_color = "🟢"
            health_desc = "Current parking utilization is healthy."
            recommendation = "Parking capacity is sufficient."
        elif avg_occ <= 70.0:
            status_label = "Moderate Occupancy"
            health_color = "🟡"
            health_desc = "Parking lot is operating normally."
            recommendation = "Moderate occupancy detected. Drivers should be directed to available spaces."
        elif avg_occ <= 90.0:
            status_label = "High Occupancy"
            health_color = "🟠"
            health_desc = "Parking demand is increasing."
            recommendation = "High occupancy detected. Consider opening overflow parking."
        else:
            status_label = "Nearly Full"
            health_color = "🔴"
            health_desc = "Parking lot is close to capacity."
            recommendation = "Parking lot is nearly full. Recommend redirecting incoming vehicles."
            
        summary_markdown = f"""
**Parking Summary**
- **Total Slots**: {stats['total_slots']}
- **Occupied Slots**: {stats['occupied_slots_final']}
- **Free Slots**: {stats['free_slots_final']}
- **Occupancy Percentage**: {stats['average_occupancy']:.1f}%

**Status**: {status_label}
**Recommendation**: {recommendation}
        """
        
        st.markdown(summary_markdown)
        
        st.markdown("### Parking Health")
        health_html = f"""
<div style="padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB; background-color: #F9FAFB; margin-top: 10px;">
    <span style="font-size: 1.5rem; margin-right: 10px;">{health_color}</span>
    <span style="font-weight: 600; font-size: 1.1rem; color: #1F2937;">{status_label}</span>
    <p style="margin: 5px 0 0 35px; color: #4B5563;">{health_desc}</p>
</div>
        """
        st.markdown(health_html, unsafe_allow_html=True)
