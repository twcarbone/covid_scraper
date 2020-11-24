def plot(date_list,cases_per_day_list,loc_shares):

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