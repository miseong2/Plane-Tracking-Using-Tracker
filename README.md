# ✈️ Plane Tracking with YOLOv8 + OpenCV

이 프로젝트는 YOLOv8을 사용해 영상 속 비행기를 탐지하고, OpenCV 추적기로 객체를 추적하며 화면 중앙과의 위치 차이를 바탕으로 제어 방향을 출력합니다.

---

## 🧰 Requirements

```bash
pip install ultralytics opencv-python opencv-contrib-python
```

> ⚠️ `opencv-contrib-python`은 CSRT 추적기를 사용하기 위해 필요합니다.

---

## ▶️ How to Run

```bash
python plane_tracking.py
```

> 실행 전 `plane.mp4`와 `yolov8n.pt` 파일이 같은 디렉토리에 있어야 합니다.

---

## 📁 Files

* `track.py`: 메인 실행 파일
* `videoTest.py`: 영상 출력 확인용 파일
* `plane.mp4`: 테스트용 영상 파일
* `yolov8n.pt`: 사전 학습된 YOLOv8n 모델 (Ultralytics에서 다운로드 가능)

---

## ⚙️ 기능 설명

1. YOLOv8로 'airplane' 클래스 탐지
2. 탐지되면 CSRT 추적기 생성 및 초기화
3. 프레임마다 추적 결과를 바탕으로 객체 중앙 좌표 계산
4. 화면 중앙과의 차이를 기반으로 제어 방향 출력
5. 객체가 사라지면 탐지 모드로 복귀

---

## 📝 동작 흐름

* `SEARCHING...` : 비행기 탐지 중
* `Tracking` : 객체를 추적 중이며, 위치 기반 제어 방향 출력
* `ON TARGET` : 객체가 화면 중앙 근처에 위치
* `TARGET LOST` : 추적 실패. 다시 탐지 모드로 전환

---

## ❗ Notes

* `cv2.TrackerCSRT_create()`는 `opencv-contrib-python` 설치 시 제공됩니다.
* 영상이 없거나 프레임 읽기에 실패하면 자동 종료됩니다.
* `q` 키를 누르면 프로그램이 종료됩니다.
