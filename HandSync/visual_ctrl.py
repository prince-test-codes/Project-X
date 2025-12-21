import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import math

# --- RYZEN CONFIGURATION ---
W_CAM, H_CAM = 480, 360
SKIP_RATIO = 2  
SMOOTHING = 5
FRAME_R = 80 
CLICK_THRESH_RATIO = 0.25

# --- SETUP ---
cap = cv2.VideoCapture(0)
cap.set(3, W_CAM)
cap.set(4, H_CAM)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0, 
    max_num_hands=1,
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Variables
p_loc_x, p_loc_y = 0, 0
c_loc_x, c_loc_y = 0, 0
frame_count = 0

# State Variables
pinch_start_time = 0
is_dragging = False
vol_cooldown = 0

w_scr, h_scr = pyautogui.size()

def get_dist(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

print(">>> POWER USER MODE: Drag, Volume, & Sniper Active.")

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    
    # 1. Frame Skipping for Performance
    run_ai = (frame_count % SKIP_RATIO == 0)
    lm_list = []
    
    if run_ai:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(hand_lms.landmark):
                    cx, cy = int(lm.x * W_CAM), int(lm.y * H_CAM)
                    lm_list.append([id, cx, cy])
    
    if len(lm_list) != 0:
        # Key Points
        x1, y1 = lm_list[8][1:]   # Index Tip
        x2, y2 = lm_list[12][1:]  # Middle Tip
        x4, y4 = lm_list[4][1:]   # Thumb Tip
        
        # Fingers Up Logic
        fingers = []
        # Thumb (Simple x-check)
        if lm_list[4][1] < lm_list[3][1]: fingers.append(1)
        else: fingers.append(0)
        # 4 Fingers
        for id in [8, 12, 16, 20]:
            if lm_list[id][2] < lm_list[id-2][2]: fingers.append(1)
            else: fingers.append(0)
            
        # Dynamic Calibration
        hand_size = get_dist(lm_list[0][1:], lm_list[5][1:])
        click_thresh = int(hand_size * CLICK_THRESH_RATIO)
        pinch_dist = get_dist((x4, y4), (x1, y1))

        # --- MODE 1: MOVEMENT & DRAG (Index Up) ---
        if fingers[1] == 1 and fingers[2] == 0 and fingers[4] == 0:
            
            # Check for Pinch (Click/Drag)
            if pinch_dist < click_thresh:
                if pinch_start_time == 0:
                    pinch_start_time = time.time()
                
                # If held for > 0.4s, start DRAGGING
                hold_time = time.time() - pinch_start_time
                if hold_time > 0.4:
                    if not is_dragging:
                        pyautogui.mouseDown()
                        is_dragging = True
                    cv2.putText(img, "DRAGGING...", (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                else:
                    cv2.putText(img, "Click...", (x1, y1-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            else:
                # RELEASE Logic
                if pinch_start_time != 0:
                    hold_time = time.time() - pinch_start_time
                    
                    if is_dragging:
                        # If we were dragging, drop it now
                        pyautogui.mouseUp()
                        is_dragging = False
                    elif hold_time < 0.4:
                        # If short tap, click
                        pyautogui.click()
                    
                    pinch_start_time = 0 # Reset

                # MOVE MOUSE
                x3 = np.interp(x1, (FRAME_R, W_CAM - FRAME_R), (0, w_scr))
                y3 = np.interp(y1, (FRAME_R, H_CAM - FRAME_R), (0, h_scr))
                
                # Sniper Mode Check? No, strictly Index Only for normal move.
                curr_smooth = SMOOTHING
                
                c_loc_x = p_loc_x + (x3 - p_loc_x) / curr_smooth
                c_loc_y = p_loc_y + (y3 - p_loc_y) / curr_smooth
                
                try: pyautogui.moveTo(c_loc_x, c_loc_y)
                except: pass
                p_loc_x, p_loc_y = c_loc_x, c_loc_y
                cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)

        # --- MODE 2: SCROLL (Index + Middle) ---
        elif fingers[1] == 1 and fingers[2] == 1:
            cv2.putText(img, "SCROLL", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            if y1 < H_CAM // 3: pyautogui.scroll(20)
            elif y1 > (H_CAM // 3) * 2: pyautogui.scroll(-20)

        # --- MODE 3: VOLUME (Thumb + Pinky "Shaka") ---
        elif fingers[0] == 1 and fingers[4] == 1 and fingers[1] == 0:
            cv2.putText(img, "VOLUME", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Use Y-position of Pinky to control volume
            # Wait for cooldown so it doesn't spam
            if time.time() - vol_cooldown > 0.2:
                if y1 < H_CAM // 3: # Hand High
                    pyautogui.press('volumeup')
                    vol_cooldown = time.time()
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                elif y1 > (H_CAM // 3) * 2: # Hand Low
                    pyautogui.press('volumedown')
                    vol_cooldown = time.time()
                    cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)

        # --- MODE 4: SNIPER (Index + Pinky "Horns") ---
        elif fingers[1] == 1 and fingers[4] == 1 and fingers[2] == 0:
             cv2.putText(img, "SNIPER MODE", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
             
             # Ultra High Smoothing = Slow Motion
             SNIPER_SMOOTH = 20 
             
             x3 = np.interp(x1, (FRAME_R, W_CAM - FRAME_R), (0, w_scr))
             y3 = np.interp(y1, (FRAME_R, H_CAM - FRAME_R), (0, h_scr))
             
             c_loc_x = p_loc_x + (x3 - p_loc_x) / SNIPER_SMOOTH
             c_loc_y = p_loc_y + (y3 - p_loc_y) / SNIPER_SMOOTH
             
             try: pyautogui.moveTo(c_loc_x, c_loc_y)
             except: pass
             p_loc_x, p_loc_y = c_loc_x, c_loc_y
             
             # Visual: Red Target
             cv2.line(img, (x1-10, y1), (x1+10, y1), (0,0,255), 2)
             cv2.line(img, (x1, y1-10), (x1, y1+10), (0,0,255), 2)

    frame_count += 1
    cv2.imshow("Power User Controls", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()