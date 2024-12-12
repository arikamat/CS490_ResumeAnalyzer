import pytest
from pathlib import Path
import io
import sys
from backend.schemas.user_input import UserInput
from backend.utils import calculate_fit_score
from backend.utils.fit_score import calculate_match_score
from backend.utils.resume_feedback import generate_feedback

JOB_DESCRIPTION_LONG="""
Job Title: Software Engineer  
Location: Remote  
Employment Type: Full-time  

About Us:  
Join our fast-growing tech company specializing in scalable, cloud-based solutions. We're looking for a driven and innovative software engineer to contribute to our cutting-edge applications.  

Responsibilities:  
- Develop, test, and maintain robust backend systems using Python and Django.  
- Create responsive and dynamic user interfaces with React and TypeScript.  
- Optimize database performance with PostgreSQL and MongoDB for handling large-scale data.  
- Design and integrate RESTful APIs to ensure seamless frontend-backend communication.  
- Collaborate with DevOps teams to implement CI/CD pipelines using Docker and GitHub Actions.  
- Debug and resolve critical software issues in production environments.  
- Participate in Agile sprints and contribute to technical documentation.  

Requirements:  
- Proficiency in Python and React.  
- Experience with TypeScript and modern JavaScript frameworks.  
- Hands-on experience with databases (PostgreSQL and MongoDB).  
- Knowledge of RESTful API design and integration.  
- Familiarity with CI/CD tools (Docker, GitHub Actions).  
- Strong debugging, communication, and problem-solving skills.  
- Bachelor's degree in Computer Science or related field, or equivalent experience.  

Nice-to-Have:  
- Experience with cloud platforms (AWS, Azure).  
- Exposure to DevOps practices and tools (e.g., Kubernetes, Terraform).  
- Open-source contributions or personal projects demonstrating technical innovation.  

What We Offer:  
- Competitive salary: $100,000 - $140,000/year.  
- Comprehensive benefits package (health, dental, vision).  
- Flexible work hours and remote options.  
- Professional growth opportunities and learning stipends.  

How to Apply:  
Submit your resume and a brief cover letter to careers@cloudinnovators.com.  
"""
GOOD_RESUME_LONG= """
John Overachiever  
San Francisco, CA | john.overachiever@email.com | (123) 456-7890 | linkedin.com/in/overachiever | github.com/overachiever  

Objective  
Visionary software engineer with 10+ years of experience in backend, frontend, and cloud infrastructure development. Seeking to leverage deep technical expertise to drive innovation and scalability at Cloud Innovators.  

Education  
Ph.D. in Computer Science  
Stanford University, CA | Graduation Date: May 2015  

Master of Science in Computer Science  
Massachusetts Institute of Technology (MIT), MA | Graduation Date: May 2012  

Bachelor of Science in Computer Science  
University of California, Berkeley, CA | Graduation Date: May 2010  

Technical Skills  
Programming Languages: Python, JavaScript, TypeScript, Go, Rust, Java  
Frontend: React, Vue.js, Angular, Redux, Tailwind CSS  
Backend: Django, FastAPI, Flask, Spring Boot, Node.js  
Databases: PostgreSQL, MongoDB, DynamoDB, MySQL  
Cloud & DevOps: AWS, Azure, Google Cloud, Kubernetes, Terraform, Jenkins  
Testing: PyTest, Cypress, Selenium, JUnit, Jest  
Other: Agile, Scrum, DevOps, CI/CD  

Professional Experience  

Principal Software Engineer  
TechWorld Corp., San Francisco, CA | June 2017 – Present  
- Architected scalable microservices architecture, reducing latency by 40%.  
- Led a team of 20 engineers to deliver a mission-critical enterprise SaaS platform.  
- Designed and deployed CI/CD pipelines using Docker and Kubernetes on AWS.  
- Spearheaded database optimization, handling over 1 billion queries/day on PostgreSQL and MongoDB.  

Senior Software Engineer  
Cloud Solutions Inc., Seattle, WA | June 2012 – May 2017  
- Developed robust backend systems with Django and Flask, powering high-traffic applications.  
- Implemented advanced RESTful API frameworks, improving integration efficiency by 50%.  
- Built responsive React-based UIs for enterprise clients.  

Projects  
CloudSync (Open Source)  
- Developed a cross-platform cloud synchronization tool with Go and React.  
- Over 50,000 stars on GitHub and adopted by major enterprises.  

Certifications  
AWS Certified Solutions Architect – Professional  
Google Cloud Professional Data Engineer  

References available upon request.  
"""
BAD_RESUME_LONG="""
Jane Doe  
Smalltown, USA | jane.doe@email.com | (555) 123-4567  

Objective  
Looking for a simple, low-stress job in tech.  

Education  
High School Diploma  
Smalltown High School, USA | Graduation Date: May 2018  

Technical Skills  
- Typing speed: 40 WPM  
- Basic Microsoft Word and Excel skills  
- Internet browsing  

Professional Experience  

Cashier  
Corner Mart, Smalltown, USA | June 2020 – Present  
- Handled cash and processed credit card transactions.  
- Stocked shelves and cleaned aisles.  

Front Desk Assistant  
Smalltown Gym, Smalltown, USA | Jan 2019 – May 2020  
- Answered phone calls and scheduled gym memberships.  
- Maintained cleanliness of the reception area.  

Projects  
- Created a blog using a free online template but never published it.  

Certifications  
None  

References available upon request.  
"""
JOB_DESCRIPTION_SHORT = """
Looking for a full-stack JavaScript developer.
Requirements: 
- JavaScript.
- React.
- Git.
- Bachelor's degree in Computer Science.
"""
GOOD_RESUME_SHORT = """
Jane Doe
San Francisco, CA | jane.doe@email.com

Education
Bachelor of Science in Computer Science

Experience
Full-Stack Developer with React.

Skills
JavaScript, React, Git
"""
BAD_RESUME_SHORT = """
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
    feedback_good = generate_feedback(UserInput(resume_text=GOOD_RESUME_LONG, job_description=JOB_DESCRIPTION_LONG))
    feedback_bad = generate_feedback(UserInput(resume_text=BAD_RESUME_LONG, job_description=JOB_DESCRIPTION_LONG))

    # Verify that the bad resume has more missing keywords than the good resume
    assert len(feedback_bad["missing_keywords"]["skills"]) >= len(feedback_good["missing_keywords"]["skills"])
    assert len(feedback_bad["missing_keywords"]["experience"]) >= len(feedback_good["missing_keywords"]["experience"])
    assert len(feedback_bad["missing_keywords"]["education"]) >= len(feedback_good["missing_keywords"]["education"])

    # Verify that the bad resume has more suggestions than the good resume
    assert len(feedback_bad["suggestions"]) > len(feedback_good["suggestions"])

def test_generate_feedback_missing_keywords():
    """
    Test the `generate_feedback` function using a good and a bad resume.

    - Verifies that the good resume has no missing keywords or suggestions.
    - Verifies that the bad resume has missing keywords and generates actionable suggestions.

    This test ensures that the function correctly identifies missing keywords and generates appropriate feedback.
    """
    feedback_good = generate_feedback(UserInput(resume_text=GOOD_RESUME_SHORT, job_description=JOB_DESCRIPTION_SHORT))
    feedback_bad = generate_feedback(UserInput(resume_text=BAD_RESUME_SHORT, job_description=JOB_DESCRIPTION_SHORT))
    
    print(feedback_good)
    print(feedback_bad)
    
    # Verify that keywords missing from bad resume are correctly extracted
    assert "javascript" in feedback_bad["missing_keywords"]["skills"]
    assert "bachelor's" in feedback_bad["missing_keywords"]["education"]
    assert "full-stack" in feedback_bad["missing_keywords"]["experience"]
    assert feedback_bad["suggestions"]
    
    # Verify that nothing is missing from the good resume
    assert not feedback_good["missing_keywords"]["skills"]
    assert not feedback_good["missing_keywords"]["education"]
    assert not feedback_good["missing_keywords"]["experience"]
    assert not feedback_good["suggestions"]
    
def test_generate_feedback_missing_job_description():
    """
    Test the `generate_feedback` function when the job description is empty.

    - Verifies that no keywords are flagged as missing.
    - Verifies that no suggestions are generated.
    """
    feedback = generate_feedback(UserInput(resume_text=GOOD_RESUME_SHORT, job_description=""))
    
    # Ensure no keywords are flagged as missing
    assert not feedback["missing_keywords"]["skills"]
    assert not feedback["missing_keywords"]["education"]
    assert not feedback["missing_keywords"]["experience"]
    
    # Ensure no suggestions are generated
    assert not feedback["suggestions"], "Suggestions should not be generated without a job description."
