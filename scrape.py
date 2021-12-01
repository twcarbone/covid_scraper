import requests
from bs4 import BeautifulSoup


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
        date = item.get_text()[10:-1]

        # Each case reported on the given day is contained in an <ul> tag
        for li in item.next_sibling.next_sibling.find_all('li'):

            # <h3> of the <li> contains the case informatioon
            case = li.find('h3').get_text()

            # Add cases from oldest to newest
            cases.insert(0, (date, case))

    if verbose:
        for case in cases:
            print(case[0] + ': ' + case[1])

    return cases
