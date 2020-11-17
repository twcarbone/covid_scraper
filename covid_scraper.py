
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
import numpy as np


# make an http request to the url
url = 'https://eblanding.com/covid-19-case-report-summary/'
page = requests.get(url)


# return a soup object
soup = bs(page.content, 'html.parser')

# print(soup.prettify())
# print(list(soup.children))

covid_data = {}

pre_list = soup.find('article').find('div').find_all('pre')
for pre in pre_list:
    pre_text = pre.get_text() # Posted on October 17, 2020:
    report_date = pre_text[pre_text.index("on")+3:pre_text.index(":")] # October 17, 2020
    # print(report_date)  

    ul = pre.next_sibling.next_sibling.find_all('li')
    cases = []
    for li in ul:
        case = li.find('h3').get_text()
        case_id = case[case.index("#")+1:case.index(":")]
        cases.append(case_id)
        # print(case) # #95: Employee at New London facility, Dept. 462
        # print(case_id) 

    covid_data[report_date] = cases

for date,cases in covid_data.items():
    print(f"{date} -- ",end="")
    for case in cases:
        if case == cases[-1]:
            print(f"{case}")
        else:
            print(f"{case}, ",end="")


# fig, ax = plt.subplots()
# ax.plot([1,2,3,4],[1,4,2,3])
    

# case_list = soup.find('article').find('div').find('ul').find_all('li')
# for li in case_list:
#     print(li.find('h3').get_text())