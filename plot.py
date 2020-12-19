import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import gridspec
import math
from datetime import datetime as dt
from log import logger_setup

logger = logger_setup("plot_data.py")


def set_y_tick_range(y_data,interval):
  """
  Define a range (list) of points for the y-axis ticks.
  """
  upper_y_limit = math.ceil(max(y_data)/interval)*interval
  y_ticks = range(0,upper_y_limit+interval,interval)
  
  return y_ticks


def plot(dates,
         cases_per_day,
         N_day_avg,
         cases_per_day_avg,
         running_totals, 
         top_N_facilities,
         count_per_top_N_facility,
         top_N_depts,
         count_per_top_N_depts):

    fig = plt.figure(figsize=(10,7))
    spec = gridspec.GridSpec(ncols=2,nrows=2,width_ratios=[2,1])

    today = dt.today()
    fig_title = "Number of COVID Cases at Electric Boat as of "\
                + today.strftime("%B %d, %Y") + ": " + str(running_totals[-1])
    fig.suptitle(fig_title)

    # plot cases per day and running average
    ax0 = fig.add_subplot(spec[0,0])
    ax0.plot(dates,cases_per_day,marker='o')
    ax0.plot(dates,cases_per_day_avg,color='r')
    ax0.set_ylabel("Cases Per Day")
    ax0.set_yticks(set_y_tick_range(cases_per_day,10))
    ax0.grid(which='major',axis='y')
    ax0.legend(["Cases per Day",f"{N_day_avg}-Day Running Average"])
    logger.info("plot cases per day")

    # plot running total
    ax1 = fig.add_subplot(spec[1,0])
    ax1.plot(dates,running_totals,marker="o")
    ax1.set_ylabel("Running Total")
    ax1.set_yticks(set_y_tick_range(running_totals,100))
    ax1.grid(which='major',axis='y')
    logger.info("plot running total")

    # plot cases by facility as a pie chart
    ax2 = fig.add_subplot(spec[0,1])
    ax2.pie(count_per_top_N_facility,labels=top_N_facilities)
    logger.info("plot cases per facility pie chart")

    # plot cases by department as pie chart
    ax3 = fig.add_subplot(spec[1,1])
    ax3.pie(count_per_top_N_depts,labels=top_N_depts)
    logger.info("plot cases per dept pie chart")

    plt.xticks(rotation=45)
    plt.gcf().autofmt_xdate()

    plt.show()