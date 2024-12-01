from pydantic import BaseModel


# Object to save the API reply
class FitScore(BaseModel):
    fit_score: int
    feedback: list[str]
