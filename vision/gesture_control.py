"""Webcam hand gesture control."""
import time
import cv2
import mediapipe as mp
import pyautogui

def main():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open webcam. Check camera permissions and other applications.")
        camera.release()
        return
    screen_w, screen_h = pyautogui.size()
    hands_api, drawing = mp.solutions.hands, mp.solutions.drawing_utils
    last_scroll, was_pinch, was_middle = 0.0, False, False
    try:
        with hands_api.Hands(max_num_hands=1,min_detection_confidence=0.7,min_tracking_confidence=0.7) as hands:
            while True:
                ok, frame = camera.read()
                if not ok: print("Could not read webcam frame."); break
                frame = cv2.flip(frame,1)
                result = hands.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
                label, pinch, middle_pinch = "No hand detected", False, False
                if result.multi_hand_landmarks:
                    hand = result.multi_hand_landmarks[0]; drawing.draw_landmarks(frame,hand,hands_api.HAND_CONNECTIONS); p=hand.landmark
                    t,i,m,r,pk = p[4],p[8],p[12],p[16],p[20]; ip,mpip,rp,pp=p[6],p[10],p[14],p[18]
                    dist=lambda a,b: ((a.x-b.x)**2+(a.y-b.y)**2)**0.5
                    io,mo,ro,po = i.y<ip.y,m.y<mpip.y,r.y<rp.y,pk.y<pp.y
                    pinch,middle_pinch = dist(t,i)<0.045,dist(t,m)<0.045
                    if pinch:
                        label="Pinch: click"
                        if not was_pinch: pyautogui.click()
                    elif middle_pinch:
                        label="Thumb + middle: double click"
                        if not was_middle: pyautogui.doubleClick()
                    elif io and not mo and not ro and not po:
                        label="Point: move pointer"; margin=0.08
                        x=min(max((i.x-margin)/(1-2*margin),0),1); y=min(max((i.y-margin)/(1-2*margin),0),1)
                        pyautogui.moveTo(int(x*screen_w),int(y*screen_h),duration=0.03)
                    elif i.y>ip.y and not mo and not ro and not po:
                        label="Point down: scroll"; now=time.monotonic()
                        if now-last_scroll>=0.25: pyautogui.scroll(-3); last_scroll=now
                    elif io and mo and ro and po: label="Open hand"
                    else: label="Hand detected"
                was_pinch,was_middle=pinch,middle_pinch
                cv2.putText(frame,label,(15,35),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
                cv2.imshow("FluffelNexus Gesture Control - press Q to quit",frame)
                if cv2.waitKey(1)&0xFF in (ord("q"),ord("Q")): break
    except Exception as exc: print(f"Gesture control stopped: {exc}")
    finally: camera.release(); cv2.destroyAllWindows()

if __name__=="__main__": main()
