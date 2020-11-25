import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import gridspec
import numpy as np


def plot(DATES, CASES_PER_DAY, RUNNING_TOTALS, LOCATIONS,SHARES):

    fig = plt.figure(figsize=(10,7))
    # fig,ax = plt.subplots(2,2,figsize=(10,7))
    spec = gridspec.GridSpec(ncols=2,nrows=2,width_ratios=[2,1])

    fig.suptitle("COVID Cases at Electric Boat")

    ax0 = fig.add_subplot(spec[0,0])
    ax0.plot(DATES,CASES_PER_DAY,marker="o")
    ax0.set_ylabel("Cases Per Day")

    ax1 = fig.add_subplot(spec[1,0])
    ax1.plot(DATES,RUNNING_TOTALS,marker="o")
    ax1.set_ylabel("Running Total")

    ax2 = fig.add_subplot(spec[0,1])
    ax2.pie(SHARES,labels=LOCATIONS)
    
    plt.xticks(rotation=45)
    plt.gcf().autofmt_xdate()

    plt.show()