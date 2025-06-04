from fastapi import FastAPI, Request
from scraper import get_valorant_stats
import asyncio

app = FastAPI()

@app.get("/stats")
async def stats(username: str = ""):
    if not username:
        return {"error": "Missing username"}
    data = await get_valorant_stats(username)
    return data
