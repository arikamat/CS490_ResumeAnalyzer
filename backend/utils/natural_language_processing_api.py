from dotenv import load_dotenv
import json
from groq import Groq, AuthenticationError, APIConnectionError
import os
from backend.schemas import FitScore


def prompt_nlp_model(prompt):
    """
    Prompts the API and with information

    Args:
        str: A question or command for the model to fulfill

    Returns:
        JSON: a dictionary with the information regarding the prompt and response
    """

    # create an instance of groq with our API key
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )

    try:
        # API call
        api_prompt = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        # return the information into a json format
        text = api_prompt.choices[0].message.content
        json_response = json.loads(text)
        res = FitScore(**json_response)

    # if the API key is invalid
    except AuthenticationError:
        return {"error": "API KEY is invalid"}

    # if no API key is inputted
    except APIConnectionError:
        return {"error": "No API KEY provided"}

    # if organizing the response into FitScore doesn't work
    except json.decoder.JSONDecodeError:
        return {"error": "API Response was not in the correct format"}

    return res
