import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture("plane.mp4")
model = YOLO("yolov8n.pt")

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패!")
        exit()
        
    results = model(frame)
    frame = results[0].plot()
        
    cv2.imshow("planeVideo", frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

