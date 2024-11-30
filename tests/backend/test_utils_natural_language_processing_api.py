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

    response_json = prompt_nlp_model("Hi",os.getenv("GROQ_API_KEY"))
    
    #test that a json is returned
    assert type(response_json) == dict;
    #test that there is a response and the response is not empty
    assert response_json['choices'][0]['message']['content']


def test_invalid_api_key():
    """
    Tests the prompt_npl_model function

    Makes sure that nothing happens if the API key is invalid
    """

    response_json = prompt_nlp_model("Hi","invalid_API_key")
    

    #if API key is invalid
    assert response_json == "API KEY IS INVALID"
    

def test_missing_api_key():
    """
    Tests the prompt_npl_model function

    Makes sure that nothing happens if there is no API key
    """

    response_json = prompt_nlp_model("Hi","")
    

    #if no API key provided
    assert response_json == "NO API KEY PROVIDED"

    



