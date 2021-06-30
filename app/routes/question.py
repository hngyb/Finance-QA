from typing import List
from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database.conn import db
from app.database.schema import Company
from app.database.models import Query, Answer
from app.services.qa import KbQAModel, KoQAModel

from app.services.compare import Compare

router = APIRouter()

@router.post("/api/question", status_code=200, response_model=Answer)
async def get_answer(request: Request, body: Query):
    question = body.question
    stock_code = body.stock_code
    
    db.get_db()
    compareRP = Compare(db)
    context = compareRP.get_report(stock_code)

    kb_answer = KbQAModel.get_answer(question, context)
    ko_answer = KoQAModel.get_answer(question, context)


    response = {"question": question, "kb_ans": kb_answer, "ko_ans": ko_answer}
    return response