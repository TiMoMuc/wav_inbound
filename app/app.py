import os
import sqlite3
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi import status, HTTPException
import uvicorn
import time
import aiofiles

app = FastAPI()


# API Key Authentication
API_KEY = os.getenv("API_KEY", "123456789") #if the API_KEY is not set, use the default value
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return api_key


# Database file path
db_file = "/data/database.db"

# Check if SQLite database file exists
if not os.path.exists(db_file):
    # Create a new SQLite database if it doesn't exist
    print("Database file not found. Creating a new database file.")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE soundfiles
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, audio_data BLOB)''')
    conn.commit()
    conn.close()
    print("Database file created successfully.")


# Route to check if the server is running
@app.get("/")
async def read_root():
    print("Root path accessed. Server is running.")
    return {"status": "success", "message": "Server is running"}

# Route to upload audio data
@app.post("/uploadAudio")
async def upload_audio(request: Request, api_key: str = Depends(get_api_key)):
    try:
        # Get the raw body content
        body = await request.body()
        print("Audio data received successfully.")

        # Function to generate a timestamp, if needed.
        # timestamp = int(time.time())

        # Function to save the file to local storage
        """ filename = f"/data/recording_{timestamp}.wav"
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(body)
         """

        # Store the audio data in the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO soundfiles (audio_data) VALUES (?)", (body,))
        conn.commit()
        conn.close()
        print("Audio data saved successfully.")

        return JSONResponse(
            content={
                "status": "success",
                "message": ".wav successfully received"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)