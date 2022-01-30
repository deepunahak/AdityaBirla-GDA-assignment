"""
Description: Class that has the following attributes
            (BANK,IFSC,MICR  CODE,BRANCH,ADDRESS,STD CODE,CITY,DISTRICT,STATE)

Author: Deepu Ranjan Nahak
Created Date: 28-01-2022
"""


class Ifsc:
    def __init__(self, bank, ifsc, micr_code, branch, address, std_code, city, district, state):
        self.bank = bank
        self.ifsc = ifsc
        self.micr_code = micr_code
        self.branch = branch
        self.address = address
        self.std_code = std_code
        self.city = city
        self.district = district
        self.state = state
