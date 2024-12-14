from fastapi import APIRouter, Request, status, HTTPException
from pydantic import ValidationError
from backend.schemas import UserInput
from backend.utils import prompt_nlp_model
from backend.schemas import FitScore
from backend.utils import calculate_fit_score
from backend.utils import get_jwt_token
from backend.db import resume_jobdescrip_db
from backend.utils.resume_feedback import generate_feedback

router = APIRouter()

# put this variable outside to change it in tests
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
async def accept_user_input(request : Request):
    """
    Takes the input from the front end and prompts the API

    Args:
        UserInput object: An object that holds the information inputted by the user (resume & job description)

    Returns:
        JSON: a dictionary with the information regarding the prompt and response

    """
    print(request.headers)
    jwt = get_jwt_token(request)
    if not jwt:
        print("jwt error")
        raise HTTPException(status_code=405, detail={"error": "invalid jwt"})
    
    userinput = resume_jobdescrip_db[jwt]

    user_input = UserInput(**userinput)
    # if resume text field is empty
    if not user_input.resume_text:
        print("empty resume text field error")
        raise HTTPException(status_code=400, detail={"error": "Missing resume text"})

    # if job description text field is empty
    if not user_input.job_description:
        print("empty job desc text field error")
        raise HTTPException(
            status_code=400, detail={"error": "Missing job description"}
        )

    # if resume input is too long
    if len(user_input.resume_text) > 10000:
        print("resume input long error")
        raise HTTPException(
            status_code=400,
            detail={"error": "Resume text is over the 10,000 character limit"},
        )

    # if job description is too long
    if len(user_input.job_description) > 10000:
        print("job desc too long")
        raise HTTPException(
            status_code=400,
            detail={"error": "Job description is over the 10,000 character limit"},
        )

    prompt = (
        (
            f"""
        This is the resume: {user_input.resume_text}
        This is the job description: {user_input.job_description}
        """
        )
        + prompt_format
    )

    response_json = prompt_nlp_model(prompt)

    # if there is an error when prompting the model
    if "error" in response_json:
        print("error in promopting model")
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
    
    
    ai_score = response_json["fit_score"]
    score, missing, matched = calculate_fit_score(user_input)
    feedback = generate_feedback(user_input)
    
    response_json["fit_score"] = (ai_score + score*100)/2
    response_json["missing_keywords"] = missing.model_dump()
    response_json["matched_keywords"] = matched.model_dump()
    response_json["feedback"] = feedback
    return response_json
