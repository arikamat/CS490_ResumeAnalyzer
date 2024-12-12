import pytest
from pathlib import Path
import io
import sys
from backend.schemas.user_input import UserInput
from backend.utils import calculate_fit_score
from backend.utils.fit_score import calculate_match_score
from backend.utils.resume_feedback import generate_feedback

JOB_DESCRIPTION = """
Looking for a Frontend JavaScript developer.
Requirements: 
- JavaScript.
- React.
- Git.
- Bachelor's degree in Computer Science.
"""
GOOD_RESUME = """
Jane Doe
San Francisco, CA | jane.doe@email.com

Education
Bachelor of Science in Computer Science

Experience
Frontend Developer with React.

Skills
JavaScript, React, Git
"""
BAD_RESUME = """
John Smith
Los Angeles, CA | john.smith@email.com

Education
High School Diploma

Skills
HTML, CSS, Microsoft Office
"""

def test_generate_feedback_good_bad_resumes():
    """
    Test the `generate_feedback` function using a good and a bad resume.

    - Verifies that the good resume has less missing keywords than the bad resume
    - Verifies that the good resume has less suggestions than the bad resume

    This test ensures that the function correctly identifies and handles both well-matched resumes and those lacking necessary qualifications.
    """
    feedback_good = generate_feedback(UserInput(resume_text=GOOD_RESUME, job_description=JOB_DESCRIPTION))
    feedback_bad = generate_feedback(UserInput(resume_text=BAD_RESUME, job_description=JOB_DESCRIPTION))

    # Verify that the bad resume has more missing keywords than the good resume
    assert len(feedback_bad["missing_keywords"]["skills"]) >= len(feedback_good["missing_keywords"]["skills"])
    assert len(feedback_bad["missing_keywords"]["experience"]) >= len(feedback_good["missing_keywords"]["experience"])
    assert len(feedback_bad["missing_keywords"]["education"]) >= len(feedback_good["missing_keywords"]["education"])

    # Verify that the bad resume has more suggestions than the good resume
    assert len(feedback_bad["suggestions"]) >= len(feedback_good["suggestions"])

def test_generate_feedback_missing_keywords():
    """
    Test the `generate_feedback` function using a good and a bad resume.

    - Verifies that the good resume has no missing keywords or suggestions.
    - Verifies that the bad resume has missing keywords and generates actionable suggestions.

    This test ensures that the function correctly identifies missing keywords and generates appropriate feedback.
    """
    feedback_good = generate_feedback(UserInput(resume_text=GOOD_RESUME, job_description=JOB_DESCRIPTION))
    feedback_bad = generate_feedback(UserInput(resume_text=BAD_RESUME, job_description=JOB_DESCRIPTION))
    
    # Verify that keywords missing from bad resume are correctly extracted
    assert "javascript" in feedback_bad["missing_keywords"]["skills"]
    assert feedback_bad["suggestions"]
    
    # Verify that nothing is missing from the good resume
    assert not feedback_good["missing_keywords"]["skills"]
    assert not feedback_good["suggestions"]
    
def test_generate_feedback_missing_job_description():
    """
    Test the `generate_feedback` function when the job description is empty.

    - Verifies that no keywords are flagged as missing.
    - Verifies that no suggestions are generated.
    """
    feedback = generate_feedback(UserInput(resume_text=GOOD_RESUME, job_description=""))
    
    # Ensure no keywords are flagged as missing
    assert not feedback["missing_keywords"]["skills"]
    assert not feedback["missing_keywords"]["education"]
    assert not feedback["missing_keywords"]["experience"]
    
    # Ensure no suggestions are generated
    assert not feedback["suggestions"], "Suggestions should not be generated without a job description."
