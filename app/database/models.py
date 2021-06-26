from pydantic import BaseModel

class Query(BaseModel):
    stock_code: str = None
    question: str = None

class Answer(BaseModel):
    question: str = None
    ans: str = None