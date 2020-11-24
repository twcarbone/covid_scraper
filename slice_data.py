def get_locations(covid_data,total_num_cases,print_flag=False):
    """
    
    """

    # create dictionary
    unique_locations = {}
    for day in covid_data:
        for location in day.location_list:
            if not(location in unique_locations):
                unique_locations[location] = 1
            else:
                unique_locations[location] += 1
       
    # make two lists (for plotting purposes)
    location_list = []
    location_count_list = []
    for location,count in unique_locations.items():
        location_list.append(location)
        location_count_list.append(count)

    # sort the lists by descending order
    zipped_lists = zip(location_count_list,location_list)
    sorted_pairs = sorted(zipped_lists,reverse=True)
    tuples = zip(*sorted_pairs)
    location_count_list,location_list = [list (tuple) for tuple in tuples]

    # raise error if the number of cases don't match
    if sum(location_count_list) != (total_num_cases-87):
        raise Exception("Total number of cases does not match")

    # compute percentage for each location
    location_shares = []
    for i,count in enumerate(location_count_list):
        location_share = (count/sum(location_count_list))*100
        location_shares.append(location_share)

    # print to console if print_flag is True
    if print_flag:
        for i,location in enumerate(location_list):
            # Quonset Point: 120/396 (30.3 %)
            print(f"{location_list[i]}: ",end="") # Quonset Point: 
            print(f"{location_count_list[i]}/{sum(location_count_list)}",end="") # 120/396
            print(f" ({round(location_shares[i],2)} %)") # (30.3 %)

    return location_list, location_count_list, location_shares



def get_running_totals(covid_data):
    """

    """

    date_list = []
    cases_per_day_list = []
    running_total_list = []
    for i,day in enumerate(covid_data):

        if day == covid_data[0]:
            # if it is the first day of data, then there is no previous day and the method
            # defaults to adding 87 to the current day's case count
            day.update_running_total()
        else:
            # otherwise, add the running total from the previous day to today's case count
            day.update_running_total(covid_data[i-1].running_total)

        # make lists for plotting purposes
        date_list.append(day.date_obj)
        cases_per_day_list.append(day.num_cases)
        running_total_list.append(day.running_total)

    return date_list, cases_per_day_list, running_total_list



def merge_day_list(list1,list2):
    """
    list1 and list2 are lists of COVID_day classes. list1 is small, and list2 is the 
    'master' list. Merge list1 into list2 at its chronoligcal location by date. Return
    list2.
    """
    for day1 in list1:
        for i,day2 in enumerate(list2):
            if day1.date_obj < day2.date_obj:
                list2.insert(i,day1)
                # we need to break to avoid an infinite loop
                break

    return list2