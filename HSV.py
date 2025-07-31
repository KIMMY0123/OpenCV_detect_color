import cv2
import numpy as np

def show_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        print(f"HSV at ({x},{y}) = H:{pixel[0]} S:{pixel[1]} V:{pixel[2]}")

# โหลดภาพ หรือเปิดกล้อง
# img = cv2.imread("your_image.jpg")  # กรณีใช้ภาพนิ่ง
cap = cv2.VideoCapture(1)  # ใช้กล้อง Webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", show_hsv_value)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
