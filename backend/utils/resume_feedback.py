from backend.schemas.user_input import UserInput
from backend.utils.fit_score import calculate_fit_score

def generate_feedback(user_input: UserInput):
    """
    Generate actionable feedback based on missing keywords.

    Args:
        user_input (UserInput): An object containing the following attributes:
            - resume_text (str): The text content of the user's resume.
            - job_description (str): The text content of the job description.

    Returns:
        dict: A dictionary containing:
            - missing_keywords (dict): Missing keywords categorized by skills, experience, and education.
            - suggestions (list): Actionable suggestions to improve the resume.
    """
    # Step 1: Calculate the fit score and missing schema
    fit_score, missing_schema = calculate_fit_score(user_input)
        
    # Step 2: Extract missing keywords
    CATEGORIES = ["skills", "experience", "education"]
    missing_keywords = {category: getattr(missing_schema, category) for category in CATEGORIES}

    suggestions = {}    # Placeholder for suggestions

    feedback = {
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }

    # Step 4: Return feedback
    return {
        feedback
    }
