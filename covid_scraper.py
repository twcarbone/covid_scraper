
# <article> element of the html is the case tracker
#   <article>
#       <div>
#           <pre>
#               Posted on November 16, 2020
#           </pre>
#           <ul>
#               <li>
#                   <h3>
#                       Employee from New London facility ...
#                   </h3>
#               <li>
#                   <h3>
#                       Employee from Groton facility ...
#                   </h3>
#           </ul>
#           <pre>
#               [...]
#           </pre>
#       </div>
#

import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


# make an http request to the url
url = 'https://eblanding.com/covid-19-case-report-summary/'
page = requests.get(url)


# return a soup object
soup = bs(page.content, 'html.parser')

# print(soup.prettify())
# print(list(soup.children))


class COVID_Day:
    def __init__(self,date):
        self.date = date
        self.case_list = [];
        self.case_ID_list = [];

    def add_case(self,case_id):
        self.case_list.append(case_id)

    def sum_cases(self):
        self.num_cases = len(self.case_list)


covid_data = [];


pre_list = soup.find('article').find('div').find_all('pre')
for pre in pre_list:
    
    # extract some text
    pre_text = pre.get_text() # Posted on October 17, 2020:
    report_date = pre_text[pre_text.index("on")+3:pre_text.index(":")] # October 17, 2020

    # after getting the date create an instance of the COVID_day class using the date
    foo = COVID_Day(report_date)

    ul = pre.next_sibling.next_sibling.find_all('li')
    for li in ul:

        # extract some text
        case = li.find('h3').get_text() # #95: Employee at New London facility, Dept. 462
        case_id = case[case.index("#")+1:case.index(":")] # 95

        # add the case to the COVID_Day
        foo.add_case(case_id)

    foo.sum_cases()
    covid_data.append(foo)


date_list = []
cases_per_day_list = []
for day in covid_data:
    date_list.append(day.date)
    cases_per_day_list.append(day.num_cases)

date_list.reverse()
cases_per_day_list.reverse()


fig,ax = plt.subplots()
ax.plot(date_list,cases_per_day_list,marker="o")
plt.xticks(rotation=45)
plt.xlabel('Date', fontsize=12)
plt.ylabel("Daily Case Count")
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

plt.gcf().autofmt_xdate()
plt.show()