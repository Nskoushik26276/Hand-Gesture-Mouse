!pip install opencv-python mediapipe pyautogui
import cv2
import mediapipe as mp
import pyautogui
from math import hypot

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe hand tracking
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Get screen size for cursor movement scaling
screen_w, screen_h = pyautogui.size()

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip horizontally for natural hand movements
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hand landmarks
    result = hand_detector.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            # Get the position of the index finger tip (landmark 8)
            x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            y = int(hand_landmarks.landmark[8].y * frame.shape[0])

            # Scale to screen coordinates and move the cursor
            screen_x = int(hand_landmarks.landmark[8].x * screen_w)
            screen_y = int(hand_landmarks.landmark[8].y * screen_h)
            pyautogui.moveTo(screen_x, screen_y)

            # Check the distance between thumb and index finger for click gesture
            thumb_x = hand_landmarks.landmark[4].x * frame.shape[1]
            thumb_y = hand_landmarks.landmark[4].y * frame.shape[0]
            distance = hypot(thumb_x - x, thumb_y - y)

            # If thumb and index finger are close, simulate a click
            if distance < 20:
                pyautogui.click()
                pyautogui.sleep(0.2)  # Prevent double clicks

    # Display the frame with landmarks
    cv2.imshow("Hand Mouse Control", frame)

    # Break the loop when 'ESC' is pressed
    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

# Release the webcam and close any open windows
cap.release()
cv2.destroyAllWindows()
