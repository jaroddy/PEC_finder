# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 09:53:25 2021

@author: jarod
"""

import pandas as pd
from easygui import *

msg = "Enter PEC Range"
title = "Lower Ct Cutoff - Higher Ct Cutoff"
fieldNames = ["Lower Ct Cutoff","Higher Ct Cutoff","Date Cutoff - MM", "Date Cutoff - DD", "Date Cutoff - YYYY", "Time Report Filename"]
fieldValues = []  # we start with blanks for the values
fieldValues = multenterbox(msg,title, fieldNames)

timereport = pd.read_csv(str(fieldValues[5]),low_memory=False)

# make sure that none of the fields was left blank
while 1:
    if fieldValues == None: break
    errmsg = ""
    for i in range(len(fieldNames)):
      if fieldValues[i].strip() == "":
        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
    if errmsg == "": break # no problems found
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

pec_report = pd.DataFrame(columns=["Specimen ID", "Rack-Slot", "Date Entered", "N1", "N2", "RP"])

for x in range(len(timereport)):
    
    pec_report_temp = pd.DataFrame(index = [0], columns=["Specimen ID", "Rack-Slot", "Date Entered", "N1", "N2", "RP"])
    
    date = timereport["received_on"][x]
    
    slash_counter = 0
    
    for y in range(len(date)):
        
        temp_pos = date[y]
        
        if (date[y] == '/') and (len(date) == 15) and (slash_counter == 0):
            
            month = int(date[y-1])
            
            day = int(date[y+1:y+3])
            
            slash_counter = slash_counter + 1
            
        elif (date[y] == '/') and (len(date) == 16) and (slash_counter == 0):
            
            month = int(date[y-2:y-1])
            
            day = int(date[y+1:y+3])
            
            slash_counter = slash_counter + 1
            
        elif (int(y+1) == len(date)) and (slash_counter == 1) and (len(date) == 15):
            
            year = int(date[y-9:y-5])
            
        elif (int(y+1) == len(date)) and (slash_counter == 1) and (len(date) == 14):
            
            year = int(date[y-8:y-4])
    
    if timereport["RP"][x] == '?':
        
        continue
    
    elif (float(timereport["RP"][x]) >= float(fieldValues[0])) and (float(timereport["RP"][x]) <= float(fieldValues[1])) and (str(timereport["N1"][x]) == 'nan') and (str(timereport["N2"][x]) == 'nan') and (month >= int(fieldValues[2])) and (day >= int(fieldValues[3])) and (year >= int(fieldValues[4])):
        
        pec_report_temp["Specimen ID"][0] = timereport["specimen"][x]
        pec_report_temp["Rack-Slot"][0] = timereport["rack_slot"][x]
        pec_report_temp["Date Entered"][0] = timereport["collected_on"][x]
        pec_report_temp["N1"][0] = timereport["N1"][x]
        pec_report_temp["N2"][0] = timereport["N2"][x]
        pec_report_temp["RP"][0] = timereport["RP"][x]
        
        pec_report = pec_report.append(pec_report_temp)
    
    print("Sample " + str(timereport["specimen"][x]) + ", number " + str(x) + " checked!") 
        
pec_report.to_csv(str(fieldValues[5]) + "_report.csv", index=False)