from pydantic import BaseModel

class QuestionRequest(BaseModel):
    channel_id: str
    content: str