import cv2
import pytesseract
import pyttsx3
import time

# Replace with your Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Start camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Keep track of last spoken text to avoid repetition
last_text = ""

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize for display
    frame = cv2.resize(frame, (640, 480))

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(blur, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # OCR: detect text
    text = pytesseract.image_to_string(thresh).strip()

    if text != "" and text != last_text:
        print("Detected Text:", text)
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        last_text = text  # update last spoken text

    # Show camera and thresholded feed
    cv2.imshow("Smart Lens OCR", frame)
    cv2.imshow("Thresholded", thresh)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
