from fastapi import APIRouter, HTTPException
from backend.schemas.user_input import UserInput
from backend.utils.resume_feedback import generate_feedback
from backend.utils.fit_score import calculate_fit_score

router = APIRouter()

@router.post("/fit-score")
async def fit_score_endpoint(data: UserInput):
    """
    API endpoint to calculate fit score and generate feedback for resumes.

    Args:
        data (UserInput): Contains resume text and job description.

    Returns:
        dict: Fit score, feedback, and missing keywords.
    """
    try:
        # Step 1: Validate input
        resume_text = data.resume_text.strip()
        job_description = data.job_description.strip()

        if not resume_text or not job_description:
            raise HTTPException(status_code=400, detail="Both resume_text and job_description are required.")
        if len(resume_text) > 10000 or len(job_description) > 10000:
            raise HTTPException(status_code=400, detail="Text exceeds the maximum allowed length of 10,000 characters.")

        # Step 2: Calculate fit score and missing keywords
        fit_score, missing_schema = calculate_fit_score(data)

        # Step 3: Generate feedback for missing keywords
        feedback_data = generate_feedback(data)

        # Step 4: Format the response
        response = {
            "fit_score": fit_score,
            "feedback": [
                {
                    "category": category,
                    "keywords": feedback_data["missing_keywords"].get(category, []),
                    "text": list(feedback_data["suggestions"].get(category, {}).values()),
                }
                for category in ["skills", "experience", "education"]
            ],
            "matched_keywords": [],  # Empty list for now
            "missing_keywords": feedback_data["missing_keywords"],
        }

        return response

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions directly (e.g., 400 Bad Request)
        raise http_exc
    except Exception as exc:
        # Handle unexpected exceptions
        raise HTTPException(status_code=500, detail="An internal server error occurred.") from exc
