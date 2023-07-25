from pydantic import BaseModel, Extra
from fastapi import FastAPI, HTTPException
import requests

import app.ner as ner

app = FastAPI()


class Item(BaseModel):
    URL: str

    class Config:
        extra = Extra.allow  # Allow unknown keys in the JSON payload


@app.post("/fetch_text/")
async def process_json(item: Item):

    # Fetch the text from the provided URL
    response = requests.get(item.URL)
    if response.status_code != 200:
        raise HTTPException(
            status_code=400, detail="Failed to fetch text content from the URL")

    final_counts = ner.extract_names_and_counts(response.text)

    # Combine the text content and metadata fields into a response JSON object
    response = {
        "URL": item.URL,
        **item.dict(exclude={'URL'}),
        "people": final_counts
    }

    # Return the JSON response
    return response


# curl -X POST -H "Content-Type: application/json" -d '{"URL": "https://www.gutenberg.org/cache/epub/345/pg345.txt", "author": "Bram Stoker", "title": "Dracula"}' http://127.0.0.1:8^C0/fetch_text/
# curl -X POST -H "Content-Type: application/json" -d '{"URL": "https://www.guwtenberg.org/cache/epub/345/pg345.txt", "author": "Bram Stoker", "title": "Dracula"}' http://127.0.0.1:8^C0/fetch_text/
