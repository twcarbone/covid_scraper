
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
from postgres_db import *
from debug import print_cases


url = 'https://eblanding.com/covid-19-case-report-summary/'
soup = get_soup(url,print_flag=False)

covid_data_pre = parse_html('pre',soup)
covid_data_p = parse_html('p',soup) # October 19th & 23rd

covid_data = merge_day_list(covid_data_p,covid_data_pre)

# print_cases(covid_data,1)

dates,daily_totals = get_daily_totals(covid_data,print_flag=False)

daily_running = get_running_totals(covid_data,print_flag=False)

facilities,facility_counts,facility_shares = bucketize_cases(covid_data,'facility',False)
depts,dept_counts,dept_shares = bucketize_cases(covid_data,'dept',False)

top_facilities,top_facility_shares = get_top_shares(facilities,facility_shares,6,False)
top_depts,top_dept_shares = get_top_shares(depts,dept_shares,50,False)

"""
conn = connect_to_psql_db("eb_covid")
for case in covid_data:
  add_case_to_db(conn,case.case_num,case.date_str,case.facility,case.dept)

conn.close()
"""


plot(dates,daily_totals,daily_running,
     top_facilities,top_facility_shares,
     top_depts,top_dept_shares)

