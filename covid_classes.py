from datetime import datetime

class covid_case:
    """
    A template for one covid case at EB.

    self.date_str           'October 23, 2020'
    self.date_obj           '2020-10-23 00:00:00'
    self.case_str           '#95: Employee at ... '
    self.case_num            95
    self.location           'Quonset Point'
    self.dept               '971'
    """

    def __init__(self,date_str,case_str):
        self.date_str = date_str
        self.date_obj = datetime.strptime(self.date_str,'%B %d, %Y')
        self.case_str = case_str
        self.case_num = int(case_str[case_str.index("#")+1:case_str.index(":")])
        self.location = get_location(self.case_str,self.case_num)
        self.dept = get_dept(self.case_str)


def get_location(case_str,case_num):
    """
    Parse the first test portion of the entire case description. Some cases are 
    outliers, and are instead assigned by looking up in a dictionary. Location is
    assigned "___LocationFailed___" if the parser failed to assign a location.
    """
    location_corrections = {
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

    location = "___LocationFailed___"
    try:
        location = case_str[case_str.index("from")+5:case_str.index(" facility")]
    except ValueError:
        for corrected_case_num,corrected_location in location_corrections.items():
            if corrected_case_num == case_num:
                location = corrected_location
    
    try:
        location = location.replace("’","") # 89,99,275
    except ValueError:
        pass

    return location



def get_dept(case_str):
    """

    """

    dept = "___DeptFailed___"
    try:
        dept = case_str[case_str.index("Dept.")+6:case_str.index("Dept.")+9]
    except ValueError:
        pass

    return dept