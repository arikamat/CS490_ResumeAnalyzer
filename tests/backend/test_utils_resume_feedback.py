import pytest
from pathlib import Path
import io
import sys
from backend.schemas.user_input import UserInput
from backend.utils import calculate_fit_score
from backend.utils.fit_score import calculate_match_score
from backend.utils.resume_feedback import generate_feedback

JOB_DESCRIPTION="""
Job Title: Software Engineer
Location: San Francisco, CA
Employment Type: Full-time

About Us: 
We are a dynamic team dedicated to building scalable, user-friendly applications. Join us to create innovative solutions using cutting-edge technologies!

Responsibilities:
Develop, test, and maintain web applications using Python and React, focusing on creating intuitive user interfaces for our enterprise-level project management platform.
Collaborate with cross-functional teams to define and implement new features, working closely with product managers and UX designers to bring innovative solutions to life.
Write clean, maintainable, and efficient code, adhering to best practices and maintaining high-quality code standards.
Debug and resolve software issues promptly, ensuring minimal downtime and optimal system performance.
Stay updated with emerging technologies and best practices, continuously improving our technical approach and team capabilities.

Requirements:
Proficiency in Python and React, with at least 3 years of hands-on experience in building full-stack web applications.
Experience with RESTful APIs and frontend-backend integration, demonstrating ability to create seamless, responsive applications.
Familiarity with version control systems (e.g., Git), with proven experience in collaborative development environments.
Strong problem-solving and communication skills, able to explain complex technical concepts to both technical and non-technical team members.
Bachelor's degree in Computer Science or related field, or equivalent experience from industry work.

Nice-to-Have:
Experience with cloud platforms (e.g., AWS, Azure), particularly in deploying and managing scalable cloud infrastructure.
Knowledge of databases (SQL/NoSQL), including PostgreSQL, MongoDB, or similar database technologies.
Familiarity with testing frameworks and CI/CD pipelines, such as Jenkins, Travis CI, or GitHub Actions.

What We Offer:
Competitive salary range of $120,000 - $160,000 per year, commensurate with experience.
Comprehensive benefits package including health, dental, and vision insurance.
Opportunity to work on exciting and impactful projects that drive technological innovation.
Supportive and growth-focused team environment with regular professional development opportunities.
Flexible work arrangements with remote and hybrid options.

How to Apply: 
Send your resume to careers@innovatetech.com. We look forward to hearing from you!
"""
GOOD_RESUME= """
John Doe
New York, NY | john.doe@email.com | (123) 456-7890 | linkedin.com/in/johndoe | github.com/johndoe

Objective
Passionate software engineer with 3+ years of experience in building scalable web applications. Skilled in Python, React, and modern development tools. Seeking to contribute expertise in full-stack development to drive impactful solutions.

Education
Bachelor of Science in Computer Science
New York University, New York, NY | Graduation Date: May 2020

Technical Skills
Programming Languages: Python, JavaScript, TypeScript
Frontend: React, Redux, Tailwind CSS
Backend: Flask, FastAPI, Django, Node.js
Databases: PostgreSQL, MongoDB
Tools & Platforms: Git, Docker, AWS, RESTful APIs
Testing: Jest, PyTest, Cypress
Other: Agile, CI/CD
Professional Experience
Software Engineer
TechSolutions Inc., New York, NY | June 2020 – Present

Designed and implemented web applications using Python (FastAPI) and React, improving performance by 30%.
Developed and consumed RESTful APIs to ensure seamless communication between frontend and backend systems.
Collaborated with product teams to create user-friendly, responsive interfaces.
Automated test coverage with PyTest and Jest, resulting in 25% fewer production bugs.
Deployed applications to AWS using Docker and managed CI/CD pipelines for faster releases.
Frontend Developer Intern`
Innovate Labs, Brooklyn, NY | Jan 2020 – May 2020

Built dynamic and responsive components using React and Redux for a customer-facing web platform.
Enhanced UI/UX design by integrating Tailwind CSS, boosting customer satisfaction by 20%.
Worked closely with backend developers to consume REST APIs efficiently.
Backend Developer Intern
NextGen Tech, Jersey City, NJ | May 2019 – Aug 2019

Developed RESTful API endpoints using Flask to support a large-scale ecommerce platform.
Implemented database models in PostgreSQL, optimizing query performance by 15%.
Created detailed API documentation to facilitate seamless frontend-backend collaboration.
Projects
TaskFlow (Personal Project)

Developed a task management web app with Python (Flask) and React, supporting real-time updates using WebSockets.
Integrated user authentication and role-based access control with JWT.
RecipeMaster (Team Project)

Built a recipe-sharing platform using Django and React, including features like search, filters, and user reviews.
Deployed the application on AWS and maintained a CI/CD pipeline with GitHub Actions.
Certifications
AWS Certified Developer – Associate
React Nanodegree – Udacity
Professional Development
Regular attendee at NYC Python and React Meetups.
Contributor to open-source projects on GitHub, focusing on web development tools and frameworks.
References available upon request.
"""
BAD_RESUME="""
Jane Smith
Los Angeles, CA | jane.smith@email.com | (555) 123-4567

Objective
Looking for any job that pays well, preferably with minimal effort.

Education
High School Diploma
Springfield High School, Springfield, USA | Graduation Date: June 2016

Technical Skills
Proficient in Microsoft Word and Excel
Typing speed of 50 words per minute
Basic internet browsing skills
Professional Experience
Cashier
Burger Town, Los Angeles, CA | May 2018 – Aug 2020

Handled cash and credit card transactions.
Restocked napkins and condiments.
Cleaned tables and counters.
Customer Service Representative
CallTime Solutions, Los Angeles, CA | Sep 2020 – Present

Answered customer calls about billing issues.
Used a company-provided script to assist customers.
Escalated complex issues to supervisors.
Projects
DIY Garden Blog (Personal Hobby)

Started a blog about growing houseplants.
Posted twice in 2021.
Photography Portfolio (Unfinished)

Took random pictures on my phone to post on social media.
Certifications
None
Professional Development
Attended one-day seminar on "Effective Communication in the Workplace" in 2019.
"""

def test_resume_feedback_normal():
    """
    Test the `generate_feedback` function using a good and a bad resume.

    - Verifies that the good resume has no missing keywords or suggestions.
    - Verifies that the bad resume has missing keywords and generates actionable suggestions.

    This test ensures that the function correctly identifies and handles both well-matched resumes and those lacking necessary qualifications.
    """

    feedback_good = generate_feedback(UserInput(resume_text=GOOD_RESUME, job_description=JOB_DESCRIPTION))
    feedback_bad = calculate_fit_score(UserInput(resume_text=BAD_RESUME, job_description=JOB_DESCRIPTION))

    print(feedback_good)
    print(feedback_bad)

    # Check feedback for the good resume (should have no missing keywords or suggestions)
    assert not feedback_good["missing_keywords"]["skills"]
    assert not feedback_good["missing_keywords"]["experience"]
    assert not feedback_good["missing_keywords"]["education"]
    assert not feedback_good["suggestions"]

    # Check feedback for the bad resume (should have missing keywords and suggestions)
    assert feedback_bad["missing_keywords"]["skills"]
    assert "Python" in feedback_bad["missing_keywords"]["skills"]
    assert feedback_bad["suggestions"]
