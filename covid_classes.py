
from datetime import datetime

class COVID_Day:
    """
    A template for one day's worth of cases, including the date, list of cases, running 
    total, etc.

    self.date_str           'October 23, 2020'
    self.date_obj           '2020-10-23 00:00:00'
    self.case_list          ['#95: Employee at ... ','#96: Employee at ... ']
    self.case_num_list      ['95','96']
    self.num_cases          14
    self.running_total      364
    """
    def __init__(self,date_str):
        self.date_str = date_str
        self.date_obj = datetime.strptime(self.date_str,'%B %d, %Y')
        self.case_list = []
        self.case_num_list = []
        self.location_list = []

    def add_case(self,case):


        self.case_list.insert(0,case)

        case_num = case[case.index("#")+1:case.index(":")]
        self.case_num_list.insert(0,case_num)

        def get_location(case):
            """
            Parse the first test portion of the entire case description. Some cases are 
            outliers, and are instead assigned by looking up in a dictionary. Location is
            assigned "___LocationFailed___" if the parser failed to assign a location.
            """
            location_corrections = {
                "88" : "Quonset Point",
                "89" : "Kings Bay",
                "90" : "Travel (Business)",
                "91" : "Quonset Point",
                "92" : "New London",
                "93" : "Travel (Personal)",
                "94" : "Quonset Point",
                "95" : "New London",
                "96" : "Groton",
                "97" : "Quonset Point",
                "98" : "Quonset Point",
                "100" : "Other",
                "104" : "NEO",
                "110" : "SUBASE",
                "111" : "Groton Airport",
                "120" : "SUBASE",
                "237" : "PNSY",
                "244" : "WEO",
                "258" : "SUBASE",
                "269" : "SUBASE",
                "278" : "PNSY",
                "292" : "PNSY"
            }

            location = "___LocationFailed___"
            try:
                location = case[case.index("from")+5:case.index(" facility")]
            except ValueError:
                # location = "__Failed__"
                for corrected_case_num,corrected_location in location_corrections.items():
                    if corrected_case_num == self.case_num_list[0]:
                        location = corrected_location
            
            try:
                location = location.replace("’","") # 89,99,275
            except ValueError:
                pass

            return location


        self.location_list.insert(0,get_location(case))

    def sum_cases(self):
        self.num_cases = len(self.case_list)

    def update_running_total(self,previous_total=87):
        # the online case counter started at case 88, so the previous total was 87
        self.running_total = self.num_cases + previous_total