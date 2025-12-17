import cv2
import mediapipe as mp
import pyautogui
import time
import math

# Configuration
COOLDOWN = 0.5
W_CAM, H_CAM = 640, 480
last_action = 0

# Initialize
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

def get_dist(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

def get_fingers(hand_lms):
    fingers = []
    # Thumb (Horizontal comparison)
    if hand_lms.landmark[4].x < hand_lms.landmark[3].x: fingers.append(1)
    else: fingers.append(0)
    # Other 4 fingers (Vertical comparison)
    for tip in [8, 12, 16, 20]:
        if hand_lms.landmark[tip].y < hand_lms.landmark[tip-2].y: fingers.append(1)
        else: fingers.append(0)
    return fingers

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    label = "Scanning..."
    curr_time = time.time()

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            fingers = get_fingers(hand_lms)
            
            # Key Distances
            pinch_dist = get_dist(hand_lms.landmark[4], hand_lms.landmark[8])
            
            # --- REDESIGNED PRIORITY LOGIC ---
            
            # 1. PRIORITY: NEUTRAL (Palm)
            if fingers == [1, 1, 1, 1, 1]:
                label = "NEUTRAL / READY"

            # 2. CLOSE TAB (OK Sign - Thumb/Index close, Mid/Ring/Pinky UP)
            elif pinch_dist < 0.04 and fingers[2] == 1:
                if curr_time - last_action > COOLDOWN:
                    pyautogui.hotkey('ctrl', 'w')
                    last_action = curr_time
                label = "CLOSE TAB"

            # 3. PLAY (Fist)
            elif fingers == [0, 0, 0, 0, 0]:
                if curr_time - last_action > COOLDOWN:
                    pyautogui.press('playpause')
                    last_action = curr_time
                label = "PLAY"

            # 4. PAUSE (4 Fingers Up, Thumb Tucked)
            elif fingers == [0, 1, 1, 1, 1]:
                if curr_time - last_action > COOLDOWN:
                    pyautogui.press('space')
                    last_action = curr_time
                label = "PAUSE"

            # 5. SCROLL (Index + Middle Up ONLY)
            elif fingers == [0, 1, 1, 0, 0]:
                y_pos = hand_lms.landmark[8].y
                if y_pos < 0.4: 
                    pyautogui.scroll(150)
                    label = "SCROLL UP"
                elif y_pos > 0.6: 
                    pyautogui.scroll(-150)
                    label = "SCROLL DOWN"

            # 6. CLICK (Index Up, then Pinch Thumb)
            elif fingers == [1, 1, 0, 0, 0]: # Thumb and Index up
                if pinch_dist < 0.04:
                    if curr_time - last_action > COOLDOWN:
                        pyautogui.click()
                        last_action = curr_time
                    label = "LEFT CLICK"
                else:
                    label = "PREPARING CLICK"

            # 7. ADDRESSING (Index Pointing Only)
            elif fingers == [0, 1, 0, 0, 0]:
                if curr_time - last_action > COOLDOWN:
                    pyautogui.press('tab')
                    last_action = curr_time
                label = "ADDRESS (TAB)"

    # Visual Feedback
    cv2.rectangle(img, (10, 10), (320, 60), (30, 30, 30), -1)
    cv2.putText(img, f"CMD: {label}", (20, 45), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Gesture Master v3", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()