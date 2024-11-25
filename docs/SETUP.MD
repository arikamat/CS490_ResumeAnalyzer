# Setting up Project locally

## Frontend 

1. ``cd frontend``
2. ``npm install`` - Installs Dependencies 
3. ``npm run dev``

## Frontend Tests with code coverage requirement of 80%

1. ``cd frontend``
2. ``npm install`` - Installs Dependencies 
3. ``npx jest --coverage --coverageThreshold '{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'``

## Backend 
1. ``pip install -r backend/requirements.txt``
2. ``uvicorn backend.main:app --reload``
3. Move ``.env`` file into backend folder. Contact a developer (README.md) for access to .env file

## Backend Tests with code coverage requirement of 80%
1. ``pip install -r backend/requirements.txt``
2. ``pytest --cov=backend --cov-report=term-missing --cov-fail-under=80``
