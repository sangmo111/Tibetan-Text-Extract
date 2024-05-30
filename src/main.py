import cv2
import pytesseract

# Function to preprocess frame
def preprocess_frame(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast using histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_gray = clahe.apply(gray)
    
    return enhanced_gray

# Function to extract subtitles
def extract_subtitles(frame):
    # Define ROI for subtitles (bottom center)
    roi_y = int(0.8 * frame.shape[0])  # Adjust as needed
    roi_x = int(0.1 * frame.shape[1])  # Adjust as needed
    roi_height = int(0.2 * frame.shape[0])  # Adjust as needed
    roi_width = int(0.8 * frame.shape[1])  # Adjust as needed
    
    # Extract ROI
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    
    return roi

# Open the video file
video_path = "/Users/jinpa/Downloads/Nyingtam_final_jinpa_jungney.mov"  # Update with the path to your video file
video = cv2.VideoCapture(video_path)

# Check if the video is opened successfully
if not video.isOpened():
    print("Error: Unable to open video file.")
    exit()

# Timestamp inputs (in seconds)
timestamps = [33, 39, 47, 53, 62]  # Update with your desired timestamps

# Iterate through each timestamp
for timestamp in timestamps:
    # Set the video capture to the desired timestamp
    video.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)

    # Read the frame at the current timestamp
    ret, frame = video.read()

    # Check if frame is read successfully
    if not ret:
        print("Error: Unable to read frame at timestamp", timestamp)
        continue

    # Preprocess frame
    processed_frame = preprocess_frame(frame)
    
    # Extract subtitles ROI
    subtitles_roi = extract_subtitles(processed_frame)
    
    # Perform OCR on subtitles ROI
    ocr_result = pytesseract.image_to_string(subtitles_roi, lang='bod')
    
    # Print OCR result
    print("Timestamp:", timestamp, "OCR Result:", ocr_result)
    
    # Display the frame with subtitles ROI
    cv2.imshow('Frame at Timestamp {}'.format(timestamp), frame)
    cv2.imshow('Subtitles ROI at Timestamp {}'.format(timestamp), subtitles_roi)
    
    # Wait for a key press to close the image window and proceed
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Release the video capture
video.release()
