# Importing all the neccary file
import json
import subprocess
import cv2
import sys

# Declaring the Image Path
IMAGE_PATH = "Test-Images/t3.png"

# Run detector.py as a separate process to avoid runtime conflicts
# between YOLO (PyTorch) and PaddleOCR (PaddlePaddle).
# Run YOLO Detection
# detector.py
# Running a Subprocess 
subprocess.run(
    [sys.executable, "detector.py", IMAGE_PATH],
    check=True
)


# Run Paddle OCR
# ocr_engine.py
subprocess.run(["python", "ocr_engine.py"], check=True)


# Read Results
# Given by detector.py and ocr_engine.py
with open("Temp/bbox.json") as f:
    bbox = json.load(f)

with open("Temp/result.json") as f:
    result = json.load(f)

plate = result["plate"]
confidence = result["confidence"]

# Declaring the cv2 image variable
img = cv2.imread(IMAGE_PATH)

x1 = bbox["x1"]
y1 = bbox["y1"]
x2 = bbox["x2"]
y2 = bbox["y2"]

# Making The Box Boundary around number plate
cv2.rectangle(
    img,
    (x1, y1),
    (x2, y2),
    (0, 0, 255),
    2
)

# Putting the text  around number plate boundary
cv2.putText(
    img,
    plate,
    (x1, y1 - 10),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.5,
    (0, 0, 255),
    5
)

# Savin the final output iage with bbox and text as .jpg
cv2.imwrite("Output-img/output.jpg", img)

# Printing out each and every information related to the number plate
print("Number Plate :", plate)
print("Confidence   :", confidence)
print("Output saved to Output-img/output.jpg")