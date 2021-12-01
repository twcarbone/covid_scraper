from scrape import *


URL = 'https://eblanding.com/covid-19-case-report-summary/'

# Create soup object
soup = get_soup(URL, verbose=False)

# parse all <pre> html tags
cases = parse_html(soup, verbose=False)

