from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import time

from app.database.conn import db
import app.database.company as company

import requests, json


class View:
    def __init__(self): # 디비 접근 분리 필요
        company_dict = {"company_name":[], "stock_code":[]}
        sess = next(db.session())
        for data in company.get_all_companies(sess):
            company_dict[data.company_name] = data.stock_code
    
        self.companies = company_dict

    def check_name(self, input_qa):
        if input_qa['name'] not in list(self.companies.keys()):
            return('name', '존재하지 않는 종목명입니다.')
        
    def get_answer(self, name, question):
        query = {}
        stock_code = self.companies[name]
        query["stock_code"] = stock_code
        query["question"] = question
        header = {"Content-Type": "application/json"}
        data = json.dumps(query)

        res = requests.post("http://127.0.0.1:8000/api/question", headers=header, data=data)
        res = json.loads(res.text)["ans"]
        
        return res

    def show_processbar(self):
        put_processbar('bar', auto_close = True);
        for i in range(1, 11):
            set_processbar('bar', i / 10)
            time.sleep(0.1)

    def webio(self):
        more = True
        cnt = 1
        
        while(more):
            # input
            input_qa = input_group('쏟아지는 증권사 리포트😱, 궁금한 정보만 찾고싶다면?', [
                input('📈종목명을 입력해주세요.', name = 'name', type = TEXT, datalist = list(self.companies.keys()), required = True),
                input('🧐무엇이 궁금하신가요?', name = 'question', placeholder = '현재 목표주가는 얼마인가요?', required = True)
            ], validate = self.check_name)
            paragraph = '이 보고서는 SK증권의 보고서입니다.'   
        
            # loading
            self.show_processbar()
        
            # output
            put_markdown('# Result %s' %cnt)

            put_tabs([
                {'title': 'Question & Answer', 'content': [
                    put_markdown('### 🧐Question'), 
                    put_code('%s' %input_qa['question']),
                    put_markdown('### 🤗Answer'),
                    put_code('%s' %self.get_answer(input_qa['name'], input_qa['question']))
                ]},
                {'title': 'Appendix', 'content': paragraph}
            ])
            
            more = actions(label = "더 궁금한 점이 있으신가요?",
                            buttons =[{'label': '네, 더 질문할래요!','value': True},
                                    {'label':'아니요, 다음에 이용할게요.', 'value' : False}])
            cnt += 1