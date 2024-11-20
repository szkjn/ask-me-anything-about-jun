from typing import List
from pydantic import BaseModel

class AnswerPath(BaseModel):
    answer_path: str
    explanation: str
    
class FollowUpQuestions(BaseModel):
    follow_up_1: str
    follow_up_2: str
    follow_up_3: str
