
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
from matplotlib import gridspec
import numpy as np
from covid_classes import COVID_Day


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



def get_locations(covid_data,total_num_cases,print_flag=False):
    """
    
    """

    # create dictionary
    unique_locations = {}
    for day in covid_data:
        for location in day.location_list:
            if not(location in unique_locations):
                unique_locations[location] = 1
            else:
                unique_locations[location] += 1
       
    # make two lists (for plotting purposes)
    location_list = []
    location_count_list = []
    for location,count in unique_locations.items():
        location_list.append(location)
        location_count_list.append(count)

    # sort the lists by descending order
    zipped_lists = zip(location_count_list,location_list)
    sorted_pairs = sorted(zipped_lists,reverse=True)
    tuples = zip(*sorted_pairs)
    location_count_list,location_list = [list (tuple) for tuple in tuples]

    # raise error if the number of cases don't match
    if sum(location_count_list) != (total_num_cases-87):
        raise Exception("Total number of cases does not match")

    # compute percentage for each location
    location_shares = []
    for i,count in enumerate(location_count_list):
        location_share = (count/sum(location_count_list))*100
        location_shares.append(location_share)

    # print to console if print_flag is True
    if print_flag:
        for i,location in enumerate(location_list):
            # Quonset Point: 120/396 (30.3 %)
            print(f"{location_list[i]}: ",end="") # Quonset Point: 
            print(f"{location_count_list[i]}/{sum(location_count_list)}",end="") # 120/396
            print(f" ({round(location_shares[i],2)} %)") # (30.3 %)

    return location_list, location_count_list, location_shares



def get_running_totals(covid_data):
    """

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

    return date_list, cases_per_day_list, running_total_list



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

# print_cases(covid_data,1)
date_list, cases_per_day_list, running_total_list = get_running_totals(covid_data)
loc_list, loc_count_list, loc_shares = get_locations(covid_data,running_total_list[-1],True)







fig = plt.figure(figsize=(10,7))
# fig,ax = plt.subplots(2,2,figsize=(10,7))
spec = gridspec.GridSpec(ncols=2,nrows=2,width_ratios=[2,1])

fig.suptitle("COVID Cases at Electric Boat")

ax0 = fig.add_subplot(spec[0,0])
ax0.plot(date_list,cases_per_day_list,marker="o")
ax0.set_ylabel("Cases Per Day")

ax1 = fig.add_subplot(spec[1,0])
ax1.plot(date_list,running_total_list,marker="o")
ax1.set_ylabel("Running Total")

ax2 = fig.add_subplot(spec[0,1])
ax2.pie(loc_shares,labels=loc_list)
# ax2.legend(labels=loc_list,loc='center right')

plt.xticks(rotation=45)
plt.gcf().autofmt_xdate()

plt.show()
