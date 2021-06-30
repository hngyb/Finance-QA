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

def insert_new(db: Session, row):
    new = models.Report(report_id = row[0], stock_code = row[1], title = row[2], price = row[3], opinion = row[4], writer = row[5], source = row[6], url = row[7], contents = row[8], report_date = row[9])
    db.add(new)
    db.commit()

