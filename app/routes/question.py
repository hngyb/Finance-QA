from typing import List
from fastapi import APIRouter

from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database.conn import db
from app.database.schema import Company
from app.database.models import Query, Answer
from app.services.qa import QAModel

router = APIRouter()


@router.post("/api/question", status_code=200, response_model=Answer)
async def get_answer(request: Request, body: Query):
    question = body.question
    context = "2021년 글로벌 스마트폰 출하량 전망을 전년대비 6% 증가한 14.07억대로 하향한다."
    answer = QAModel.get_answer(question, context)

    response = {"question": question, "ans": answer}
    return response