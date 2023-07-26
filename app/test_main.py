from fastapi.testclient import TestClient
from pydantic import BaseModel, Extra

import pytest

from app.main import app
from app.config import correct_response_people


class Item(BaseModel):
    URL: str

    class Config:
        extra = Extra.allow  # Allow unknown keys in the JSON payload


# TestClient for FastAPI app
client = TestClient(app)


def test_fetch_text_success_gutenberg():
    """Test: Provide a sample Gutenberg URL."""

    test_url = "https://www.gutenberg.org/cache/epub/64317/pg64317.txt"
    response = client.post(
        "/get_text/", json={"URL": test_url, "author": "John Doe", })

    assert response.status_code == 200
    assert response.json()["URL"] == test_url
    assert response.json()["author"] == "John Doe"


def test_fetch_toy_example():
    """Test: Provide a sample URL for toy example that returns a known text content."""

    test_url = "https://raw.githubusercontent.com/athrado/api_task/main/sample_text.txt"

    response = client.post(
        "/get_text/", json={"URL": test_url, "author": "ChatGPT", "title": "Travel Stories"})
    assert response.json()['title'] == 'Travel Stories'
    assert response.json()['people'] == correct_response_people


def test_fetch_text_failed():
    """Test: Provide a sample URL that returns an error (404, for example)"""

    test_url = "https://example.com/non_existent_page"
    response = client.post("/get_text/", json={"URL": test_url})

    assert response.status_code == 400
    assert "Failed to fetch text content from the URL" in response.json()[
        "detail"]


if __name__ == "__main__":
    pytest.main(["-v", __file__])
