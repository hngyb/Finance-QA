from sqlalchemy.orm import Session
import app.database.schema as models

def get_context(db: Session, code):
    return db.query(models.Report.contents).filter(models.Report.stock_code == code).order_by(models.Report.report_date.desc()).first()

def get_recent_date(db: Session, code):
    return db.query(models.Report.report_date).filter(models.Report.stock_code == code).order_by(models.Report.report_date.desc()).first()

def get_title(db: Session, code):
    return db.query(models.Report.title).filter(models.Report.stock_code == code).order_by(models.Report.report_date.desc()).first()

def get_source(db: Session, code):
    return db.query(models.Report.source).filter(models.Report.stock_code == code).order_by(models.Report.report_date.desc()).first()

def get_url(db: Session, code):
    return db.query(models.Report.url).filter(models.Report.stock_code == code).order_by(models.Report.report_date.desc()).first()

def insert_new(db: Session, row):  # compare.py에서 사용되는 함수 / db에 제대로 들어가는지 확인 필요
    new = models.Report(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    db.add(new)
    db.commit()

