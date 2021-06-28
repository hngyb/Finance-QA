from sqlalchemy.orm import Session
import app.database.schema as models

def get_all_companies(db: Session):
    return db.query(models.Company).all()

def get_company_code(db: Session, name):
    return db.query(models.Company.stock_code).filter(models.Company.company_name == name).all()