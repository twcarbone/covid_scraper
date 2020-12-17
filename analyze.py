import statistics as stats
import numpy as np


def merge_day_list(list1,list2):
    """
    list1 and list2 are lists of covid_case classes. list1 is small, and list2 is the 
    'master' list. Merge list1 into list2 at its chronoligcal location by date. Return
    list2.
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

    # for each case in the covid_data list, if the date associated with the case is not in
    # the dictionary already, add it; otherwise increment the daily total by 1
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
            # if the iterator is on a new date, then the previous date was the last date in
            # a day, and its case number is the running total for that day.
            dates.append(covid_data[i-1].date_str)
            daily_running.append(covid_data[i-1].case_num)

    if print_flag:
        print("-------------------------------------------")
        for i,date in enumerate(dates):
            print(f"{date}: {daily_running[i]}")

    return daily_running



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
      data_running_avg.append(np.nan)
    else:
      data_slice = data[i-n_day+1:i]
      data_slice_avg = stats.mean(data_slice)
      data_running_avg.append(data_slice_avg)
  
  running_avg_dict = {
    "n_day" : n_day,
    "data_running_avg" : data_running_avg
  }

  return running_avg_dict

