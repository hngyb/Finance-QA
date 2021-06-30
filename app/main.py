from dataclasses import asdict
from typing import Optional

import uvicorn
from fastapi import FastAPI
from pywebio.platform.fastapi import webio_routes
from app.database.conn import db
from app.common.config import conf
from app.routes import index, question

from app.view import View
from app.services.compare import Compare

def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    app.include_router(index.router)
    app.include_router(question.router)

    view = View()
    # compareRP = Compare()
    # compareRP.get_report("005930")
    app.mount("/view", FastAPI(routes=webio_routes(view.webio)))
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)