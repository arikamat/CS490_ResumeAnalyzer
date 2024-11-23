# AI Powered Resume Analyzer

High Level Project Overview 

This project will serve as a platform for users to get feedback with an NLP model on improving resumes in addition to getting personalized job recommendations based on their qualifications. Our goals include having a proper fullstack site using React, Python, and utilizing some NLP model.

Users would be able to sign up, log in, upload their resume, and recieve AI feedback on their resume to assist in job applications. 

Goals: 
- User can upload resume and application can conduct text parsing
- NLP analysis for suggesting skills and keyword formatting 
- Job matching with dataset of job descriptions
- User can register, log in, log out, and view dashboard effectively


**[Trello Board](https://trello.com/invite/b/673eacd72cbff9b6965ef40d/ATTI7663db6d740e452040ba181d65c238e9AFC9EA63/cs490-tbd-team-9)**

**[Requirements Github](https://github.com/njit-prof-bill/resume_analyzer_documentation/tree/main)**

Team Members
- Jeremy Kurian (jck44)
- Ari Kamat (ak2762)
- Safwan Noor (sn749)
- Haitham Awad (hha9)
- Noah Paul (ndp)

To contact us, send an email to [UCID][at]njit.edu. Each team member's UCID is listed in parenthesis above


Setting up Project locally

# Frontend 

1. ``npm install`` 
2. ``npm run dev``

# Backend 
1. ``pip install -r backend/requirements.txt``
2. ``uvicorn backend.main:app --reload``

# Backend Tests with code coverage requirement of 80%
1. ``pip install -r backend/requirements.txt``
2. ``pytest --cov=backend --cov-report=term-missing --cov-fail-under=80``
