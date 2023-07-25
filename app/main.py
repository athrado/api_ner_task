from pydantic import BaseModel, Extra
from fastapi import FastAPI, HTTPException
import requests

import app.ner as ner

app = FastAPI()


class Item(BaseModel):
    URL: str

    class Config:
        extra = Extra.allow  # allow unknown keys in the JSON payload


@app.post("/fetch_text/")
async def process_json(item: Item):
    """Processing json paylaod for loading text.

    Args:
        item (Item): Arguments

    Raises:
        HTTPException: In case URL cannot be found.

    Returns:
        dict: Reponse containing people and location counts.
    """

    # Fetch the text from the provided URL
    response = requests.get(item.URL)
    if response.status_code != 200:
        raise HTTPException(
            status_code=400, detail="Failed to fetch text content from the URL")

    final_counts = ner.extract_ne_counts(response.text)

    # Combine the text content and metadata fields into a response JSON object
    response = {
        "URL": item.URL,
        **item.dict(exclude={'URL'}),
        "people": final_counts
    }

    # Return the JSON response
    return response
