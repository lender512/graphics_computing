import cv2
import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression
from utils.torch_utils import select_device
import time

def count_people_cars_and_bikes(full_path_input_video):
    # Load YOLOv7 model
    device = select_device('gpu')
    model = attempt_load('yolov7.pt', map_location=device)
    
    # Open video file
    cap = cv2.VideoCapture(full_path_input_video)
    
    # Initialize counters
    people_count = 0
    bike_count = 0
    car_count = 0
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate number of frames to skip to process 5 frames per second
    frame_skip = max(int(fps / 5), 1)
    
    start_time = time.time()
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Process only every nth frame
        if frame_count % frame_skip != 0:
            continue
        
        # Preprocess frame
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).to(device).float() / 255.0
        img = img.permute(2, 0, 1).unsqueeze(0)
        
        # Run inference
        pred = model(img)[0]
        pred = non_max_suppression(pred, 0.25, 0.45, classes=[0, 1, 2])  # person, bicycle, car
        
        # Process detections
        for det in pred[0]:
            cls = int(det[5])
            if cls == 0:  # person
                people_count += 1
            elif cls == 1:  # bicycle
                bike_count += 1
            elif cls == 2:  # car
                car_count += 1
        
        # Check time constraint
        if time.time() - start_time > 300:  # 5 minutes
            print("Time limit exceeded. Stopping early.")
            break
    
    cap.release()
    
    return [people_count, bike_count, car_count]

if __name__ == "__main__":
    result = count_people_cars_and_bikes('video-for-yolo/videoplayback.mp4')
    print(f"People detected: {result[0]}")
    print(f"Bikes detected: {result[1]}")
    print(f"Cars detected: {result[2]}")