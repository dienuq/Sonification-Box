#anaconda -> conda activate osc
#anaconda terminal: cd to the file directory where handtracking.py file is
#anaconda terminal: python Handtracking.py

import cv2
import mediapipe as mp
import time
import argparse
import time

from pythonosc import udp_client

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

data = ' '


parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

while True:
    
    success, img = cap.read()

    # flip the image 
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # identify left/right hand 
                #currentHand = results.multi_handedness[0].classification[0].label
                

                #print(currentHand)
                
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)

                data = data + str(cx) + " " + str(cy) + " "

                #if (currentHand == 'Left'):
                 #   dataLeft = dataLeft + str(cx) + " " + str(cy) + " "
                #else:
                    #dataRight = dataRight + str(cx) + " " + str(cy) + " "
                      

            #send hand landmarks
            client.send_message("/wek/inputs", data)
            #client.send_message("/wek/inputs/left", dataLeft)
            #client.send_message("/wek/inputs/right", dataRight)
            time.sleep(0.01)
            data = ''
            #dataLeft = ''
            #dataRight = ''
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



    