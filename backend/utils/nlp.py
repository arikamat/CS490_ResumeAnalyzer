from dotenv import load_dotenv
import json
from groq import Groq, AuthenticationError, APIConnectionError
import os

from backend.schemas.user_input import UserInput

JOB_DESCRIPTION_PROMPT = """
Please parse the following job description and separate it into three sections: skills, experience, and education. Do not change or modify the text in any way; simply split the content as is into the appropriate categories.

Output format:
{
  "skills": "Full text of the skills section from the job description",
  "experience": "Full text of the experience section from the job description",
  "education": "Full text of the education section from the job description"
}

Return ONLY the JSON output and nothing else.

Job Description Text:

"""

RESUME_PROMPT = """
Please parse the following resume text and separate it into three sections: skills, experience, and education. Do not change or modify the text in any way; simply split the content as is into the appropriate categories.

Output format:
{
  "skills": "Full text of the skills section from the resume",
  "experience": "Full text of the experience section from the resume",
  "education": "Full text of the education section from the resume"
}

Return ONLY the JSON output and nothing else.

Resume Text:

"""

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

    # if the API key is invalid
    except AuthenticationError:
        return {"error": "API KEY is invalid"}

    # if no API key is inputted
    except APIConnectionError:
        return {"error": "No API KEY provided"}

    # if organizing the response into FitScore doesn't work
    except json.decoder.JSONDecodeError:
        return {"error": "API Response was not in the correct format"}
    
    

    return json_response


def calculate_fit_score(user_input: UserInput):
    resume_prompt = RESUME_PROMPT + user_input.resume_text
    job_prompt = JOB_DESCRIPTION_PROMPT + user_input.job_description

    resume_split_up = prompt_nlp_model(resume_prompt)
    job_split_up = prompt_nlp_model(job_prompt)

    print(resume_split_up)
    print(job_split_up)