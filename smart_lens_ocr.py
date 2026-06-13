import cv2
import pytesseract

# Set path to Tesseract OCR (adjust if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize for display
    frame = cv2.resize(frame, (640, 480))
    
    # Convert to grayscale (better for OCR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Optional: threshold for better OCR
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # OCR: detect text
    text = pytesseract.image_to_string(thresh)
    if text.strip() != "":
        print("Detected Text:", text.strip())

    # Show video feed
    cv2.imshow("Smart Lens OCR", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
