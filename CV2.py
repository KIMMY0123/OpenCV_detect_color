import cv2
import numpy as np

def find_centroid(mask, frame, color_name, color_bgr):
    contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area > 500:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                cv2.circle(frame, (cx, cy), 5, color_bgr, -1)
                cv2.putText(frame, f"{color_name} ({cx},{cy})", (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 2)

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("cann't connected the camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Unable to read images from camera")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)
# -----------------------------------------------
    lower_grean1 = np.array([36, 50, 50])
    upper_grean1 = np.array([70, 255, 255])

    lower_green2 = np.array([70, 50, 50])
    upper_green2 = np.array([86, 255, 255])
   
    mask2 = cv2.inRange(hsv, lower_grean1, upper_grean1) + cv2.inRange(hsv, lower_green2, upper_green2)
# -----------------------------------------------
    lower_blue1 = np.array([90, 50, 50])
    upper_blue1 = np.array([110, 255, 255])
    
    lower_blue2 = np.array([110, 50, 50])
    upper_blue2 = np.array([130, 255, 255])
    
    mask3 = cv2.inRange(hsv, lower_blue1, upper_blue1) + cv2.inRange(hsv, lower_blue2, upper_blue2)
# -----------------------------------------------
    lower_yellow1 = np.array([15, 50, 50])
    upper_yellow1 = np.array([25, 255, 255])

    lower_yellow2 = np.array([25, 50, 50])
    upper_yellow2 = np.array([35, 255, 255])

    mask4 = cv2.inRange(hsv, lower_yellow1, upper_yellow1) + cv2.inRange(hsv, lower_yellow2, upper_yellow2)
# -----------------------------------------------
    mask_all = cv2.bitwise_or(mask1, mask2)
    mask_all = cv2.bitwise_or(mask_all, mask3)
    mask_all = cv2.bitwise_or(mask_all, mask4)


    result = cv2.bitwise_and(frame, frame, mask=mask_all)

    find_centroid(mask1, frame, "Red", (0, 0, 255))
    find_centroid(mask2, frame, "Green", (0, 255, 0))
    find_centroid(mask3, frame, "Blue", (255, 0, 0))
    find_centroid(mask4, frame, "Yellow", (0, 255, 255))

    cv2.imshow('Camera', frame)
    cv2.imshow('Mask', mask_all)
    cv2.imshow('Detected color', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyWindow()
