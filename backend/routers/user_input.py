from fastapi import APIRouter, status, HTTPException
from backend.schemas import UserInput
from backend.utils import prompt_nlp_model

router = APIRouter()

#put this variable outside to change it in tests
prompt_format = """

        Create a fitscore for how well the resume fits and return it in json format like 
        
            "fit_score": 85,
            "feedback": [
                "Add skills related to project management.",
                "Improve your summary section to include specific achievements."
            ]
        ",

        ONLY RETURN THE JSON AND NOTHING ELSE
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

    return response_json
