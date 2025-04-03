import mysql.connector
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from starlette.middleware.cors import CORSMiddleware
import face_recognition
import urllib.request
import numpy as np
import cv2
import os
from dotenv import load_dotenv
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature


# Initialize FastAPI app
app = FastAPI()

# Load environment variables
load_dotenv()

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

@app.post("/recognize")
async def recognize(lat: str = Form(...), lon: str = Form(...), image: UploadFile = File(...)):
    try:
        # Connect to database
        db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            passwd=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT'),
        )

        if(db.is_connected() == False):
            raise HTTPException(status_code=500, detail='Database connection failed')

        # Get list of users from database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        # Get polygon locations from database
        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()

        polygons = []

        # Loop through locations
        for location in locations:
            # 0 id
            # 1 lat
            # 2 lon

            # Get polygon coordinates
            polygons.append(((float(location[1]), float(location[2]))))

        # Check if lat and lon are in any polygon
        point = Feature(geometry=Point((float(lon), float(lat))))
        polygon = Polygon([polygons])

        if(boolean_point_in_polygon(point, polygon) == False):
            raise HTTPException(status_code=403, detail='Location not allowed')

        # Load input image
        # request_image = urllib.request.urlopen(request.image)

        # Form data input image
        # Load input image
        try:
            contents = await image.read()
            nparr = np.frombuffer(contents, np.uint8)
            request_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if request_image is None:
                raise ValueError("Failed to decode image from uploaded file. Check file format.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing uploaded image: {e}")

        # Convert to RGB
        rgb_image = cv2.cvtColor(request_image, cv2.COLOR_BGR2RGB)

        result = None

        # Loop through users
        for data in results:
            # Get user name
            # 0 id
            # 1 name
            # 2 image

            # Get base image to compare
            try:
                sample_image = face_recognition.load_image_file(urllib.request.urlopen(data[2]))
                sample_image_encoded = face_recognition.face_encodings(sample_image)[0]
            except Exception as e:
                print(f"Error processing sample image for user {data[1]}: {e}")
                continue  # Skip to the next user if there's an issue with the sample image

            # Find faces
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

            # Loop through faces
            for face_encoding in face_encodings :
                # Compare faces
                results = face_recognition.compare_faces([sample_image_encoded], face_encoding)

                # Print results
                if results[0]:
                    print(f"Face found for user {data[1]}")
                    # Stop loop if face is found
                    result = {
                        'code': 200,
                        'message': 'Face found for user ' + data[1],
                    }
                    break

            # Stop loop if face is found
            if(result):
                break

        # Return result if found
        if(result):
            return result
        else:
            raise HTTPException(status_code=404, detail='Face not found')

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        # Catch other exceptions
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()
