from fastapi import APIRouter
from starlette.requests import Request

from app.database.conn import db
from app.database.models import Query, Answer
from app.services.qa import KbQAModel, KoQAModel

from app.services.compare import Compare

import app.database.company as company
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

@router.get("/api/companies", status_code=200)
async def get_companies():
    db.get_db()
    sess = next(db.session())
    return company.get_all_companies(sess)
