import cv2
from ultralytics import YOLO

cap = cv2.VideoCapture("plane.mp4")
model = YOLO("yolov8n.pt")

TARGET_CLASS = "airplane"
#추적 상태 변수
isTracking = False
#추적기
Tracker = None

# 창 설정 추가
cv2.namedWindow('plane tracking', cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 읽기 실패!")
        exit()
        
    #화면 중앙 좌표 계산
    frame_height, frame_width = frame.shape[:2]
    frame_x_center = frame_width//2
    frame_y_center = frame_height//2
    cv2.circle(frame, (frame_x_center, frame_y_center), 5, (0,0,255), -1)
    command = ""
        
    if isTracking:
        success, bbox = Tracker.update(frame)
        if success:
            (x, y, w, h) = (int(v) for v in bbox)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "Tracking", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            
            #객체 좌표, 중앙과의 차이 계산
            obj_x_center = (x+w)-(w//2)
            obj_y_center = (y+h)-(h//2)
            error_x = obj_x_center - frame_x_center #양수면 객체가 오른쪽에 있음
            error_y = obj_y_center - frame_y_center #양수면 객체가 아래쪽에 있음
            cv2.circle(frame, (obj_x_center, obj_y_center), 5, (255,0,0), -1)
            deadzone = 50
            
            #제어 방향 판단
            if error_x > deadzone:
                command += "RIGHT"
            elif error_x < -deadzone:
                command += "LEFT"
            if error_y > deadzone:
                command += "DOWN"
            elif error_y < -deadzone:
                command += "UP"
                
            if command == "":
                command = "ON TARGET"
            
        else:
            isTracking = False
            Tracker = None
            command = "TARGET LOST"
            
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
        command = "SEARCHING..."
    
    cv2.putText(frame, command, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
    cv2.imshow('plane tracking', frame)
    if cv2.waitKey(10)&0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

