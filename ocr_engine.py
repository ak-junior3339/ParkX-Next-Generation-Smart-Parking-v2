# Importing dependencies 
import json
from paddleocr import PaddleOCR
import re 

# Creating the object of PaddleOCR
ocr = PaddleOCR(lang="en")
STATE_CODES = {
    "AP", "AR", "AS", "BR", "CG", "CH", "DD", "DL",
    "GA", "GJ", "HR", "HP", "JH", "JK", "KA", "KL",
    "LA", "LD", "MH", "ML", "MN", "MP", "MZ", "NL",
    "OD", "PB", "PY", "RJ", "SK", "TN", "TR", "TS",
    "UK", "UP", "WB"
}
# function to read plate contents
def read_plate():

    # predecting the text
    result = ocr.predict("Temp/plate.jpg")

    if len(result[0]["rec_texts"]) == 0:
        raise Exception("OCR could not detect text.")

    # Extracting the plate from result output 
    plate = result[0]["rec_texts"][0]
    # Extracting the confidence from result output 
    confidence = result[0]["rec_scores"][0]
    plate = plate.upper().strip()
    plate = re.sub(r'[\s\-:.]+', '', plate)
    plate = re.sub(r'^(?:IND|IN|I)', '', plate)
    pattern = r'^[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{4}$'
    if (re.match(pattern, plate) and plate[:2] in STATE_CODES):
        pass
    else:
        plate = "Cannot detect or Invalid"
        confidence = 0.0
    # Storing the output in json format so that main can refer to it 
    with open("Temp/result.json", "w") as f:
        json.dump(
            {
                "plate": plate,
                "confidence": confidence
            },
            f,
            indent=4
        )

    # Conformation that OCR is completed
    print("OCR Complete")


if __name__ == "__main__":
    # call the function read_template() from the program start
    read_plate()