from sqlalchemy.orm import Session
import app.database.schema as models

def get_all_companies(db: Session):
    return db.query(models.Company).all()