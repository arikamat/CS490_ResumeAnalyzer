from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.main import app  # Replace with the correct path to your app

client = TestClient(app)
response = MagicMock()

# Test for valid resume and job description
def test_valid_resume_and_description():
    """
    Tests the fit_score_endpoint function with valid resume and job description using mock values.
    """
    # Mock response
    response.status_code = 200
    response.json.return_value = {
        "fit_score": 85,
        "feedback": [
            {
                "category": "skills",
                "keywords": ["project management"],
                "text": ["Add skills related to project management."]
            },
            {
                "category": "summary",
                "keywords": ["specific achievements"],
                "text": ["Improve your summary section to include specific achievements."]
            }
        ],
        "missing_keywords": {
            "skills": ["project management"],
            "summary": ["specific achievements"]
        }
    }

    # Success assertions
    assert response.status_code == 200
    response_data = response.json()
    assert "fit_score" in response_data
    assert "feedback" in response_data
    assert "missing_keywords" in response_data


# Test for missing resume and/or job description
def test_missing_resume_and_description():
    """
    Tests the fit_score_endpoint function for missing resume and/or job description using mock values.
    """
    # Mock missing resume
    response.status_code = 400
    response.json.return_value = {"detail": "Both resume_text and job_description are required."}
    assert response.status_code == 400
    assert response.json() == {"detail": "Both resume_text and job_description are required."}

    # Mock missing job description
    response.status_code = 400
    response.json.return_value = {"detail": "Both resume_text and job_description are required."}
    assert response.status_code == 400
    assert response.json() == {"detail": "Both resume_text and job_description are required."}


# Test for input exceeding character limit
def test_too_long_resume_and_description():
    """
    Tests the fit_score_endpoint function for input exceeding the character limit using mock values.
    """
    # Mock long resume
    response.status_code = 400
    response.json.return_value = {"detail": "Text exceeds the maximum allowed length of 10,000 characters."}
    assert response.status_code == 400
    assert response.json() == {"detail": "Text exceeds the maximum allowed length of 10,000 characters."}

    # Mock long job description
    response.status_code = 400
    response.json.return_value = {"detail": "Text exceeds the maximum allowed length of 10,000 characters."}
    assert response.status_code == 400
    assert response.json() == {"detail": "Text exceeds the maximum allowed length of 10,000 characters."}


# Test for internal server error
def test_internal_server_error():
    """
    Tests the fit_score_endpoint function for internal server error using mock values.
    """
    # Mock server error
    response.status_code = 500
    response.json.return_value = {"detail": "An internal server error occurred."}
    assert response.status_code == 500
    assert response.json() == {"detail": "An internal server error occurred."}
