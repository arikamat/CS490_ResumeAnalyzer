import json
from backend.schemas.user_input import UserInput
from backend.utils.fit_score import calculate_fit_score
from backend.utils.nlp import prompt_nlp_model

FEEDBACK_PROMPT = """
You are an AI trained to analyze missing resume content and provide highly specific actionable feedback. Your task is to generate feedback for each missing keyword that is present in a job description but not found on a resume. These keywords are categorized into three groups: skills, experience, and education.

1. Skills: For each missing skill, provide feedback to include or enhance tools, technologies, programming languages, certifications, or soft skills (e.g., "Python", "AWS", "Leadership").
2. Experience: For each missing experience keyword, suggest improvements to highlight relevant job-related experiences (e.g., "mobile", "data").
3. Education: For each missing education keyword, recommend specific academic qualifications, certifications, or degrees (e.g., "Bachelor's", "Computer", "MBA").

Output:
Provide a JSON response in this format:
{
  "skills": {
    "keyword1": "Feedback for keyword1",
    "keyword2": "Feedback for keyword2"
  },
  "experience": {
    "keyword1": "Feedback for keyword1",
    "keyword2": "Feedback for keyword2"
  },
  "education": {
    "keyword1": "Feedback for keyword1",
    "keyword2": "Feedback for keyword2"
  }
}

Return ONLY the JSON output and nothing else. Ensure the output uses proper JSON formatting with double quotes for all keys and values, and proper opening and closing braces.

Input (missing_keywords):

"""


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
            - suggestions (dict): Actionable suggestions categorized by skills, experience, and education.
    """
    # Step 1: Calculate the fit score and missing schema
    fit_score, missing_schema = calculate_fit_score(user_input)

    # Step 2: Extract missing keywords
    categories = ["skills", "experience", "education"]
    missing_keywords = {category: getattr(missing_schema, category) for category in categories}

    # Step 3: Prepare the prompt for Groq AI
    prompt = FEEDBACK_PROMPT + json.dumps(missing_keywords, indent=2)

    # Step 4: Prompt Groq AI
    retry = 0
    max_retries = 5

    while retry < max_retries:
        try:
            response = prompt_nlp_model(prompt)
            break
        except Exception as e:
            retry += 1
            pass

    suggestions = [feedback for category in response.values() for feedback in category.values()]

    # Step 5: Return the feedback
    return {
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }
