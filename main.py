import glob
import os
import cv2
import time
from emailing import send_email
video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
status_list = []
count = 1

def clean_folder():
    print("Clean_Folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("Clean_Folder function Ended")
while True:
    status = 0
    check,frame = video.read()

    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_g = cv2.GaussianBlur(grey_frame,(21,11), 0)


    if first_frame is None:
        first_frame = grey_frame_g

    alpha_frame = cv2.absdiff(first_frame, grey_frame_g)

    thresh_frame = cv2.threshold(alpha_frame,60,255,cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    contours,check, = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 2000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 1 :
        send_email(image_with_object)
        clean_folder()




    cv2.imshow("My video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
