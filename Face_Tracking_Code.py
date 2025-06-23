import cv2
import serial
import time

# Initialize serial communication with Arduino (adjust COM port)
try:
    arduino = serial.Serial('COM7', 9600, timeout=1)  # Adjust 'COM7' to your Arduino port
    time.sleep(2)  # Wait for Arduino to initialize
except serial.SerialException as e:
    print(f"Error: Could not open serial port: {e}")
    exit()

# Load pre-trained face detector (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
if face_cascade.empty():
    print("Error: Could not load Haar Cascade classifier.")
    exit()

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)  # Reduced resolution for smoother performance
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Constants
FRAME_WIDTH = 640  # Width of the camera frame
FRAME_HEIGHT = 480  # Height of the camera frame
send_interval = 2  # Interval to wait before sending coordinates again (in seconds)
last_sent_time = time.time()  # Initialize last sent time

def send_position_to_arduino(x, y):
    """Send the X and Y positions to the Arduino."""
    try:
        position = f"{x},{y}\n"  # Format: "x,y"
        arduino.write(position.encode())  # Encode to bytes and send to Arduino
        print(f"Sent to Arduino: {position.strip()}")
    except serial.SerialException as e:
        print(f"Error sending to Arduino: {e}")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Mirror the frame to act as a mirror view
    frame = cv2.flip(frame, 1)

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if 2 seconds have passed since the last send
    current_time = time.time()
    if current_time - last_sent_time >= send_interval:
        if len(faces) > 0:
            # Process the first detected face
            (x, y, w, h) = faces[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Calculate the center of the face in the X and Y directions
            centerX = x + w // 2
            centerY = y + h // 2
            print(f"Face detected at X={centerX}, Y={centerY}")  # Debug print

            # Send coordinates to Arduino (without scaling to servo range)
            send_position_to_arduino(centerX, centerY)

            # Update the last sent time
            last_sent_time = current_time

        else:
            # If no face is detected, send default "0,0" to turn off the laser
            send_position_to_arduino(0, 0)
            print("No face detected. Laser turned off.")

    # Display the frame with rectangles
    cv2.imshow('Face Tracking', frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
