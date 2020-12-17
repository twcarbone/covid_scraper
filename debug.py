def print_cases(covid_data,option):
    """
    Helper function for testing.

    """
    for i,case in enumerate(covid_data):

        if option == 1:
            """
            556: New London
            557: Groton
            558: Kings Highway
            559: Groton
            """
            print(f"{case.case_num}:\t{case.facility}")
     

        if option == 2:
            """
            November 12, 2020 -- 318,319,320, ... ,346
            November 13, 2020 -- 347,348,349, ... ,360
            November 15, 2020 -- 361,362,363, ... ,370
            """
            if case == covid_data[0]:
                print(f"{case.date_str} -- {case.case_num},",end="")
            elif case == covid_data[-1]:
                print(case.case_num)
            else:
                if covid_data[i].date_str == covid_data[i-1].date_str:
                    print(f"{case.case_num},",end="")
                else:
                    print(f"\n{case.date_str} -- {case.case_num},",end="")



        elif option == 3:
            """

            """
            print(f"{case.case_num} : {case.bldg}")


        elif option == 4:
            """
            
            """
            print(case.case_str)


        elif option == 5:
            """
            
            """
            print(F"{case.case_num}:\t{case.dept}")

