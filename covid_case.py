from datetime import datetime

class covid_case:
    """
    A template for one covid case at EB.

    self.date_str           'October 23, 2020'
    self.date_obj           '2020-10-23 00:00:00'
    self.case_str           '#95: Employee at ... '
    self.case_num            95
    self.facility           'Quonset Point'
    self.dept               '971'
    """

    def __init__(self,date_str,case_str):
        self.date_str = date_str
        self.date_obj = datetime.strptime(self.date_str,'%B %d, %Y')
        self.case_str = case_str
        self.case_num = int(case_str[case_str.index("#")+1:case_str.index(":")])
        self.facility = get_facility(self.case_str, self.case_num)
        self.dept = get_dept(self.case_str)
        self.bldg = get_bldg(self.case_str)
        self.last_day = get_last_day(self.case_str, self.case_num)
        # self.last_day_obj = datetime.strptime(self.last_day,'%B %d, %Y')


def get_facility(case_str,case_num):
    """
    Parse the first test portion of the entire case description. Some cases are 
    outliers, and are instead assigned by looking up in a dictionary. facility is
    assigned "___FacilityFailed___" if the parser failed to assign a facility.
    """
    facility_corrections = {
        88 : "Quonset Point",
        89 : "Kings Bay",
        90 : "Travel (Business)",
        91 : "Quonset Point",
        92 : "New London",
        93 : "Travel (Personal)",
        94 : "Quonset Point",
        95 : "New London",
        96 : "Groton",
        97 : "Quonset Point",
        98 : "Quonset Point",
        100 : "Other",
        104 : "NEO",
        110 : "SUBASE",
        111 : "Groton Airport",
        120 : "SUBASE",
        237 : "PNSY",
        244 : "WEO",
        258 : "SUBASE",
        269 : "SUBASE",
        278 : "PNSY",
        292 : "PNSY"
    }

    facility = "___facilityFailed___"
    try:
        facility = case_str[case_str.index("from")+5:case_str.index(" facility")]
    except ValueError:
        pass
    
    try:
        facility = facility.replace("’","") # for 89,99,275
    except ValueError:
        pass

    for corrected_case_num,corrected_facility in facility_corrections.items():
        if corrected_case_num == case_num:
            facility = corrected_facility

    return facility



def get_dept(case_str):
    """

    """

    dept = "___DeptFailed___"
    try:
        dept = case_str[case_str.index("Dept.")+6:case_str.index("Dept.")+9]
    except ValueError:
        pass

    return dept



def get_bldg(case_str):
    """

    """
    bldg = "___BldgFailed___"
    try:
        bldg = case_str[case_str.index("Dept.")+11:case_str.index("last")-2]

        if bldg == "":
            bldg = "___NoBldg___"

    except ValueError:
        pass

    return bldg



def get_last_day(case_str,case_num):
    """

    """
    last_day_corrections = {
        95 : "N/A",
        98 : "N/A",
        109 : "N/A",
        117 : "N/A",
        127 : "N/A",
        137 : "N/A",
        139 : "N/A",
        140 : "N/A",
        142 : "N/A",
        165 : "N/A",
        186 : "N/A",
        202 : "N/A",
        216 : "N/A",
        221 : "N/A",
        235 : "N/A",
        239 : "N/A",
        331 : "N/A",
        700 : "December 3, 2020",
        798 : "N/A"
    }

    last_day = "___LastDayFailed___"
    try:
        last_day = case_str[case_str.index("last day of work")+20:
            case_str.index("and tested")-1]
        
        last_day += ", 2020"

    except ValueError:
        pass

    for corrected_case_num,corrected_last_day in last_day_corrections.items():
        if corrected_case_num == case_num:
            last_day = corrected_last_day

    if last_day != "N/A":
        try:
            last_day = datetime.strptime(last_day,'%B %d, %Y')
        except ValueError:
            print(f"Failed of case {case_num}: {last_day} is " 
                  + "not of the form 'Month Day, Year'")
    
    return last_day

