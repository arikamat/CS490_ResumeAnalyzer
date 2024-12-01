from fastapi import APIRouter, status, HTTPException
from pydantic import ValidationError
from backend.schemas import UserInput
from backend.utils import prompt_nlp_model
from backend.schemas import FitScore

router = APIRouter()

#put this variable outside to change it in tests
prompt_format = """
Generate a fit score to evaluate how well the resume matches the job description. Return the result in JSON format with the following structure:

{
    "fit_score": 85,
    "feedback": [
        "Add skills related to project management.",
        "Improve your summary section to include specific achievements."
    ]
}

Ensure the JSON output is precise and includes:
1. A numerical fit score between 0 and 100. (A percentage)
2. A list of actionable feedback points.

The feedback should only provide actionable suggestions to improve the resume. Do not include any information about how the fit score was calculated. 

Return ONLY the JSON output and nothing else.

"""

@router.post("/api/analyze")
async def accept_user_input(user_input: UserInput):
    """
    Takes the input from the front end and prompts the API

    Args:
        UserInput object: An object that holds the information inputted by the user (resume & job description)

    Returns:
        JSON: a dictionary with the information regarding the prompt and response

    """
    # if resume text field is empty
    if not user_input.resume_text:
        raise HTTPException(status_code=400, detail={"error": "Missing resume text"})

    # if job description text field is empty
    if not user_input.job_description:
        raise HTTPException(
            status_code=400, detail={"error": "Missing job description"}
        )

    # if resume input is too long
    if len(user_input.resume_text) > 10000:
        raise HTTPException(
            status_code=400,
            detail={"error": "Resume text is over the 10,000 character limit"},
        )

    # if job description is too long
    if len(user_input.job_description) > 10000:
        raise HTTPException(
            status_code=400,
            detail={"error": "Job description is over the 10,000 character limit"},
        )

    prompt = (
        f"""
        This is the resume: {user_input.resume_text}
        This is the job description: {user_input.job_description}
        """) + prompt_format    

    response_json = prompt_nlp_model(prompt)

    # if there is an error when prompting the model
    if "error" in response_json:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Unable to process request at this time. Please try again later."
            },
        )
    try:
        res = FitScore(**response_json)
    
    except ValidationError:
        return {"error": "Cannot fit API response into FitScore"}
    return res.model_dump()
