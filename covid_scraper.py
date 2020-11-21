
# <article> element of the html is the case tracker
#   <article>
#       <div>
#           <pre> **
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
#   ** some <pre> </pre> entries are <p> </P instead

import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

# make an http request to the url
url = 'https://eblanding.com/covid-19-case-report-summary/'
page = requests.get(url)


# return a soup object
soup = bs(page.content, 'html.parser')

# print(soup.prettify())
# print(list(soup.children))


def print_case_list_per_day(covid_data):
    for day in covid_data:
        print(f"{day.date_str} ({day.date_obj}) -- ",end="")

        for case in day.case_list:
            if case == day.case_list[-1]:
                print(case)
            else:
                print(f"{case}, ",end="")


def parse_html(tag,soup):
    covid_data = []

    tag = soup.find('article').find('div').find_all(tag)
    for pre in tag:
    
        # extract some text
        pre_text = pre.get_text() # Posted on October 17, 2020:
        report_date = pre_text[pre_text.index("on")+3:pre_text.index(":")] # October 17, 2020

        # after getting the date create an instance of the COVID_day class using the date
        foo = COVID_Day(report_date)

        # convert the date string into a datetime object
        foo.make_date_obj()

        ul = pre.next_sibling.next_sibling.find_all('li')
        for li in ul:

            # extract some text
            case = li.find('h3').get_text() # #95: Employee at New London facility, Dept. 462
            case_id = case[case.index("#")+1:case.index(":")] # 95

            # add the case to the COVID_Day
            foo.add_case(case_id)

        foo.sum_cases() # creates a self.num_cases property
        covid_data.append(foo)

    return covid_data


# class for covid day
class COVID_Day:
    def __init__(self,date_str):
        self.date_str = date_str
        self.case_list = [];
        self.case_ID_list = [];

    def add_case(self,case_id):
        self.case_list.append(case_id)

    def sum_cases(self):
        self.num_cases = len(self.case_list)

    def update_running_total(self,previous_total=87):
        # the online case counter started at case 88, so the previous total was 87
        self.running_total = self.num_cases + previous_total

    def make_date_obj(self):
        self.date_obj = datetime.strptime(self.date_str,'%B %d, %Y')

# ==================================================

covid_data_pre = parse_html('pre',soup)
covid_data_p = parse_html('p',soup) # October 19th & 23rd

print_case_list_per_day(covid_data_pre)
print("================================================================================")
print_case_list_per_day(covid_data_p)




"""
# the list starts with the most recent data, so we need to reverse it to be in 
# chronological order
covid_data.reverse()


date_list = []
cases_per_day_list = []
running_total_list = []
for i,day in enumerate(covid_data):

    if day == covid_data[0]:
        # if it is the first day of data, then there is no previous day and the method
        # defaults to adding 87 to the current day's case count
        day.update_running_total()
    else:
        # otherwise, add the running total from the previous day to today's case count
        day.update_running_total(covid_data[i-1].running_total)

    # make lists for plotting purposes
    date_list.append(day.date)
    cases_per_day_list.append(day.num_cases)
    running_total_list.append(day.running_total)




fig,ax = plt.subplots(2,figsize=(10,7))
fig.suptitle("COVID Cases at Electric Boat")
ax[0].plot(date_list,cases_per_day_list,marker="o")
ax[1].plot(date_list,running_total_list,marker="o")

plt.xticks(rotation=45)
ax[0].set_ylabel("Cases Per Day")
ax[1].set_ylabel("Running Total")

ax[1].xaxis.set_major_locator(mdates.AutoDateLocator())

plt.gcf().autofmt_xdate()
plt.show()
"""