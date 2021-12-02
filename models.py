from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Case(Base):
    __tablename__ = 'cases'

    case_id = Column(Integer, primary_key=True)
    case_num = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    dept = Column(String, nullable=False)

    def __repr__(self):
        return "<Case(case_id='{}', case_num='{}', date='{}', dept='{}')>"\
                .format(self.case_id, self.case_num, self.date, self.dept)
    


