import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture("plane.mp4")
model = YOLO("yolov8n.pt")

TARGET_CLASS = "airplane"
#추적 상태 변수
isTracking = False
#추적기
Tracker = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패!")
        exit()
        
    if isTracking:
        success, bbox = Tracker.update(frame)
        if success:
            (x, y, w, h) = (int(v) for v in bbox)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "Tracking", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        else:
            isTracking = False
            Tracker = None
            
    else:
        results = model(frame)
        for r in results:
            for box in r.boxes:
                class_name = model.names[int(box.cls)]
                if TARGET_CLASS == class_name and box.conf>0.6:
                    
                    x1, y1, x2, y2 = box.xyxy[0]
                    bbox = (int(x1), int(y1), int(x2-x1), int(y2-y1))
                    
                    Tracker = cv2.TrackerCSRT_create()
                    Tracker.init(frame, bbox)
                    isTracking = True
                    break
            if isTracking:
                break
    
    cv2.imshow('plane tracking', frame)
    if cv2.waitKey(10)&0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

