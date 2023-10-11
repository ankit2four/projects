import cv2 
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import numpy as np 

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands 
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin,volMax = volume.GetVolumeRange()[:2]

while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark):
                h,w,_ = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy]) 
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    
    if lmList != []:
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]

        x3,y3 = lmList[4][1],lmList[4][2]
        x4,y4 = lmList[12][1],lmList[12][2]

        cv2.circle(img,(x1,y1),4,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),4,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        

        cv2.circle(img,(x3,y3),4,(0,255,0),cv2.FILLED)
        cv2.circle(img,(x4,y4),4,(0,255,0),cv2.FILLED)
        cv2.line(img,(x3,y3),(x4,y4),(0,255,0),3)
        


        length = hypot(x2-x1,y2-y1)

        bright = np.interp(length,[5,140],[15,100])
        cv2.putText(img, "BRIGHTNESS ", (x2+5,y2+5), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,0,0), 1)
        print(bright,length)
        sbc.set_brightness(int(bright))

        length1 = hypot(x4-x3,y4-y3)

        vol = np.interp(length1,[5,120],[volMin,volMax])
        cv2.putText(img, "VOLUME ", (x4+5,y4+5), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0,0,0), 1)
        print(vol,length1)
        volume.SetMasterVolumeLevel(vol, None)

        # Hand range 15 - 220
        # Volume range -63.5 - 0.0
        
    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
