import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    screen_width, screen_height = pyautogui.size()
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            index_pip = hand_landmarks.landmark[6] 
            middle_tip = hand_landmarks.landmark[12]
            middle_pip = hand_landmarks.landmark[10]
            ring_tip = hand_landmarks.landmark[16]
            ring_pip = hand_landmarks.landmark[14]
            pinky_tip = hand_landmarks.landmark[20]
            pinky_pip = hand_landmarks.landmark[18]

            # --- EXAMPLE 1: Pinch (Thumb + Index Finger) ---
            distance_pinch = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            
            # --- EXAMPLE 2: Index Finger stretched ---
            is_index_open = index_tip.y < index_pip.y
            
            # --- EXAMPLE 3: Distance from Thumb to middle finger ---
            distance_middle = ((thumb_tip.x - middle_tip.x) ** 2 + (thumb_tip.y - middle_tip.y) ** 2) ** 0.5

            # --- EXAMPLE 4: Open hand ---
            is_middle_open = middle_tip.y < middle_pip.y
            is_ring_open = ring_tip.y < ring_pip.y
            is_pinky_open = pinky_tip.y < pinky_pip.y

            if is_index_open and is_middle_open and is_ring_open and is_pinky_open:
                label = 'Open Hand'
            # Logik für Textausgabe kombinieren
            elif distance_pinch < 0.05:
                label = 'Pinch (Thumb + Index)'
                pyautogui.click()
            elif distance_middle < 0.05:
                label = 'Klick (Thumb + Middle)'
                
            elif is_index_open:
                label = 'Index Finger stretched'
                pyautogui.moveTo(int(index_tip.x * screen_width), int(index_tip.y * screen_height), duration=0.1)
            else:
                label = 'Closed Hand'
                
            cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
    cv2.imshow('Gesture Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
