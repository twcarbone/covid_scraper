from scrape import *
from crud import *
from models import Case

# Specific querying functions
from sqlalchemy import func, and_, or_


URL = 'https://eblanding.com/covid-19-case-report-summary/'

# Create soup object
soup = get_soup(URL, verbose=False)

# parse all <pre> html tags
cases = parse_html(soup, verbose=False)

recreate_database()

with session_scope() as s:
    for case in cases:
        s.add(Case(
            case_num=case[1],
            date=case[0],
            dept=case[3]
            )
        )

    # SELECT case_num, date FROM cases WHERE dept='462'
#    r = s.query(Case.case_num, Case.date).filter(Case.dept=='462').all()
    
    # SELECT * FROM cases WHERE dept='462' AND case_num>1000
#     r = s.query(Case).filter(
#             and_(
#                 Case.dept=='462',
#                 Case.case_num>1000
#                 )
#             ).all()
   
    # SELECT COUNT(case_num), dept FROM cases GROUP BY dept DESC LIMIT 15
#     r = s.query(
#             func.count(Case.case_num), Case.dept).\
#             group_by(Case.dept).\
#             order_by(func.count(Case.case_num).desc()).\
#             limit(15)
    
    for item in r:
        print(item)

