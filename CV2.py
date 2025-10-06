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

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("⚠️❗cann't connected the camera❌")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Unable to read images from camera")
        break

#if you want to improve the quality of the image to make the color more accurate, 
# you can add the + function in front of it again such as + cv2.inRange(hsv, lower_red2, upper_red2) etc.

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 94, 169])
    upper_red1 = np.array([11, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
# -----------------------------------------------
    lower_grean1 = np.array([42, 94, 150])
    upper_grean1 = np.array([79, 255, 255])

    mask2 = cv2.inRange(hsv, lower_grean1, upper_grean1)
# -----------------------------------------------
    lower_blue1 = np.array([92, 161, 173])
    upper_blue1 = np.array([179, 255, 255])
    
    mask3 = cv2.inRange(hsv, lower_blue1, upper_blue1)
# -----------------------------------------------
    lower_yellow1 = np.array([18, 30, 195])
    upper_yellow1 = np.array([63, 139, 255])

    mask4 = cv2.inRange(hsv, lower_yellow1, upper_yellow1)
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
