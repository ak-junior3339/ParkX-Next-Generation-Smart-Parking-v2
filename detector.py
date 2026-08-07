# Importing Neccary Dependencies
import os
import json
import cv2
from ultralytics import YOLO
import sys

# Intializing Dir. Path
MODEL_PATH = "Models/best.pt"
TEMP_DIR = "Temp"

# Making Directory if not exsists
os.makedirs(TEMP_DIR, exist_ok=True)

# Intialializing YOLO model
model = YOLO(MODEL_PATH)

# function to detect a number plate which takes the image path as parameter
def detect_number_plate(image_path):

    # Intializing the image 
    img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError("Image not found.")

    # Predicting the Plate using thr model
    results = model.predict(img, verbose=False)

    if len(results[0].boxes) == 0:
        print("No number plate detected.")
        return
    # extracting the box from results which has co-ordinates
    box = results[0].boxes[0]

    # extracting the coordinates and mapping it to integer
    x1, y1, x2, y2 = map(int, box.xyxy[0])

    # cropping the image to only the number plate
    crop = img[y1:y2, x1:x2]

    # Saving the cropped plate in Temp/plate.jpg
    cv2.imwrite(f"{TEMP_DIR}/plate.jpg", crop)

    # Saving the coordinates as json format so that it can be used by main.py
    with open(f"{TEMP_DIR}/bbox.json", "w") as f:
        json.dump(
            {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
            },
            f,
            indent=4
        )

    # Message Confirming prediction is complete
    print("Detection Complete")


if __name__ == "__main__":
    # at the start of program function is called with image path called by main.py
    detect_number_plate(sys.argv[1])