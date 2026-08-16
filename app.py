from fastapi import FastAPI,Request,UploadFile,File,HTTPException,status
import os
from fastapi import Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles 
import filetype
import subprocess
import sys
import json
import cv2
from database import create_tables , check_in , check_out , get_all_vehicles , get_all_parking_records,get_all_stats,get_admin_search
from pydantic import BaseModel

app = FastAPI(title="Smart-Park" , version="3.0")
create_tables()
ADMIN_PASSWORD = "Admin1234"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)



# Validate Uploaded File Type

# Perform two levels of file-type validation:
#
# 1. Validate the MIME ( MIME (Multipurpose Internet Mail Extension type) Written as type/subtype)
#    type provided by the client using
#    `file.content_type`. This ensures that the uploaded file
#    claims to be one of the supported image formats.
#
# 2. Verify the actual file contents using `filetype.guess()`.
#    The MIME type supplied by the client cannot be fully trusted,
#    because a file can be renamed or its Content-Type can be
#    incorrectly specified.
#
#    `filetype.guess()` examines the binary contents of the uploaded
#    file and determines its actual file type. We then compare the
#    detected MIME type with our list of supported image formats.
#
# This prevents non-image files or incorrectly labelled files from
# being passed to the computer-vision pipeline (YOLO + PaddleOCR).
#
# HTTP 415 (Unsupported Media Type) is returned whenever the uploaded
# file is not a supported image or its actual type cannot be determined.
def validate_file_size_type(file: UploadFile):

    FILE_SIZE = 2 * 1024 * 1024  # 2 MB

    accepted_file_types = [
        "image/png",
        "image/jpeg",
        "image/jpg"
    ]

    # Checking the type is in accepted type or not
    if file.content_type not in accepted_file_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PNG and JPEG and JPG images are allowed."
        )

    # Check actual file type
    file_info = filetype.guess(file.file)

    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to determine file type."
        )

    if file_info.mime not in accepted_file_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type."
        )

    # Check file size
    file.file.seek(0)

    real_file_size = 0

    for chunk in file.file:
        real_file_size += len(chunk)

        if real_file_size > FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 2 MB."
            )

    # Reset file pointer (IMP.)
    file.file.seek(0)


# A function to detect the plate as well as dwtecting the number plate
# we are running the sub-processes for yolo and ocr 
# and using bbox.json and result.json to get the final result from yolo and ocr_engine 
async def detect_image(file_path :str):
    # Running YOLO detector 
    subprocess.run(
    [sys.executable, "detector.py", file_path],
    check=True
    )

    # Running PaddleOCR
    subprocess.run([sys.executable, "ocr_engine.py"], check=True) 

    with open("Temp/bbox.json") as f:
        bbox = json.load(f)

    with open("Temp/result.json") as f:
        result = json.load(f)

    plate = result["plate"]
    confidence = result["confidence"]

    # Declaring the cv2 image variable
    img = cv2.imread(file_path)

    # Drawing the number plate box and the number plate on cv2 image
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

    # Returning the result
    return {
        "message": "Detection completed",
        "number_plate" : plate,
        "confidence" : confidence,
        "image_url": "/output/output.jpg"
    }


@app.get("/health")
def health():
    return {"status": "ok"}

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount(
    "/output",
    StaticFiles(directory="Output-img"),
    name="output"
)
@app.get('/',response_class=HTMLResponse)
def greet(request: Request):
    return templates.TemplateResponse(
        request, 
        "index.html"
    )

@app.post('/file')
async def upload_file(file: UploadFile = File(...)):
    #validate the uploaded file
    validate_file_size_type(file)

    #created a path for uploaded image
    file_path = os.path.join(UPLOAD_DIR,file.filename)

    # Save uploaded image
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    print("Image uploaded:", file.filename)

    # Calling the detection endpoint
    result = await detect_image(file_path)
    return result



class CheckInRequest(BaseModel):
    plate_number:str

@app.post("/check-in")
def check_in_vehicle(request : CheckInRequest):
    result = check_in(request.plate_number)
    return result

class CheckOutRequest(BaseModel):
    plate_number : str 
@app.post("/check-out")
def check_out_vehicle(request : CheckOutRequest):
    result = check_out(request.plate_number)
    return result

@app.post("/admin-login")
async def admin_login(password: str = Form(...)):

    if password == ADMIN_PASSWORD:
        return {
            "success": True,
            "message": "Access granted."
        }

    return {
        "success": False,
        "message": "Incorrect password."
    }


@app.get("/admincontent",response_class=HTMLResponse)
def adminContent(request: Request):

    return templates.TemplateResponse(
        request, 
        "adminContent.html"
    )

@app.get("/vehicleData")
def get_vehicle_data():
    return [
        dict(vehicle)
        for vehicle in get_all_vehicles()
    ]

@app.get("/parkingData")
def get_parking_data():
    return [
        dict(parking)
        for parking in get_all_parking_records()
    ]

@app.get("/dashstats")
def get_stats():
    stats = get_all_stats()
    return stats

## Adding search feature route for backend
@app.post("/admin-search")
async def admin_search(plate: str = Form(...)):
    records = get_admin_search(plate)

    if not records:
        return {
            "success": False,
            "message": "No records found for this vehicle.",
            "records": []
        }

    return {
        "success": True,
        "message": "Vehicle records found.",
        "records": [
            dict(record)
            for record in records
        ]
    } 
#checkout page for checking out a vehicle
@app.get("/check-out-page",response_class=HTMLResponse)
def checkoutContent(request: Request):
    return templates.TemplateResponse( 
        request,
        "CheckOut.html",
    )