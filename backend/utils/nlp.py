from dotenv import load_dotenv
import json
import os
import google.generativeai as genai


def prompt_nlp_model(prompt):
    """
    Prompts the API and returns information

    Args:
        prompt (str): A question or command for the model to fulfill

    Returns:
        JSON: A dictionary with the information regarding the prompt and response
    """
    # Load environment variables
    load_dotenv()

    # Create an instance of Gemini with our API key
    genai.configure(api_key=os.getenv("GEMINI_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        api_prompt = model.generate_content(prompt)

        # Extract the response text
        text = api_prompt.text
        text = text.replace("```json", "").replace("```", "").replace("\n", "")
        # Attempt to parse the response as JSON
        json_response = json.loads(text)
    except:
        return {"error": "AI API Error"}

    return json_response
