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
1. Run ``sudo apt install python3-venv`` in project root
2. Run ``python3 -m venv venv`` in project root
3. Run ``source venv/bin/activate`` in project root
4. Run ``pip install -r backend/requirements.txt`` in project root
5. Run ``python -c "import nltk; nltk.download('wordnet'); nltk.download('stopwords')"`` in project root
6. Move ``.env`` file into backend folder. Contact a developer (README.md) for access to .env file
7. Run ``uvicorn backend.main:app --reload`` in project root


## Backend Tests with code coverage requirement of 80%
1. Follow steps 1-6 in the backend section
2. Run ``pytest --cov=backend --cov-report=term-missing --cov-fail-under=80`` in project root
