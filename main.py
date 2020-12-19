
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


from scrape import *
from analyze import *
from plot import *
from db import *
from debug import print_cases
from log import logger_setup
from all_covid_data import all_covid_data

logger = logger_setup("main.py")


logger.info("*************** begin script ***************")

# create soup object from html
url = 'https://eblanding.com/covid-19-case-report-summary/'
soup = get_soup(url,print_flag=False)
logger.info('create soup object from html')

# parse all <pre> html tags
covid_data_pre = parse_html('pre',soup)
logger.info("parse all <pre> html tags")

# parse all <p> html tags
covid_data_p = parse_html('p',soup) # October 19th & 23rd
logger.info("parse all <p> html tags")

# merge <pre> and <p> lists
covid_data = merge_day_list(covid_data_p,covid_data_pre)
logger.info("merge <pre> and <p> lists")

# print_cases(covid_data,3)

all_covid_data = all_covid_data(covid_data)

"""
conn = connect_to_psql_db("eb_covid")
for case in covid_data:
  add_case_to_db(conn,case.case_num,case.date_str,case.facility,case.dept)

conn.close()
"""

# plot the data
plot(all_covid_data.report_date_list,
     all_covid_data.daily_total_list,
     all_covid_data.N_day_avg,
     all_covid_data.N_day_running_avg,
     all_covid_data.running_total_list, 
     all_covid_data.top_N_facility_list,
     all_covid_data.count_per_top_N_facility,
     all_covid_data.top_N_dept_list,
     all_covid_data.count_per_top_N_dept)
logger.info("plot the data")

logger.info("*************** end script ***************")