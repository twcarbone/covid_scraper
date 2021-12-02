import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_soup(URL, verbose=False):
    """
    Return soup object of URL.
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    if verbose:
        article = soup.find('article')
        print(article.prettify())

    return soup    


def parse_html(soup, verbose=False):
    """

    """
    cases = []

    # Each <pre> or <p> tag denotes a new day of case reporting
    # e.g. 'Posted on October 17, 2020:'
    pre = soup.find('article').find('div').find_all('pre')
    p = soup.find('article').find('div').find_all('p')

    for item in pre + p: 
        date = datetime.strptime(item.get_text()[10:-1], '%B %d, %Y')

        # Each case reported on the given day is contained in an <ul> tag
        for li in item.next_sibling.next_sibling.find_all('li'):

            # <h3> of the <li> contains the entire case description
            desc = li.find('h3').get_text()

            # Parse information from each case description
            num = int(desc[desc.find('#')+1:desc.find(':')].replace(',',''))
            bldg = desc[desc.find('from')+4:desc.find('facility')-1]
            dept = desc[desc.find('Dept')+6:desc.find('Dept')+9]

            # Add cases from oldest to newest
            cases.insert(0, (date, num, bldg, dept, desc))

    if verbose:
        for case in cases:
            print('%s, %d, %s, %s (%s)' % case)
        
        print(str(cases[0][1]))
        print(type(cases[0][1]))
        print(len(cases))

    return cases
