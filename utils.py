import pickle
import pandas as pd
import os
import io

def load_parking_positions(uploaded_file_or_path):
    """
    Loads parking slot positions from a pickle (.pkl) file.
    Supports file paths and uploaded file-like objects from Streamlit.
    Handles legacy formats and normalizes layout list to:
    [(x, y, width, height, slot_number), ...]
    
    Args:
        uploaded_file_or_path (str/Path/UploadedFile): Input file source.
        
    Returns:
        list: Normalized list of slot tuples (x, y, w, h, slot_num).
    """
    pos_list = []
    try:
        if isinstance(uploaded_file_or_path, (str, os.PathLike)):
            with open(uploaded_file_or_path, 'rb') as f:
                pos_list = pickle.load(f)
        else:
            # File-like object from Streamlit file_uploader
            # Read bytes directly
            bytes_data = uploaded_file_or_path.read()
            # Reset seek position if reused
            uploaded_file_or_path.seek(0)
            pos_list = pickle.loads(bytes_data)
            
        # Normalize layouts to standard 5-element tuple format (x, y, w, h, slot_num)
        if pos_list:
            if not isinstance(pos_list, list):
                pos_list = list(pos_list)
            
            first_element = pos_list[0]
            if len(first_element) == 2:  # Old (x, y) format
                pos_list = [(x, y, 107, 48, i + 1) for i, (x, y) in enumerate(pos_list)]
            elif len(first_element) == 3:  # Old (x, y, slot_number) format
                pos_list = [(x, y, 107, 48, slot_num) for x, y, slot_num in pos_list]
                
    except Exception as e:
        raise ValueError(f"Error parsing layout file: {e}")
        
    return pos_list

def generate_csv(history_log):
    """
    Converts a history tracking list of statistics into a downloadable CSV string.
    
    Args:
        history_log (list of dict): Entries containing Timestamp, Total, Occupied, Free, Occupancy %
        
    Returns:
        str: CSV content formatted as a UTF-8 string.
    """
    if not history_log:
        df = pd.DataFrame(columns=["Timestamp", "Total Slots", "Occupied Slots", "Free Slots", "Occupancy Percentage"])
    else:
        df = pd.DataFrame(history_log)
        
    # Convert dataframe to CSV string
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def create_default_layout(dest_path):
    """
    Programmatically creates a default sample_layout.pkl containing 12 parking slot coordinates
    in a clean 2x6 grid pattern. This ensures the app can run out-of-the-box.
    
    Args:
        dest_path (str): File destination path to write the pickle data.
    """
    # Grid parameters based on standard slot dimensions
    width = 107
    height = 48
    slots = []
    
    # Row 1 (6 slots)
    x_positions_r1 = [50, 180, 310, 440, 570, 700]
    y_r1 = 150
    for i, x in enumerate(x_positions_r1):
        slots.append((x, y_r1, width, height, i + 1))
        
    # Row 2 (6 slots)
    x_positions_r2 = [50, 180, 310, 440, 570, 700]
    y_r2 = 350
    for i, x in enumerate(x_positions_r2):
        slots.append((x, y_r2, width, height, i + 7))
        
    # Ensure directory path exists
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    
    # Save list to file
    with open(dest_path, 'wb') as f:
        pickle.dump(slots, f)
