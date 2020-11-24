


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

    """

    # create an empty dictionary
    daily_totals = {}

    # for each case in the covid_data list, if the date associated with the case is not in
    # the dictionary already, add it; otherwise increment the daily total by 1
    for case in covid_data:
        if not(case.date_str in daily_totals):
            daily_totals[case.date_str] = 1
        else:
            daily_totals[case.date_str] += 1

    if print_flag:
        for date,total in daily_totals.items():
            print(f"{date}: {total}")

    return daily_totals



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



def get_top_locations(location_list,location_shares,n,print_flag=False):
    """
    Determine the top n locations with COVID cases, and assign the rest to 'Other'.
    """
    top_locations = location_list[0:n-1]
    top_locations.append("Other")

    top_shares = location_shares[0:n-1]
    top_shares.append(round(sum(location_shares[n:-1]),2))
    
    if print_flag:
        for i,top_share in enumerate(top_shares):
            print(f"{top_locations[i]}: {top_shares[i]} %")
    
    return top_locations,top_shares





