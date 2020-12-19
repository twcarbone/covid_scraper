
import scrape
import analyze as az
from plot import plot
import db as db
from debug import print_cases
from log import logger_setup
from all_covid_data import all_covid_data

logger = logger_setup("main.py")

logger.info("*************** begin script ***************")

# create soup object from html
url = 'https://eblanding.com/covid-19-case-report-summary/'
soup = scrape.get_soup(url,print_flag=False)
logger.info('create soup object from html')

# parse all <pre> html tags
covid_data_pre = scrape.parse_html('pre',soup)
logger.info("parse all <pre> html tags")

# parse all <p> html tags
covid_data_p = scrape.parse_html('p',soup) # October 19th & 23rd
logger.info("parse all <p> html tags")

# merge <pre> and <p> lists
covid_data = az.merge_day_list(covid_data_p,covid_data_pre)
logger.info("merge <pre> and <p> lists")

# print_cases(covid_data,3)

# orgnaize summary data into class
all_covid_data = all_covid_data(covid_data)

"""
conn = db.connect_to_psql_db("eb_covid")
for case in covid_data:
  db.add_case_to_db(conn,case.case_num,case.date_str,case.facility,case.dept)

conn.close()
"""
az.fit_SIR(all_covid_data.report_date_list,
           all_covid_data.running_total_list)

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
"""
logger.info("*************** end script ***************")