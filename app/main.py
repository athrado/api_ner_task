from pydantic import BaseModel, Extra
from fastapi import FastAPI, HTTPException
import requests

import app.ner as ner

# Create instance
app = FastAPI(title='NER API',
              description='''Extract name entities from given URL 
              and return people and their counts for location mentions.''')

class UserIn(BaseModel): 
# Data model for request body

    URL: str

    class Config:
        extra = Extra.allow  # allow unknown keys

class Reponse(BaseModel): 
# Data model for response body

    URL: str
    people: list

    class Config:
        extra = Extra.allow  # allow unknown keys


@app.post("/get_text_and_ents/", response_model=Reponse) 
async def extract_named_entities(user_in: UserIn, 
                                 merge_appos: bool = False): # path operation function, executed whenever request to path with POST
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

    final_counts = ner.extract_ne_counts(response.text, merge_appositions=merge_appos)

    # Combine the NE counts and metadata fields into a response JSON object
    response_body = {
        **user_in.dict(),
        "people": final_counts
    }

    # Return the JSON response
    return response_body
