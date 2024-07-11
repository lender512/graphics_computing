import cv2
import numpy as np
from yolov5 import YOLOv5
from segment_anything import SamPredictor

def highlight_people_cars_and_bikes(
    full_path_input_image,
    color_scale_image,
    color_scale_people,
    color_scale_cars,
    color_scale_bikes,
    full_path_output_image
):
    image = cv2.imread(full_path_input_image)
    original_shape = image.shape

    image[:] = color_scale_image

    # Load YOLO model
    yolo = YOLOv5("yolov5s.pt")

    results = yolo.predict(image)
    
    classes_of_interest = ['person', 'car', 'bicycle']
    filtered_results = [res for res in results if res['class'] in classes_of_interest]

    # Load SAM model
    sam = SamPredictor("sam_vit_b.pth") 

    for result in filtered_results:
        x1, y1, x2, y2 = result['box']

        object_crop = image[y1:y2, x1:x2]
        sam.set_image(object_crop)
        masks, _ = sam.predict()
        
        if result['class'] == 'person':
            color_scale = color_scale_people
        elif result['class'] == 'car':
            color_scale = color_scale_cars
        elif result['class'] == 'bicycle':
            color_scale = color_scale_bikes

        for mask in masks:
            object_crop[mask] = color_scale

        image[y1:y2, x1:x2] = object_crop

    cv2.imwrite(full_path_output_image, image)
if __name__ == "__main__":
    highlight_people_cars_and_bikes(
        full_path_input_image='images-for-last-exercise/example-1.jpeg',
        color_scale_image=(255, 255, 255),
        color_scale_people=(255, 0, 0),
        color_scale_cars=(0, 255, 0),
        color_scale_bikes=(0, 0, 255),
        full_path_output_image='detections-example-1.jpg'
    )
