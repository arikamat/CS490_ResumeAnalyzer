import string
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from backend.schemas.categorical_keyword import CategoricalKeyword
from backend.schemas.user_input import UserInput
from backend.utils.nlp import prompt_nlp_model

stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

JOB_DESCRIPTION_PROMPT = """
You are an AI trained to analyze job descriptions and extract highly specific, bite-sized keywords. Your task is to categorize these keywords into three groups: skills, experience, and education. Each keyword should be 1 word to maximize matching potential.

1. Skills: Extract tools, technologies, programming languages, certifications, or soft skills mentioned in the job description (e.g., "Python", "AWS", "Leadership"). Each keyword should be exactly 1 word 
2. Experience: Extract concise job-related phrases or concepts (e.g., "mobile", "data"). Each keyword should be exactly 1 word 
3. Education: Extract minimal, precise educational or certification-related terms (e.g., "Bachelor's", "Computer", "MBA"). Each keyword should be exactly 1 word 

Output:
Provide a JSON response in this format:

```
{
  "skills": ["List of skills. Each keyword should be exactly 1 word"],
  "experience": ["List of experience-related keywords. Each keyword should be exactly 1 word"],
  "education": ["List of education-related keywords. Each keyword should be exactly 1 word"]
}
```

Return ONLY the JSON output and nothing else. Ensure the output uses proper JSON formatting with double quotes for all keys and values, and proper opening and closing braces.

If you can't find any dont just extract my examples. Only extract from the following input. it is okay if you can't find any keywords. just leave it as an empty list []

Input (Job Description):


"""

# RESUME_PROMPT = """
# You are an AI trained to analyze resumes and extract highly specific, bite-sized keywords. Your task is to categorize these keywords into three groups: skills, experience, and education. Each keyword should be exactly 1 word to maximize matching potential.

# 1. Skills: Extract tools, technologies, programming languages, certifications, or soft skills mentioned in the job description (e.g., "Python", "AWS", "Leadership"). Keywords should be less than 3 words
# 2. Experience: Extract concise job-related phrases or concepts (e.g., "mobile", "data"). Each keyword should be exactly 1 word
# 3. Education: Extract minimal, precise educational or certification-related terms (e.g., "Bachelor's", "Computer", "MBA"). Each keyword should be exactly 1 word

# Output:
# Provide a JSON response in this format:
# ```
# {
#   "skills": ["List of skills. Each keyword should be exactly 1 word"],
#   "experience": ["List of experience-related keywords. Each keyword should be exactly 1 word"],
#   "education": ["List of education-related keywords. Each keyword should be exactly 1 word"]
# }
# ```
# Return ONLY the JSON output and nothing else. Ensure the output uses proper JSON formatting with double quotes for all keys and values, and proper opening and closing braces. Ensure every keyword is 1 word.

# If you can't find any dont just extract my examples. Only extract from the following input. it is okay if you can't find any keywords. just leave it as an empty list []
# Input (Resume Text):


# """
def get_synonyms(word):
    """
    Return a set of synonyms for a given word using nltk/wordnet.

    Args:
        word (str): The word for which synonyms will be generated.

    Returns:
        set: A set containing synonyms of the given word.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms


def process_keyword(keyword, synonyms=False):
    """
    Process a keyword by removing punctuation, stemming it, and adding its synonyms.

    Args:
        keyword (str): The keyword to process.

    Returns:
        set: A set containing the processed keyword, stemmed content, synonyms, and stemmed synonyms
    """
    s = set()
    keyword = keyword.lower()
    if "/" in keyword:
        s = s.union(set(keyword.split("/")))
    keyword = keyword.translate(str.maketrans("", "", string.punctuation))

    if keyword in stop_words:
        return s
    stemmed_keyword = stemmer.stem(keyword)

    s.add(stemmed_keyword)
    s.add(keyword)

    if synonyms:
        for synonym in get_synonyms(keyword):
            syn = synonym.lower().replace("_", " ")
            s.add(syn)
            s.add(stemmer.stem(syn))
    return s


def process_keywords(keywords):
    """
    Process a list of keywords and combine their processed results into a set.

    Args:
        keywords (list): A list of keywords to process.

    Returns:
        set: A set containing the processed keywords.
    """
    s = set()
    for keyword in keywords:
        s = s.union(process_keyword(keyword))
    return s


def calculate_match_score(job_keywords, resume_keywords, weights):
    """
    Calculate match scores for job and resume keywords based on category weights.

    Args:
        job_keywords (dict): A dictionary with list of job keywords categorized by skills, experience, and education.
        resume_keywords (list): A list of all words in resume
        weights (dict): A dictionary of category weights for skills, experience, and education.

    Returns:
        total_fit_score (float): The overall fit score.
        scores (dict):Category-wise match scores.
        missing (dict): Missing keywords in each category.
        matched (dict): Keywords that matched in each category
    """

    processed_resume_keywords = process_keywords(resume_keywords)

    scores = {}
    missing = {"skills": [], "education": [], "experience": []}
    matched = {"skills": [], "education": [], "experience": []}
    for category, weight in weights.items():
        match_ct = 0
        for i in job_keywords[category]:
            stemmed_and_syn = process_keyword(i)
            matches = stemmed_and_syn.intersection(processed_resume_keywords)
            if len(matches) > 0:
                match_ct += 1
                matched[category].append(i)
            else:
                missing[category].append(i)
        if len(job_keywords[category]) == 0:
            scores[category] = weight
        else:
            scores[category] = weight * match_ct / len(job_keywords[category])

    # Compute total fit score
    total_fit_score = sum(scores.values())
    return total_fit_score, scores, missing, matched


def calculate_fit_score(user_input: UserInput):
    """
    Compute the overall fit score for a user's resume compared to a job description.

    This function utilizes Gemini to extract categorized keywords from the job description. It calculates a fit score based on category weights
    (skills, experience, and education) and how many of them match and also outputs missing keywords in each category.

    Args:
        user_input (UserInput): An object containing the following attributes:
        resume_text (str): The text content of the user's resume.
        job_description (str): The text content of the job description.

    Returns:
        fit_score (float): The overall fit score, a weighted value indicating the alignment between the resume and job description.
        missing_schema (CategoricalKeyword): An object containing the missing keywords for each category (skills, experience, education).
        matched_schema (CategoricalKeyword): An object containing the matched keywords for each category (skills, experience, education).

    Workflow:
        1. Ask AI to extract relevant keywords from job description and resume and categorize it
        2. Splits multi-word keywords into individual words, removes duplicates, and convert them to lowercase for consistent comparison.
        3. Calculates the fit score and missing keywords by comparing processed keywords across categories, applying weights to categories (skills: 60%, experience: 20%, education: 20%). Uses stemming and synonym matching to maximize chances of a match
        4. Returns the fit score and a schema detailing missing keywords.
    """
    basic = {"skills": [], "education": [], "experience": []}
    if len(user_input.resume_text) == 0:
        return 0.0, CategoricalKeyword(**basic), CategoricalKeyword(**basic)
    if len(user_input.job_description) == 0:
        return 0.0, CategoricalKeyword(**basic), CategoricalKeyword(**basic)

    # resume_prompt = RESUME_PROMPT + user_input.resume_text
    job_prompt = JOB_DESCRIPTION_PROMPT + user_input.job_description.replace("/", " ")
    resume_keywords = user_input.resume_text.replace("/", " ").split()
    resume_keywords = list(set(resume_keywords))
    resume_keywords = [x.lower() for x in resume_keywords]

    # Ask ai to get keywords of job description
    retry = 0
    flag = True
    while flag and retry < 5:
        try:
            print(f"FS_Attempt: {retry + 1}")
            job_keywords = prompt_nlp_model(job_prompt)
            parsed = CategoricalKeyword(**job_keywords)
            print("Successfully parsed keywords.")
            flag = False
        except Exception as e:
            print(f"Error occurred on attempt {retry + 1}: {e}")
            retry += 1

    WEIGHTS = {"skills": 0.6, "experience": 0.2, "education": 0.2}
    CATEGORIES = ["skills", "experience", "education"]

    # Even if ai gives us multiple worded keywords. This will split it all up
    for category in CATEGORIES:
        job_keywords[category] = [
            word for string in job_keywords[category] for word in string.split()
        ]
        job_keywords[category] = list(set(job_keywords[category]))

    for category in CATEGORIES:
        job_keywords[category] = [x.lower() for x in job_keywords[category]]

    # if job description is bogus return 0
    total_keywords = 0
    for i in job_keywords:
        total_keywords += len(job_keywords[i])
    if total_keywords == 0:
        return 0.0, CategoricalKeyword(**basic), CategoricalKeyword(**basic)

    fit_score, detailed_scores, missing, matched = calculate_match_score(
        job_keywords, resume_keywords, WEIGHTS
    )

    missing_schema = CategoricalKeyword(**missing)
    matched_schema = CategoricalKeyword(**matched)
    return fit_score, missing_schema, matched_schema
