from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    CHAR,
    DECIMAL,
    Date,
    VARCHAR,
    ForeignKey,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.dialects.mysql import LONGTEXT

from app.database.conn import Base, db

class Company(Base):
    __tablename__ = "company"
    stock_code = Column(CHAR(length=6), nullable=False, unique=True, primary_key=True)
    company_name = Column(VARCHAR(length=50), nullable=False, unique=True)
    report = relationship("Report", back_populates="company")

class Report(Base):
    __tablename__ = "report"
    report_id = Column(Integer, nullable= False, unique=True, primary_key=True)
    stock_code = Column(CHAR(length=6), ForeignKey('company.stock_code'), nullable=False, unique=True)
    title = Column(VARCHAR(512))
    price = Column(DECIMAL(10,2))
    opinion = Column(VARCHAR(20))
    writer = Column(VARCHAR(20))
    source = Column(VARCHAR(20))
    url = Column(VARCHAR(512))
    contents = Column(LONGTEXT)
    report_date = Column(Date)
    company = relationship("Company", back_populates="report")