
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


from get_web_data import *
from slice_data import *
from plot_data import *


def print_cases(covid_data,option):
    """
    Helper function for testing.

    """
    for case in covid_data:
        # 393: Groton
        if option == 1:
            print(f"{case.case_num}:\t{case.location}")

       
        # # October 23, 2020 (2020-10-23 00:00:00) -- []
        # elif option == 2:
        #     print(f"{case.date_str} ({case.date_obj}) -- ",end="")

        #     for case_num in day.case_num_list:
        #         if case_num == day.case_num_list[-1]:
        #             print(case_num)
        #         else:
        #             print(f"{case_num}, ",end="")
       

        # 
        elif option == 3:
             print(f"{case.case_str[0:75]} -- {case.dept}")

        # 
        elif option == 4:
            print(case.case_str)

        # 
        elif option == 5:
            print(F"{case.case_num}:\t{case.dept}")

# ==================================================

soup = get_soup('https://eblanding.com/covid-19-case-report-summary/')
covid_data_pre = parse_html('pre',soup)
covid_data_p = parse_html('p',soup) # October 19th & 23rd

covid_data = merge_day_list(covid_data_p,covid_data_pre)

print_cases(covid_data,3)

dates,daily_totals = get_daily_totals(covid_data,print_flag=False)

daily_running = get_running_totals(covid_data,print_flag=False)

locations,location_counts,location_shares = get_locations(covid_data,print_flag=False)

top_locations,top_shares = get_top_locations(locations,location_shares,6,False)

# plot(dates,daily_totals,daily_running,top_locations,top_shares)

