from dotenv import load_dotenv
import json
from groq import Groq, AuthenticationError, APIConnectionError
import os


def prompt_nlp_model(prompt, api_inputted_key): 
    """
    Prompts the API and with information

    Args:
        str: A question or command for the model to fulfill

    Returns:
        JSON: a dictionary with the information regarding the prompt and response
    """

    #create an instance of groq with our API key
    client = Groq(api_key= api_inputted_key,)
    
    try:
        #API call
        api_prompt = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",

        )

    #if the API key is invalid
    except AuthenticationError:
        return "API KEY IS INVALID"

    #if no API key is inputted
    except APIConnectionError:
        return "NO API KEY PROVIDED"

    #return the information into a json format
    return json.loads(api_prompt.model_dump_json(indent=2))

