import cv2
import pytesseract

# Function to preprocess frame for OCR
def preprocess_frame(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive thresholding to handle different lighting conditions
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    return thresh

# Function to extract subtitles ROI
def extract_subtitles(frame):
    # Define ROI for subtitles (bottom center)
    roi_y = int(0.7 * frame.shape[0])  # Adjust as needed
    roi_x = int(0.1 * frame.shape[1])  # Adjust as needed
    roi_height = int(0.2 * frame.shape[0])  # Adjust as needed
    roi_width = int(0.6 * frame.shape[1])  # Adjust as needed
    
    # Extract ROI
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    
    return roi

# Function to perform OCR with Tesseract
def perform_ocr(image):
    # Define Tesseract configuration
    config = '--oem 3 --psm 6'  # LSTM OCR Engine, Assume a single uniform block of text
    result = pytesseract.image_to_string(image, config=config, lang='bod')
    return result

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
    ocr_result = perform_ocr(subtitles_roi)
    
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
