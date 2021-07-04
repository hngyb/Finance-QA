import re
import os
import time
from datetime import datetime

from tika import parser
from bs4 import BeautifulSoup
from selenium import webdriver

from app.database.conn import db
import app.database.report as report

DRIVER_PATH = 'app/chromedriver'

class Compare:
    def __init__(self, db):
        self.sess = next(db.session())
        self.contents = None
    
    def download_pdf(self, link):
        """
        최신 REPORT 다운로드 함수
        :return:
        """
        options = webdriver.ChromeOptions()
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                    "download.default_directory": os.getcwd() + '/app/database/PDF',
                    "download.prompt_for_download": False,
                    "plugins.always_open_pdf_externally": True,
                    "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option('prefs', profile)
        driver = webdriver.Chrome(DRIVER_PATH, options=options)
        
        driver.get(link)
        time.sleep(5)
        driver.close()

    def pdf_to_html(self, filename):
        """
        최신 REPORT 형식 변환 함수(PDF -> HTML)
        :return:
        """
        self.contents = parser.from_file(os.getcwd() + f'/app/database/PDF/{filename}.pdf')['content'].strip()
        self.contents = re.sub('([a-zA-Zㄱ-ㅎ가-힣])(\n\n)([a-zA-Zㄱ-ㅎ가-힣])', '\\1\\3', self.contents)
        self.contents = re.sub('(\s)(\n\n)([a-zA-Zㄱ-ㅎ가-힣])', ' \\3', self.contents)
        self.contents = re.sub('[\n ]{4,}', '\n', self.contents)

    def get_report(self, code):
        try:
            sdate = report.get_recent_date(self.sess, code)[0].strftime("%Y-%m-%d")
        except:
            sdate = '2020-11-26'  #DB 크롤링 시작 일자

        edate = datetime.today().strftime("%Y-%m-%d")

        driver = webdriver.Chrome(DRIVER_PATH)
        base_url = 'http://consensus.hankyung.com'
        recent_url = f'http://consensus.hankyung.com/apps.analysis/analysis.list?sdate={sdate}&edate={edate}&now_page=1&search_value=&report_type=CO&pagenum=20&search_text={code}&business_code='
        driver.get(recent_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        try:
            recent_date = sorted([date.text for date in soup.find_all('td', class_= 'first txt_number')])[-1]    

            if recent_date != sdate :
                for idx in range(1, len(soup.select('#contents > div.table_style01 > table > tbody > tr'))+1):
                    date = soup.select(f'#contents > div.table_style01 > table > tbody > tr:nth-of-type({str(idx)}) > td.first.txt_number')[0].get_text()
                    if recent_date == date:
                        title = soup.select(f'#contents > div.table_style01 > table > tbody > tr:nth-of-type({str(idx)}) > td.text_l > div > div > strong')[0].get_text() 
                        company = re.search('(.*)\\(\d', title).group(1)
                        stock_code = re.search('(\d+)', title).group(1)
                        price = soup.select(f'#contents > div.table_style01 > table > tbody > tr:nth-of-type({str(idx)}) > td.text_r.txt_number')[0].get_text()
                        price = price.replace(',', '')
                        opinion = soup.select(f'#contents > div.table_style01 > table > tbody > tr:nth-of-type({str(idx)}) > td:nth-of-type(4)')[0].get_text().strip()
                        writer = soup.select(f'#contents > div.table_style01 > table > tbody > tr:nth-of-type({str(idx)}) > td:nth-of-type(5)')[0].get_text()
                        source = soup.select(f'#contents > div.table_style01 > table > tbody > tr:nth-of-type({str(idx)}) > td:nth-of-type(6)')[0].get_text()
                        url = base_url + soup.select(f'#contents > div.table_style01 > table > tbody > tr:nth-of-type({str(idx)}) > td:nth-of-type(9) > div > a')[0]['href']
                        self.download_pdf(url)
                        report_id = url[-6:]
                        self.pdf_to_html(report_id)
                        row = [report_id, stock_code, title, price, opinion, writer, source, url, ''.join(list(self.contents)[:]), date]
                        report.insert_new(self.sess, row) 
                    else:
                        pass
            return report.get_context(self.sess, code)[0]
        except:
            return False