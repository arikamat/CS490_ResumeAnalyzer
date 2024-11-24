# Setting up Project locally

## Frontend 

1. ``npm install`` - Installs Dependencies 
2. ``npm run dev``

## Backend 
1. ``pip install -r backend/requirements.txt``
2. ``uvicorn backend.main:app --reload``

## Backend Tests with code coverage requirement of 80%
1. ``pip install -r backend/requirements.txt``
2. ``pytest --cov=backend --cov-report=term-missing --cov-fail-under=80``