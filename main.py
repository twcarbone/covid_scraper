
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

    option      1: 'case_num -- location'
                2: 'date -- case_num_list'
                3: 'short'
                4: 'long'
    """
    for case in covid_data:
        # 
        if option == 1:
            print(f"{case.case_num}:\t{case.location}")

        #
        elif option == 2:
            print(f"{case.date_str} ({case.date_obj}) -- ",end="")

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

# ==================================================

soup = get_soup('https://eblanding.com/covid-19-case-report-summary/')
covid_data_pre = parse_html('pre',soup)
covid_data_p = parse_html('p',soup) # October 19th & 23rd

covid_data = merge_day_list(covid_data_p,covid_data_pre)

print_cases(covid_data,1)

daily_totals = get_daily_totals(covid_data,print_flag=True)

"""
loc_list, loc_count_list, loc_shares = get_locations(covid_data,running_total_list[-1],False)

top_locations,top_shares = get_top_locations(loc_list,loc_shares,6,False)

# plot(date_list,cases_per_day_list,running_total_list,top_locations,top_shares)
"""






