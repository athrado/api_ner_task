from pydantic import BaseModel, Extra
from fastapi import FastAPI, HTTPException
import requests

import app.ner as ner

app = FastAPI(title='NER API',
              description='''Extract name entities from given URL 
              and return people and their counts for location mentions.''')


class UserIn(BaseModel):
    URL: str

    class Config:
        extra = Extra.allow  # allow unknown keys in the JSON payload


class Reponse(BaseModel):
    URL: str
    people: list

    class Config:
        extra = Extra.allow  # allow unknown keys in the JSON payload


@app.post("/get_text_and_ents/", response_model=Reponse)
async def extract_named_entities(user_in: UserIn):
    """Process json payload containing URL to text:

    - retrieve text from URL
    - remove header/footer/tags for Gutenberg Project texts
    - find names and locations using spaCy's NER 
    - count names and mentions of locations within certain range
    - create response in desired format

    Args:
        user_in (Item): User input as payload arguments.

    Raises:
        HTTPException: In case URL cannot be found.

    Returns:
        json: Reponse containing people and location counts.
    """

    # Fetch the text from the provided URL
    response = requests.get(user_in.URL)
    if response.status_code != 200:
        raise HTTPException(
            status_code=400, detail="Failed to fetch text content from the URL")

    final_counts = ner.extract_ne_counts(response.text)

    # Combine the NE counts and metadata fields into a response JSON object
    response = {
        **user_in.dict(),
        "people": final_counts
    }

    # Return the JSON response
    return response
