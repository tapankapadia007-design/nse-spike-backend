from fastapi import FastAPI
from kiteconnect import KiteConnect, KiteTicker
import os

app = FastAPI()

API_KEY = os.getenv("plxxli4ca3wmhteb")
ACCESS_TOKEN = os.getenv("eMM4fA2O46trtW5QCESvSZbKF5E4er6K")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

@app.get("/")
def home():
    return {"status":"running"}
