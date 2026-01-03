from pydantic import BaseModel

class JobHuntState(BaseModel):
    cv_text: str
    job_title: str
    job_description: str
    task: str
    model_name: str        # ✅ NEW
    feedback: str = ""
    satisfied: bool = False

    # outputs
    cover_letter: str = ""
    networking: str | dict = ""
    review: str | dict = ""
