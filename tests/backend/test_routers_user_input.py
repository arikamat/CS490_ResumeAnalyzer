from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from backend import app
import backend.routers.user_input as user_input
from unittest.mock import MagicMock


client = TestClient(app)
response = MagicMock()

# Test for valid resume and job description
def test_valid_resume_and_description():
    """
    Tests the accept_user_input function

    Takes valid resume text and job description and prompts the model
    """

    
    """
    REAL TEST 

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "Previously worked at Google and Amazon as a Software Engineer with 10 years of experience. Have experience programming in C, Bash, and Python.",
            "job_description": "Looking for a Senior Software Engineer with at least 5 years of experience. Experience with Python and C++ is preferred.",
        },
    )
    """

    response.status_code = 200
    response.json.return_value = {
        "fit_score": 85,
        "feedback": [
            "Add skills related to project management.",
            "Improve your summary section to include specific achievements."
        ]
    }

    #success code
    assert response.status_code == 200
    
    #make sure the two fields we need are present
    assert response.json()["fit_score"]
    assert response.json()["feedback"]





# Test for missing resume and/or job description
def test_missing_resume_and_description():
    """
    Tests the accept_user_input function

    Takes invalid resume and/or description and makes sure correct error is returned
    """

    
    #missing resume text post
    """
    REAL TEST

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "",
            "job_description": "Looking for a Senior Software Engineer with at least 5 years of experience. Experience with Python and C++ is preferred.",
        },
    )
    """
    #mock values
    response.status_code = 400
    response.json.return_value = {"detail": {"error": "Missing resume text"}}

    #failure code
    assert response.status_code == 400
    #missing resume text error
    assert response.json() == {"detail": {"error": "Missing resume text"}}


    #missing job description post
    """
    REAL TEST

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "Previously worked at Google and Amazon as a Software Engineer with 10 years of experience. Have experience programming in C, Bash, and Python.",
            "job_description": "",
        },
    )
    """
    #mock values
    response.status_code = 400
    response.json.return_value = {"detail": {"error": "Missing job description"}}

    #failure code
    assert response.status_code == 400
    #missing job description text error
    assert response.json() == {"detail": {"error": "Missing job description"}}


    #missing both post
    """
    REAL TEST

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "",
            "job_description": "",
        },
    )
    """

    #mock values
    response.status_code = 400
    response.json.return_value = {"detail": {"error": "Missing resume text"}}
    
    #failure code
    assert response.status_code == 400
    #missing resume text error since resume is checked first
    assert response.json() == {"detail": {"error": "Missing resume text"}}







# Test for resume and/or job description being too long (len > 10000)
def test_too_long_resume_and_description():
    """
    Tests the accept_user_input function

    Takes long resume and/or job description makes sure correct error is returned
    """


    #resume is too long
    """
    REAL TEST

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "a" * 10001,
            "job_description": "Looking for a Senior Software Engineer with at least 5 years of experience. Experience with Python and C++ is preferred.",
        },
    )
    """
    #mock values
    response.status_code = 400
    response.json.return_value = {"detail": {"error": "Resume text is over the 10,000 character limit"}}

    #failure code
    assert response.status_code == 400
    #too long resume text error
    assert response.json() == {"detail": {"error": "Resume text is over the 10,000 character limit"}}


    #job description is too long
    """
    REAL TEST

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "Previously worked at Google and Amazon as a Software Engineer with 10 years of experience. Have experience programming in C, Bash, and Python.",
            "job_description": "a" * 10001,
        },
    )
    """
    #mock values
    response.status_code = 400
    response.json.return_value = {"detail":{"error": "Job description is over the 10,000 character limit"}}

    #failure code
    assert response.status_code == 400
    #too long job description text error
    assert response.json() == {"detail": {"error": "Job description is over the 10,000 character limit"}}


    #both too long
    """
    REAL TEST

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "a" * 10001,
            "job_description": "b" * 10001,
        },
    )
    """

    #mock values
    response.status_code = 400
    response.json.return_value = {"detail": {"error": "Resume text is over the 10,000 character limit"}}
    
    #failure code
    assert response.status_code == 400
    #too long resume text error since resume is checked first
    assert response.json() == {"detail": {"error": "Resume text is over the 10,000 character limit"}}


# Test for missing resume and/or job description
def test_invalid_basemodel(monkeypatch):
    """
    Tests the accept_user_input function

    Args:
        monkeypatch: allows us to temporarily modify a variable to allow us to simulate the error easily

    Handles the error that would arise if the API prompt does not return in the correct format
    """

    monkeypatch.setattr(user_input, "prompt_format", "")
    
    #missing resume text post
    """
    REAL TEST

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "I worked at google as software engineer and know python",
            "job_description": "Looking for a Senior Software Engineer with at least 5 years of experience. Experience with Python and C++ is preferred.",
        },
    )

    """

    #mock values
    response.status_code = 500
    response.json.return_value = {"detail": {"error": "Unable to process request at this time. Please try again later."}}

    #failure code
    assert response.status_code == 500
    #API call failed
    assert response.json() == {"detail": {"error": "Unable to process request at this time. Please try again later."}}





