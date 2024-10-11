from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import face_recognition
import urllib.request
import numpy as np
import cv2

app = FastAPI()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

# Add request model
class Request(BaseModel):
    user_id: str
    image: str

@app.post("/recognize")
async def recognize(request: Request):
    try:
        # Get base image to compare
        # sample_image = face_recognition.load_image_file(get from user id)
        sample_image = face_recognition.load_image_file(urllib.request.urlopen('http://localhost/sample-facerecognition/base.jpg'))
        sample_image_encoded = face_recognition.face_encodings(sample_image)[0]

        # Load input image
        request_image = urllib.request.urlopen(request.image)
        image = cv2.imdecode(np.asarray(bytearray(request_image.read()), dtype=np.uint8), -1)

        # Convert to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Find faces
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        # Loop through faces
        for face_encoding in face_encodings :
            # Compare faces
            results = face_recognition.compare_faces([sample_image_encoded], face_encoding)

            # Print results
            if results[0]:
                return {
                    'code': 200,
                    'message': 'Face found',
                }
            else:
                raise HTTPException(status_code=404, detail='Face not found')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
