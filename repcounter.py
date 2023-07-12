import numpy as np
import posedetect as pm
import cv2

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
color = (0, 0, 255)
lm_wanted = []
per = 0
bar = 0
angle_limits = ()
pullups_color = (0, 0, 255)
squats_color = (0, 0, 255)
abs_color = (0, 0, 255)
pushups_color = (0, 0, 255)


def click_event(event, x, y, params, flags):
    global lm_wanted
    global angle_limits
    global count, per, bar
    global pullups_color, squats_color, abs_color, pushups_color

    if event == cv2.EVENT_LBUTTONDOWN:
        if (x > 25) & (x < 170) & (y > 150) & (y < 200):
            lm_wanted = [11, 13, 15, 12, 14, 16]
            angle_limits = (40, 140)
            count = 0
            pullups_color = (255, 0, 0)
            squats_color = (0, 0, 255)
            abs_color = (0, 0, 255)
            pushups_color = (0, 0, 255)
        if (x > 25) & (x < 170) & (y > 225) & (y < 275):
            lm_wanted = [24, 26, 28, 23, 25, 27]
            angle_limits = (40, 140)
            count = 0
            pullups_color = (0, 0, 255)
            squats_color = (255, 0, 0)
            abs_color = (0, 0, 255)
            pushups_color = (0, 0, 255)
        if (x > 25) & (x < 170) & (y > 300) & (y < 350):
            lm_wanted = [11, 23, 27, 12, 24, 28]
            angle_limits = (90, 150)
            count = 0
            pullups_color = (0, 0, 255)
            squats_color = (0, 0, 255)
            abs_color = (255, 0, 0)
            pushups_color = (0, 0, 255)
        if (x > 25) & (x < 170) & (y > 375) & (y < 425):
            lm_wanted = [11, 13, 15, 12, 14, 16]
            angle_limits = (50, 140)
            count = 0
            pullups_color = (0, 0, 255)
            squats_color = (0, 0, 255)
            abs_color = (0, 0, 255)
            pushups_color = (255, 0, 0)
        if (x > 25) & (x < 170) & (y > 450) & (y < 500):
            lm_wanted = []
            count = 0
            per = 0
            bar = 0
            pullups_color = (0, 0, 255)
            squats_color = (0, 0, 255)
            abs_color = (0, 0, 255)
            pushups_color = (0, 0, 255)


while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
    cv2.rectangle(img, (0, 600), (125, 720), (0, 0, 255), cv2.FILLED)
    cv2.rectangle(img, (25, 150), (170, 200), pullups_color, cv2.FILLED)
    cv2.putText(img, 'PULL-UPS', (35, 185), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (255, 255, 255), 2)
    cv2.rectangle(img, (25, 225), (170, 275), squats_color, cv2.FILLED)
    cv2.putText(img, 'SQUATS', (50, 260), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (255, 255, 255), 2)
    cv2.rectangle(img, (25, 300), (170, 350), abs_color, cv2.FILLED)
    cv2.putText(img, 'ABS', (70, 335), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (255, 255, 255), 2)
    cv2.rectangle(img, (25, 375), (170, 425), pushups_color, cv2.FILLED)
    cv2.putText(img, 'PUSH-UPS', (35, 410), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (255, 255, 255), 2)
    cv2.rectangle(img, (25, 450), (170, 500), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, 'RESET', (60, 485), cv2.FONT_HERSHEY_PLAIN, 1.5,
                (255, 255, 255), 2)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    cv2.putText(img, f'{int(per)} %', (1075, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)
    cv2.putText(img, str(int(count)), (35, 690), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 10)
    if lm_wanted != []:
        if len(lmList) != 0:
            angle1 = detector.findAngle(img, lm_wanted[0], lm_wanted[1], lm_wanted[2])
            per1 = np.interp(angle1, angle_limits, (100, 0))
            bar1 = np.interp(angle1, angle_limits, (100, 650))

            angle2 = detector.findAngle(img, lm_wanted[3], lm_wanted[4], lm_wanted[5])
            per2 = np.interp(angle2, angle_limits, (100, 0))
            bar2 = np.interp(angle2, angle_limits, (100, 650))

            per = (per1 + per2) / 2
            bar = (bar1 + bar2) / 2
            color = (0, 0, 255)

            if per == 100:
                color = (255, 0, 0)
                if direction == 0:
                    count += 0.5
                    direction = 1

            if per == 0:
                color = (0, 0, 255)
                if direction == 1:
                    count += 0.5
                    direction = 0

            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(img, f'{int(per)} %', (1075, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                        color, 4)
            cv2.putText(img, str(int(count)), (35, 690), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 10)

    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', click_event)
    cv2.waitKey(1)