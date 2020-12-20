import statistics as stats
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import gridspec
import datetime


def merge_day_list(list1,list2):
    """
    list1 and list2 are lists of covid_case classes. list1 is small, and list2 is the
    'master' list. Merge list1 into list2 at its chronoligcal location by date.
    Return list2.
    """
    for case1 in list1:
        for i,case2 in enumerate(list2):
            if case1.case_num < case2.case_num:
                list2.insert(i,case1)
                # we need to break to avoid an infinite loop
                break

    return list2



def get_daily_totals(covid_data,print_flag=False):
    """
    Returns dictionary daily totals.

    daily_totals = {
        ...
        "November 23, 2020" : 22,
        "November 24, 2020" : 9,
        "November 25, 2020" : 13,
        ...
    }
    """

    # create an empty dictionary
    daily_totals = {}

    # for each case in the covid_data list, if the date associated with the case is
    # not in the dictionary already, add it; otherwise increment the daily total by 1
    for case in covid_data:
        if not(case.date_obj in daily_totals):
            daily_totals[case.date_obj] = 1
        else:
            daily_totals[case.date_obj] += 1
    
    # make 2 lists for plotting
    dates = []
    totals = []
    for date,total in daily_totals.items():
        dates.append(date)
        totals.append(total)

    if print_flag:
        print("-------------------------------------------")
        for date,total in daily_totals.items():
            print(f"{date}: {total}")

    return dates, totals



def get_running_totals(covid_data,print_flag=False):
    """

    """
    dates = []
    daily_running = []
    for i,case in enumerate(covid_data):
        if case == covid_data[0]:
            continue
        elif case == covid_data[-1]:
            # for the final case in the list
            dates.append(case.date_str)
            daily_running.append(case.case_num)
        elif case.date_str == covid_data[i-1].date_str:
            continue
        else:
            # if the iterator is on a new date, then the previous date was the last
            # date in a day, and its case number is the running total for that day.
            dates.append(covid_data[i-1].date_str)
            daily_running.append(covid_data[i-1].case_num)

    if print_flag:
        print("-------------------------------------------")
        for i,date in enumerate(dates):
            print(f"{date}: {daily_running[i]}")

    return daily_running



def fill_data(r_dates,daily_running):
    """
    1.  loop thru r_dates
    2.  if a date is skipped, insert an entry for that date in both r_dates and
        daily_running
    3.  fill the new entry in daily_running with lineraly interpolated value
    4.  complete for every missing date from r_dates[0] thru r_dates[-1]
    """
    pf = False # flag for printing to console

    r_dates_filled = []
    daily_running_filled = []

    for i in range(len(r_dates)):
        
        # begin by putting the current reported date onto the new list
        r_dates_filled.append(r_dates[i])
        daily_running_filled.append(daily_running[i])

        if r_dates[i] == r_dates[-1]:
            # catch the final case; do nothing
            pass
        else:
            # dt is the number of days between case i and case i+1
            dt = r_dates[i+1] - r_dates[i]
            dt = int(dt.days)

            # if there is no jump, then we are OK and move to the next report date
            if dt == 1:
                pass
            else:
                # this algorithm is a little complicated, so this is an example to
                # illustrate what it's doing
                #
                # pretend i is June 3, 2020 and i+1 is June 7, 2020
                # >>> dt = 4
                #
                # we want to linearally interpolate at integer days, so iterate on
                # range(1,dt), making [1,2,3]. the "x" range for interpolation are
                # [0,4]. the "y" values corresponding to 0 and 4 are the case totals
                # from June 3 and June 7. by interpolating on "x" equal to 1,2,3 we
                # get the total for June 4, June 5, and June 6
                for x in range(1,dt):
                    # incriment one day
                    r_dates_filled.append(r_dates[i]+datetime.timedelta(days=x))

                    # linearly interpolate
                    x_range = [0, dt]
                    y_range = daily_running[i], daily_running[i+1]
                    new_case = np.interp(x,x_range,y_range)
                    daily_running_filled.append(new_case)
    
    # test print
    if pf:
        for i in range(len(r_dates)):
            print(f"{r_dates[i]}: {daily_running[i]} -- "
                + f"{r_dates_filled[i]}: {daily_running_filled[i]}")

    return r_dates_filled, daily_running_filled



def fill_backwards(dates_corr, running_corr):
    """
    The EB landing covid tracker started tracking at case 88. This function
    extrapolates backwards and returns an array of dates and running totals going
    back to case 1. note that the script calculates a running total at each day, so
    fractional totals may arise.
    """

    # the cutoff date by which to calcualte the linear portion of the curve is
    # guessed-and-checked until an extrapolation curve is generated that projects
    # cases beginning to be recorded in approx. January 2020, which is when COVID
    # first started to impact the US.
    guess_date = "September 22, 2020"
    x1_o = 0
    x2_o = dates_corr.index(datetime.datetime.strptime(guess_date,'%B %d, %Y'))

    y1_o = running_corr[0]
    y2_o = running_corr[x2_o]

    # compute slope of the linear portion of the line
    m = (y2_o - y1_o) / (x2_o - x1_o)

    # work backwards from the start date, linearly decrimenting
    dates_corr_extrap_list = []
    running_corr_exrap_list = []
    y2 = y1_o
    for i in range(1,500):
        # calculate the case total one day previous
        #   m = (y2-y1)/(x2-x1)
        #   but, x2-x1 = 1 because we are decrimenting one day at a time
        #   so, y1 = y2 - m
        y1 = y2 - m

        if y1 > 0:
            dates_corr_extrap_list.insert(0,dates_corr[0]-datetime.timedelta(days=i))
            running_corr_exrap_list.insert(0,y1)
            y2 = y1
        else:
            break

    return dates_corr_extrap_list, running_corr_exrap_list



def bucketize_cases(covid_data,attr,print_flag=False):
    """
    Return three lists
    """

    # create dictionary
    unique_attrs = {}
    for case in covid_data:
        if not(getattr(case,attr) in unique_attrs):
            unique_attrs[getattr(case,attr)] = 1
        else:
            unique_attrs[getattr(case,attr)] += 1
       
    # make two lists (for plotting purposes)
    unique_attrs_list = []
    unique_attrs_count_list = []
    for attr,count in unique_attrs.items():
        unique_attrs_list.append(attr)
        unique_attrs_count_list.append(count)

    # sort the lists by descending order
    zipped_lists = zip(unique_attrs_count_list,unique_attrs_list)
    sorted_pairs = sorted(zipped_lists,reverse=True)
    tuples = zip(*sorted_pairs)
    unique_attrs_count_list,unique_attrs_list = [list (tuple) for tuple in tuples]

    # raise error if the number of cases don't match
    if sum(unique_attrs_count_list) != (covid_data[-1].case_num-87):
        raise Exception("Total number of cases does not match")

    # compute percentage for each location
    attr_shares = []
    for i,count in enumerate(unique_attrs_count_list):
        attr_share = (count/sum(unique_attrs_count_list))*100
        attr_shares.append(attr_share)

    # print to console if print_flag is True
    if print_flag:
        print("-------------------------------------------")
        for i,attr in enumerate(unique_attrs_list):
            # Quonset Point: 120/396 (30.3 %)
            print(f"{unique_attrs_list[i]}: ",end="") # Quonset Point: 
            print(f"{unique_attrs_count_list[i]}/" 
                  + f"{sum(unique_attrs_count_list)}",end="") # 120/396
            print(f" ({round(attr_shares[i],2)} %)") # (30.3 %)

    return unique_attrs_list, unique_attrs_count_list, attr_shares



def get_top_shares(attr_list,attr_shares,n,print_flag=False):
    """
    Determine the top n locations with COVID cases, and assign the rest to 'Other'.
    """
    top_attrs = attr_list[0:n-1]
    top_attrs.append("Other")

    top_shares = attr_shares[0:n-1]
    top_shares.append(round(sum(attr_shares[n:-1]),2))
    
    if print_flag:
        print("-------------------------------------------")
        for i,top_share in enumerate(top_shares):
            print(f"{top_attrs[i]}: {top_shares[i]} %")
    
    return top_attrs,top_shares



def get_running_average(data,n_day):
  """
  Returns a dict containing a list the same length as 'data' and the argument
  'n_day'. The first n-1 days are equal to the first n-1 entries from 'data'. All
  remaining data points are the n-day running average.

  Example: data = [5,8,1,6,9,4,5,6,6,2,8] n_day = 4

    data_running_avg = [5,8,1,?,?,?,...] index =  0 1 2 3 4 5 ...
                            ^
                            if i < n_days-1:  # (i.e., less than 3)
                              # don't compute the avg
                            else:
                              # get an n_day slice using [i-n_day+1:i]
  """
  data_running_avg = []
  for i,value in enumerate(data):
    if i < n_day-1:
      data_running_avg.append(value)
    else:
      data_slice = data[i-n_day+1:i]
      data_slice_avg = stats.mean(data_slice)
      data_running_avg.append(data_slice_avg)

  return data_running_avg



def fit_SIR(totals):
    """
    Fit a Susceptible, Infected, Recovered (SIR) curve to the data.

    Credit due to the following resource:
    <scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/>
    """

    pf = False

    def deriv(y, t, N, beta, gamma):
        """
        set up ODE.
        """
        (S, I, R) = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I

        return dSdt,dIdt,dRdt
    

    # zero-normalize the data
    totals_norm = [totals[n]-totals[0] for n in range(len(totals))]

    # make a list of time points (in days)
    t = range(0,400)

    # estimate total population, N
    N_rng = range(10000,15000,100)

    # estimate initial number of infected and recovered individuals, I_0, R_0
    I_0 = 1
    R_0 = 0

    # estimate contact rate, beta, and mean recovery rate, gamma (in 1/days)
    beta_rng = np.arange(0.13,0.21,0.01)
    gamma_rng = np.arange(0.09,0.21,0.01)

    if pf:
        # make plot
        fig = plt.figure(figsize=(9,5))
        x_min = 0
        x_max = 400
        y_min = 0
        y_max = 2000
        ax = fig.add_subplot()
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    # loop thru each population, beta, and gamma estimate
    best_low_delta = 99999
    for n in N_rng:

        # everyone else, S_0, is susceptible
        S_0 = n - I_0 - R_0

        # compile into tuple of initial conditions
        y_0 = (S_0, I_0, R_0)

        for b in beta_rng:
            for g in gamma_rng:

                # integrate the SIR equations over t
                # we only care about I
                ret = odeint(deriv, y_0, t, args=(n, b, g))
                foo, I, bar = ret.T

                # slice the modeled infection rate data to be equal to the lenght of
                # data we currently have
                I_slc = I[0:len(totals)]

                # compute a list of deltas between the actual data and the modeled
                # data, then compute its average
                abs_deltas = [abs(totals_norm[i]-I[i]) for i in range(len(I_slc))]
                low_delta = max(abs_deltas)
                
                # ax.plot(t,I)

                # compare the avg that was just calculated to the best avg that has
                # been calcualted for the entire run and assign new "winners", if
                # appropriate
                if low_delta < best_low_delta:
                    params = (n, b, g)
                    I_best = I
                    best_low_deltas = abs_deltas
                    best_low_delta = low_delta

    if pf:
        ax.plot(range(len(totals_norm)),totals_norm,marker="o",color='r')
        ax.plot(t,I_best,color='black')
        ax.legend(["Total cases","Projected SIR Infection Curve"])
        plt.show()

    return I_best, params

