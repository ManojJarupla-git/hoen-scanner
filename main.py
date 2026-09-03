import json
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Data models replacing Java Search and SearchResult classes
class Search(BaseModel):
    city: str

class SearchResult(BaseModel):
    city: str
    title: str
    kind: Optional[str] = "unknown"

search_results: List[SearchResult] = []

# Reads rental_cars.json and hotels.json on startup
@app.on_event("startup")
def load_data():
    global search_results
    combined_data = []

    # Update these paths if your JSON files are inside a subfolder (e.g., Path("resources/rental_cars.json"))
    car_file = Path("src/main/resources/rental_cars.json")
    hotel_file = Path("src/main/resources/hotels.json")

    if car_file.exists():
        with open(car_file, "r", encoding="utf-8") as f:
            combined_data.extend(json.load(f))

    if hotel_file.exists():
        with open(hotel_file, "r", encoding="utf-8") as f:
            combined_data.extend(json.load(f))

    search_results = [SearchResult(**item) for item in combined_data]

# REST API endpoint replacing SearchResource.java
@app.post("/search", response_model=List[SearchResult])
def search(payload: Search):
    # Filters search results by city name (case-insensitive)
    return [
        item for item in search_results 
        if item.city.lower() == payload.city.lower()
    ]