import cv2
import numpy as np

def process_video_frame(img):
    """
    Applies image preprocessing pipeline: Gray -> Gaussian Blur -> Adaptive Threshold -> Median Blur -> Dilation.
    Keep this identical to the original implementation.
    
    Args:
        img (ndarray): Raw input video frame (BGR).
        
    Returns:
        ndarray: Preprocessed binary dilated frame.
    """
    # 1. Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Apply Gaussian Blur to smooth out noise
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    
    # 3. Apply Adaptive Thresholding to create binary image (edges highlighted)
    img_threshold = cv2.adaptiveThreshold(
        img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16
    )
    
    # 4. Apply Median Blur to remove small pixel noise
    img_median = cv2.medianBlur(img_threshold, 5)
    
    # 5. Apply Dilation to thicken white edges for better counting
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)
    
    return img_dilate

def put_text_rect(img, text, pos, scale=1, thickness=1, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=3):
    """
    Draws text with a filled background rectangle using only native OpenCV.
    Replaces the cvzone.putTextRect library dependency.
    
    Args:
        img (ndarray): Image to draw on.
        text (str): Text message to overlay.
        pos (tuple): (x, y) bottom-left position of the text baseline.
        scale (float): Font scale factor.
        thickness (int): Font stroke thickness.
        colorT (tuple): Text color in BGR format.
        colorR (tuple): Background rectangle color in BGR format.
        offset (int): Padding around the text block.
        
    Returns:
        ndarray: Image with text overlays.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Calculate text dimensions
    (w, h), baseline = cv2.getTextSize(text, font, scale, thickness)
    x, y = pos
    
    # Define rectangle coordinates with offset padding
    x1, y1 = x - offset, y - h - offset
    x2, y2 = x + w + offset, y + baseline + offset
    
    # Draw background box
    cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
    # Draw text
    cv2.putText(img, text, (x, y), font, scale, colorT, thickness)
    return img

def check_parking_space(img_pro, img, pos_list, threshold_factor=0.15):
    """
    Checks the occupancy status of each parking space defined in pos_list.
    Draws red rectangles for occupied slots and green rectangles for free slots.
    
    Args:
        img_pro (ndarray): Preprocessed binary dilated frame.
        img (ndarray): Raw BGR frame to draw annotations on.
        pos_list (list): Bounding box layout list of tuples (x, y, w, h, slot_num).
        threshold_factor (float): Ratio used to compute occupancy threshold.
        
    Returns:
        space_counter (int): Number of free spaces.
        slot_status (dict): Maps slot_num to occupancy boolean (True if occupied).
        annotated_img (ndarray): BGR image with bounding boxes and text overlays.
    """
    space_counter = 0
    slot_status = {}
    
    # Create copy of image to prevent side-effects on source frame
    annotated_img = img.copy()
    
    for pos in pos_list:
        # Extract slot bounds and identifier
        x, y, w, h, slot_num = pos
        
        # Crop parking slot region
        img_crop = img_pro[y:y + h, x:x + w]
        # Count non-zero (white) pixels indicating vehicle edge density
        count = cv2.countNonZero(img_crop)
        # Compute threshold based on size of slot and threshold factor
        threshold = w * h * threshold_factor
        
        # Decide occupancy
        is_occupied = count >= threshold
        slot_status[slot_num] = is_occupied
        
        if not is_occupied:
            color = (0, 255, 0)  # Green for free
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)  # Red for occupied
            thickness = 2
            
        # Draw parking box
        cv2.rectangle(annotated_img, (x, y), (x + w, y + h), color, thickness)
        
        # Draw labels: Slot number and Edge density pixel counts
        put_text_rect(
            annotated_img, 
            f"Slot {slot_num}", 
            (x, y + 15), 
            scale=0.4, 
            thickness=1, 
            colorT=(255, 255, 255), 
            colorR=color, 
            offset=2
        )
        put_text_rect(
            annotated_img, 
            f"{count}/{int(threshold)}", 
            (x, y + h - 3), 
            scale=0.4, 
            thickness=1, 
            colorT=(255, 255, 255), 
            colorR=color, 
            offset=2
        )
        
    return space_counter, slot_status, annotated_img
