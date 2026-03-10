from fastapi import FastAPI
from kiteconnect import KiteConnect, KiteTicker
import os
import json
import requests

app = FastAPI()

API_KEY = os.getenv("plxxli4ca3wmhteb")
ACCESS_TOKEN = os.getenv("eMM4fA2O46trtW5QCESvSZbKF5E4er6K")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

spikes = []

# Load NSE instruments
url="https://api.kite.trade/instruments"
data=requests.get(url).text.split("\n")

tokens=[]
symbols={}

for row in data[1:500]:
    r=row.split(",")

    if len(r)>10 and r[11]=="NSE":

        token=int(r[0])
        symbol=r[2]

        tokens.append(token)
        symbols[token]=symbol

price_cache={}

def on_ticks(ws,ticks):

    global spikes

    for t in ticks:

        token=t["instrument_token"]
        price=t["last_price"]

        if token in price_cache:

            old=price_cache[token]

            move=((price-old)/old)*100

            if abs(move)>0.5:

                spikes.append({
                    "symbol":symbols[token],
                    "price":price,
                    "move":round(move,2)
                })

        price_cache[token]=price

def on_connect(ws,response):

    ws.subscribe(tokens)
    ws.set_mode(ws.MODE_LTP,tokens)

kws=KiteTicker(API_KEY,ACCESS_TOKEN)

kws.on_ticks=on_ticks
kws.on_connect=on_connect

import threading
threading.Thread(target=kws.connect).start()

@app.get("/spikes")
def get_spikes():

    global spikes

    s=spikes[-20:]

    return s
