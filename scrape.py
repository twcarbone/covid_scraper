import requests
from bs4 import BeautifulSoup as bs
from covid_case import covid_case
from log import logger_setup

logger = logger_setup("get_web_data.py")


def get_soup(url,print_flag=False):
    """

    """
    page = requests.get(url)
    logger.info(f"HTTP status is: {page.status_code}")
    soup = bs(page.content, 'html.parser')

    if print_flag:
        article = soup.find('article')
        print(article.prettify())

    logger.info("soup object successfully returned")
    return soup
    


def parse_html(tag,soup):
    """
    Returns a list of covid_case classes, one for each covid case at EB.
    """
    covid_data = []

    tag_list = soup.find('article').find('div').find_all(tag)
    for pre in tag_list:
    
        # extract some text
        pre_text = pre.get_text() # Posted on October 17, 2020:
        date_str = pre_text[pre_text.index("on")+3:pre_text.index(":")] # October 17, 2020

        ul = pre.next_sibling.next_sibling.find_all('li')
        for li in ul:

            # extract some text
            case_str = li.find('h3').get_text() # #95: Employee at New London facility, Dept. 462

            # add the case to the COVID_Day
            covid_data.append(covid_case(date_str,case_str))

    covid_data.reverse()
    return covid_data
