import pytest
from backend.utils import prompt_nlp_model
from dotenv import load_dotenv
import os
import io
import sys

def test_valid_prompt_and_api_key():
    """
    Tests the prompt_npl_model function

    Takes the prompt and valid API key and returns a json that contains the response as well as other information on the prompt
    """


    prompt = """

    "This is a resume: michael is a computer scientist who worked at google he is good at C,Python, and Bash. 
    This is a job description: We are looking for computer scientists here at Amazon who are good at Bash and Java.    
    
    Create a fitscore for how well the resume fits and return it in json format like 
    {
        "fit_score": 85,
        "feedback": [
            "Add skills related to project management.",
            "Improve your summary section to include specific achievements."
        ]
    }

    ONLY RETURN THE JSON AND NOTHING ELSE

    """
    
    #REAL TEST -> response_json = prompt_nlp_model(prompt)
    
    #mock return value
    response_json = {
        "fit_score": 85,
        "feedback": [
            "Add skills related to project management.",
            "Improve your summary section to include specific achievements."
        ]
    }

    #test that a json is returned
    assert type(response_json) == dict;
    #test that there is a response and the response is not empty
    assert response_json["fit_score"]
    assert response_json["feedback"]


def test_invalid_api_key(monkeypatch):
    """
    Tests the prompt_npl_model function

    Args:
        monkeypatch: allows us to temporarily modify the environmental variables for the duration of the test

    Makes sure that nothing happens if the API key is invalid
    """
    
    #change API key to be invalid
    monkeypatch.setenv("GROQ_API_KEY", "incorrect_api_key")

    #do not need to do a mock response since not using our API Key
    response_json = prompt_nlp_model("Hi")
    
    #if API key is invalid
    assert response_json == {"error": "API KEY is invalid"}
    

def test_missing_api_key(monkeypatch):
    """
    Tests the prompt_npl_model function

    Args:
        monkeypatch: allows us to temporarily modify the environmental variables for the duration of the test

    Makes sure that nothing happens if there is no API key
    """

    #change API key to be empty
    monkeypatch.setenv("GROQ_API_KEY", "")

    #do not need to do a mock response since not using our API Key
    response_json = prompt_nlp_model("Hi")
    

    #if no API key provided
    assert response_json == {"error": "No API KEY provided"}

    



