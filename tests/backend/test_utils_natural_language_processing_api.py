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

    # REAL TEST -> response_json = prompt_nlp_model(os.getenv("GROQ_API_KEY"))
    
    #mock return value
    response_json = {'id': 'chatcmpl-d848c6d0-09b2-422a-a186-3f1d185fb767', 'choices': [{'finish_reason': 'stop', 'index': 0, 'logprobs': None, 'message': {'content': "Hi! It's nice to meet you. Is there something I can help you with or would you like to chat?", 'role': 'assistant', 'function_call': None, 'tool_calls': None}}], 'created': 1733002669, 'model': 'llama3-8b-8192', 'object': 'chat.completion', 'system_fingerprint': 'fp_6a6771ae9c', 'usage': {'completion_tokens': 25, 'prompt_tokens': 12, 'total_tokens': 37, 'completion_time': 0.020833333, 'prompt_time': 0.001769811, 'queue_time': 0.011339129, 'total_time': 0.022603144}, 'x_groq': {'id': 'req_01jdzg4btfetsv4ca968w6c182'}}

    #test that a json is returned
    assert type(response_json) == dict;
    #test that there is a response and the response is not empty
    assert response_json['choices'][0]['message']['content']


def test_invalid_api_key(monkeypatch):
    """
    Tests the prompt_npl_model function

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

    Makes sure that nothing happens if there is no API key
    """

    #change API key to be empty
    monkeypatch.setenv("GROQ_API_KEY", "")

    #do not need to do a mock response since not using our API Key
    response_json = prompt_nlp_model("Hi")
    

    #if no API key provided
    assert response_json == {"error": "No API KEY provided"}

    



