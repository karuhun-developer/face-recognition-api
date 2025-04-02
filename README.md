## Installation without Docker

1. Clone this Repo

   `git clone https://github.com/karuhun-developer/face-recognition-api.git`

2. Cd into the face-recognition-api folder

   `cd face-recognition-api`

3. Create a virtual environment

   `python -m venv venv`

4. Activate virtualenv

   `source venv/bin/activate`

5. Cd into the src folder

   `cd src`

6. Install the required packages

   `python -m pip install -r requirements.txt`

7. Start the app

   ```shell
    python main.py
   ```

   7b. Start the app using Uvicorn

   ```shell
    uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8002
   ```

8. App run on port 8002.

## Installation with Docker

1. Clone this Repo

   `git clone https://github.com/karuhun-developer/face-recognition-api.git`

2. Cd into the face-recognition-api folder

   `cd face-recognition-api`

3. Use Docker-Compose to spin up containers

   `docker-compose up -d --build`

4. App run on port 8002.

## If Face Recognition model error

```bash
pip install wheel setuptools pip --upgrade
pip install git+https://github.com/ageitgey/face_recognition_models --verbose
```
