from scrape import *
from crud import *
from models import Case


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


