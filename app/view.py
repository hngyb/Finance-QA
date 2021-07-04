from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import time

from app.database.conn import db
import app.database.company as company
import app.database.report as report

import requests, json


class View:
    def __init__(self):
        company_dict = {}
        self.companies = company_dict
        self.sess = next(db.session())
    
    def get_companies(self):
        headers = {'accept': 'application/json'}
        res = requests.get("http://127.0.0.1:8000/api/companies", headers=headers)
        res = json.loads(res.text)
        for data in res:
            self.companies[data['company_name']] = data['stock_code']
        
    def check_name(self, input_qa):
        if input_qa['name'] not in list(self.companies.keys()):
            return('name', '존재하지 않는 종목명입니다.')
        
    def get_answer(self, name, question):
        query = {}
        try:
            stock_code = self.companies[name]
            query["stock_code"] = stock_code
            query["question"] = question
            header = {"Content-Type": "application/json"}
            data = json.dumps(query)

            res = requests.post("http://127.0.0.1:8000/api/question", headers=header, data=data)
            kb_res = json.loads(res.text)["kb_ans"]
            ko_res = json.loads(res.text)["ko_ans"]

            res = "KBAlbert: " + kb_res + "\nKobert: " + ko_res
        except:
            res = '최근 6개월 내에 발행된 신규 리포트가 존재하지 않습니다.'
            
        return res

    def get_reportinfo(self, name):
        info = {}
        try: 
            stock_code = self.companies[name]
            info['title'] = report.get_title(self.sess, stock_code)[0]
            info['report_date'] = report.get_recent_date(self.sess, stock_code)[0]
            info['source'] = report.get_source(self.sess, stock_code)[0]
            info['url'] = report.get_url(self.sess, stock_code)[0]
        except:
            info = {'title': '-', 'report_date': '-', 'source': '-', 'url': '-'}
        return info

    def show_processbar(self):
        put_processbar('bar', auto_close = True)
        for i in range(1, 11):
            set_processbar('bar', i / 10)
            time.sleep(0.1)

    def webio(self):
        self.get_companies()
        more = True
        
        while(more):
            with use_scope('scope', clear =True):
                # input
                input_qa = input_group('쏟아지는 증권사 리포트, 궁금한 정보만 찾고싶다면?', [
                    input('📈종목명을 입력해주세요.', name = 'name', type = TEXT, datalist = list(self.companies.keys()), required = True),
                    input('🧐무엇이 궁금하신가요?', name = 'question', placeholder = 'EX) 현재 목표주가는 얼마인가요?', required = True)
                ], validate = self.check_name)
            
                # loading
                answer = self.get_answer(input_qa['name'], input_qa['question'])
                reportinfo = self.get_reportinfo(input_qa['name'])
                    
                self.show_processbar()
            
                # output
                put_markdown('# Result [%s]' %input_qa["name"])

                put_tabs([
                    {'title': 'Question & Answer', 'content': [
                        put_markdown('### 🧐Question'), 
                        put_code('%s' %input_qa['question']),
                        put_markdown('### 🤗Answer'),
                        put_code('%s' %answer)
                    ]},
                    {'title': 'Appendix', 'content': put_table([
                                                        ['제목', reportinfo['title']],
                                                        ['날짜', reportinfo['report_date']],
                                                        ['출처', reportinfo['source']],
                                                        ['원문 리포트', put_markdown('[Link](%s)' %reportinfo["url"])]
                                                    ])
                    }
                ])

            more = actions(label = "더 궁금한 점이 있으신가요?",
                            buttons =[{'label': '네, 더 질문할래요!','value': True},
                                    {'label':'아니요, 다음에 이용할게요.', 'value' : False}])