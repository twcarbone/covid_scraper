
"""
//
<article> element of the html is the case tracker
    <article>
        <div>
            <pre> **
                Posted on November 16, 2020
            </pre>
            <ul>
                <li>
                     <h3>
                          Employee from New London facility ...
                    </h3>
                <li>
                    <h3>
                        Employee from Groton facility ...
                    </h3>
            </ul>
        <pre>
            [...]
        </pre>
        <p> **
            [...]
        </p>
    </div>

** both <pre> and <p> tags are used to denote daily postings

//
Note: to be able to see a figure from wsl using matplotlib:
    0. install VcXsrv on Windows
    1. from Windows, run C:/Program Files/VcXsrv/xlaunch.exe
    2. from wsl, run 'export DISPLAY=localhost:0.0'

"""


import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from covid_classes import COVID_Day as COVID_Day


# make an http request to the url
url = 'https://eblanding.com/covid-19-case-report-summary/'
page = requests.get(url)


# return a soup object
soup = bs(page.content, 'html.parser')

# print(soup.prettify())
# print(list(soup.children))


def parse_html(tag,soup):
    covid_data = []

    tag_list = soup.find('article').find('div').find_all(tag)
    for pre in tag_list:
    
        # extract some text
        pre_text = pre.get_text() # Posted on October 17, 2020:
        report_date = pre_text[pre_text.index("on")+3:pre_text.index(":")] # October 17, 2020

        # after getting the date create an instance of the COVID_day class using the date
        foo = COVID_Day(report_date)

        ul = pre.next_sibling.next_sibling.find_all('li')
        for li in ul:

            # extract some text
            case = li.find('h3').get_text() # #95: Employee at New London facility, Dept. 462

            # add the case to the COVID_Day
            foo.add_case(case)

        foo.sum_cases() # creates a self.num_cases property
        covid_data.append(foo)

    covid_data.reverse()
    return covid_data


def print_cases(covid_data,option):
    """
    Helper function for testing.

    option      1: 'case_num -- location'
                2: 'date -- case_num_list'
                3: 'short'
                4: 'long'
    """
    for day in covid_data:
        # 
        if option == 1:
            for case_num, location in zip(day.case_num_list,day.location_list):
                print(f"{case_num}:\t{location}")

        #
        elif option == 2:
            print(f"{day.date_str} ({day.date_obj}) -- ",end="")

            for case_num in day.case_num_list:
                if case_num == day.case_num_list[-1]:
                    print(case_num)
                else:
                    print(f"{case_num}, ",end="")

        else:
            for case in day.case_list:
                #
                if option == 3:
                    print(case[0:100])

                #
                elif option == 4:
                    print(case)



def print_unique_locations(covid_data):
    unique = []
    for day in covid_data:
        for location in day.location_list:
            if not(location in unique):
                unique.append(location)
                print(location)


def merge_day_list(list1,list2):
    """
    list1 and list2 are lists of COVID_day classes. list1 is small, and list2 is the 
    'master' list. Merge list1 into list2 at its chronoligcal location by date. Return
    list2.
    """
    for day1 in list1:
        for i,day2 in enumerate(list2):
            if day1.date_obj < day2.date_obj:
                list2.insert(i,day1)
                # we need to break to avoid an infinite loop
                break

    return list2


# ==================================================

covid_data_pre = parse_html('pre',soup)
covid_data_p = parse_html('p',soup) # October 19th & 23rd
covid_data = merge_day_list(covid_data_p,covid_data_pre)

print_cases(covid_data,1)
print_unique_locations(covid_data)

"""
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
    date_list.append(day.date_obj)
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