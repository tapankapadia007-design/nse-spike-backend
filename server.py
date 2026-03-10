from fastapi import FastAPI
import random

app = FastAPI()

# demo data (later will connect Zerodha)
stocks = [
"RELIANCE","TCS","INFY","SBIN",
"HDFCBANK","ICICIBANK","ITC"
]

@app.get("/spikes")
def spikes():

    data=[]

    for s in stocks:

        move=round(random.uniform(-2,2),2)

        data.append({
        "symbol":s,
        "price":round(random.uniform(500,3000),2),
        "move":move,
        "timeframe":"30s"
        })

    return data