!pip install opencv-python mediapipe pyautogui
import cv2
import mediapipe as mp
import pyautogui
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)  # Mirror the image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    h, w, _ = img.shape
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)
            lm_list = hand_landmark.landmark
            index_finger_tip = lm_list[8]
            thumb_tip = lm_list[4]
            x = int(index_finger_tip.x * w)
            y = int(index_finger_tip.y * h)
            screen_x = int(index_finger_tip.x * screen_w)
            screen_y = int(index_finger_tip.y * screen_h)
            pyautogui.moveTo(screen_x, screen_y)
            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)
            distance = ((x - thumb_x) ** 2 + (y - thumb_y) ** 2) ** 0.5
            if distance < 40:
                pyautogui.click()
                cv2.putText(img, "Click", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow("Hand Gesture Control", img)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
