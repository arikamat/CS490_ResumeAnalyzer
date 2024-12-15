import json
from backend.schemas.user_input import UserInput
from backend.schemas import CategoricalKeyword
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


def generate_feedback(missing_schema: CategoricalKeyword):
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

    categories = ["skills", "experience", "education"]

    if missing_schema == []:
        return {
            "missing_keywords": {category: [] for category in categories},
            "suggestions": {category: {} for category in categories},
        }

    # Step 2: Extract missing keywords
    missing_keywords = {
        category: getattr(missing_schema, category) for category in categories
    }

    # Step 3: Check if all entries in missing_keywords are empty
    if all(not keywords for keywords in missing_keywords.values()):
        # If there are no missing keywords, return empty suggestions
        return {
            "missing_keywords": missing_keywords,
            "suggestions": {category: {} for category in categories},
        }

    # Step 4: Prepare the prompt for gemini AI
    prompt = FEEDBACK_PROMPT + json.dumps(missing_keywords, indent=2)

    # Step 5: Prompt gemini AI
    retry = 0
    max_retries = 5
    response = None  # Default response in case of repeated failures

    while retry < max_retries:
        try:
            print(f"RF_Attempt {retry + 1}")
            response = prompt_nlp_model(prompt)  # Call the function
            print("Success!")
            break  # Exit loop on success
        except Exception as e:  # Catch specific exceptions
            print(f"Error occurred on attempt {retry + 1}: {e}")
            retry += 1

    if not response:
        return {
            "missing_keywords": missing_keywords,
            "suggestions": {category: {} for category in categories},
        }

    # Step 6: Return the feedback
    return {"missing_keywords": missing_keywords, "suggestions": response}
