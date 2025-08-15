# main.py
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def read_health():
    return {"The server is healthy!!!"}

# MongoDB configuration
MONGODB_URI = "mongodb+srv://DatabaseUser:mora2000@cluster0.2g59arm.mongodb.net/"  # Replace with your MongoDB URI
DB_NAME = "Sentinal"              # Your database name

# Connect to MongoDB
try:
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    print("Successfully connected to MongoDB!")
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")

@app.get("/test-connection")
async def test_connection():
    try:
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        return {"status": "success", "message": "MongoDB connection is active"}
    except ConnectionFailure:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "MongoDB connection failed"}
        )

# Example collection usage
@app.get("/users/count")
async def count_users():
    users_collection = db["users"]
    count = users_collection.count_documents({})
    return {"user_count": count}