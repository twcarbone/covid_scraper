import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import gridspec
import math
from log import logger_setup

logger = logger_setup("plot_data.py")


def set_y_tick_range(y_data,interval):
  """
  Define a range (list) of points for the y-axis ticks.
  """
  upper_y_limit = math.ceil(max(y_data)/interval)*interval
  y_ticks = range(0,upper_y_limit+interval,interval)
  
  return y_ticks


def plot(DATES, CASES_PER_DAY, CASES_PER_DAY_AVG_DICT, 
        RUNNING_TOTALS, 
        FACILITIES,LOC_SHARES,
        DEPTS,DEPT_SHARES):

    # deconstruct dictionary of running average info
    CASES_PER_DAY_AVG = CASES_PER_DAY_AVG_DICT["data_running_avg"]
    N_DAY_AVG = CASES_PER_DAY_AVG_DICT["n_day"]

    fig = plt.figure(figsize=(10,7))
    # fig,ax = plt.subplots(2,2,figsize=(10,7))
    spec = gridspec.GridSpec(ncols=2,nrows=2,width_ratios=[2,1])

    fig.suptitle(f"Number of COVID Cases at Electric Boat: {RUNNING_TOTALS[-1]}")

    # plot cases per day
    ax0 = fig.add_subplot(spec[0,0])
    ax0.plot(DATES,CASES_PER_DAY,marker='o')
    ax0.plot(DATES,CASES_PER_DAY_AVG,color='r')
    ax0.set_ylabel("Cases Per Day")
    ax0.set_yticks(set_y_tick_range(CASES_PER_DAY,10))
    ax0.grid(which='major',axis='y')
    ax0.legend(["Cases per Day",f"{N_DAY_AVG}-Day Running Average"])
    logger.info("plot cases per day")

    # plot running total
    ax1 = fig.add_subplot(spec[1,0])
    ax1.plot(DATES,RUNNING_TOTALS,marker="o")
    ax1.set_ylabel("Running Total")
    ax1.set_yticks(set_y_tick_range(RUNNING_TOTALS,100))
    ax1.grid(which='major',axis='y')
    logger.info("plot running total")

    # plot cases per facility as a pie chart
    ax2 = fig.add_subplot(spec[0,1])
    ax2.pie(LOC_SHARES,labels=FACILITIES)
    logger.info("plot cases per facility pie chart")

    # plot cases by department as pie chart
    ax3 = fig.add_subplot(spec[1,1])
    ax3.pie(DEPT_SHARES,labels=DEPTS)
    logger.info("plot cases per dept pie chart")

    plt.xticks(rotation=45)
    plt.gcf().autofmt_xdate()

    plt.show()