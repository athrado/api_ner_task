from fastapi.testclient import TestClient
from pydantic import BaseModel, Extra

import pytest

from .main import app


class Item(BaseModel):
    URL: str

    class Config:
        extra = Extra.allow  # Allow unknown keys in the JSON payload


# TestClient for FastAPI app
client = TestClient(app)


def test_fetch_text_success():
    # Provide a sample URL that returns a known text content
    test_url = "https://www.gutenberg.org/cache/epub/2447/pg2447.txt"
    response = client.post(
        "/fetch_text/", json={"URL": test_url, "author": "John Doe", })

    assert response.status_code == 200
    assert response.json()["URL"] == test_url
    assert response.json()["author"] == "John Doe"
   # assert "people" in response.json()


def test_fetch_text_failed():
    # Provide a sample URL that returns an error (404, for example)
    test_url = "https://example.com/non_existent_page"
    response = client.post("/fetch_text/", json={"URL": test_url})

    assert response.status_code == 400
    assert "Failed to fetch text content from the URL" in response.json()[
        "detail"]


if __name__ == "__main__":
    # You can run the tests using pytest or any other testing framework you prefer

    pytest.main(["-v", __file__])
