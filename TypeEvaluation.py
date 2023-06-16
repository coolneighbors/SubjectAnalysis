"""
Created on Tuesday, May 16 2023

@author: Grady Robbins

This script analyzes total movement ratio of subjects separated by type. Useful for larger reviews, not for individual classification.

Can also specify specific subject IDs that should not be counted in results

"""

import numpy as np
import pandas as pd
import math
import re
import csv

Types = ['1','2','4','8','16'] # enter type values here

#load in files
ClassificationFile = r'Classifications.csv'
TargetFile = r'Targets.csv'

CoordinateData = np.loadtxt(TargetFile,delimiter=',',usecols=(0,1)).astype(float)
ClassificationText = open(ClassificationFile, "r")
TargetText = open(TargetFile, 'r')
#load in RA and DEC of subjects
RA = CoordinateData[:,0]
DEC = CoordinateData[:,1]

typeRA = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typeDEC = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typedata = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
#generate searchable patterns for each target by type
patterntype = {Types[0]:'"#Type"":""'+Types[0]+'"',Types[1]:'"#Type"":""'+Types[1]+'"',Types[2]:'"#Type"":""'+Types[2]+'"',Types[3]:'"#Type"":""'+Types[3]+'"',Types[4]:'"#Type"":""'+Types[4]+'"'}

#separate RA and DEC by type
for line in TargetText:
    linesplit = re.split(',',line)
    for i in range(5):
        if str(2**i)+'\n' in linesplit[2]:
            typeRA[str(2**i)].append(str(linesplit[0]))
            typeDEC[str(2**i)].append(str(linesplit[1]))

type_presence = 0
#read in data and search for specific type
final_counter = 0
bad_ID = [78412786,78412838,78517043,78517056,79925646,79925663,78412820,78517052,79925658] # these IDs should not be counted, as the targets are not verified
#separate data by type and remove bad IDs
ClassificationCounter = 0
for line in ClassificationText:
    ClassificationCounter += 1
    if re.search(patterntype[Types[0]], line):
        typedata[Types[0]].append(line)
    if re.search(patterntype[Types[1]], line):
        typedata[Types[1]].append(line)
    if re.search(patterntype[Types[2]], line):
        bad_ID_counter = 0
        for n in range(len(bad_ID)):
            if str(bad_ID[n]) in line:
                bad_ID_counter = 1
        if bad_ID_counter != 1:
            typedata[Types[2]].append(line)
    if re.search(patterntype[Types[3]], line):
        typedata[Types[3]].append(line)
    if re.search(patterntype[Types[4]], line):
        typedata[Types[4]].append(line)

move_count = {Types[0]:0,Types[1]:0,Types[2]:0,Types[3]:0,Types[4]:0}
nomove_count = {Types[0]:0,Types[1]:0,Types[2]:0,Types[3]:0,Types[4]:0}
#determine movement counts by type
for i in range(5):
    for l in range(len(typedata[str(2**i)])):
        if "Yes" in typedata[str(2**i)][l]:
            move_count[str(2**i)] +=1
        if "No" in typedata[str(2**i)][l]:
            nomove_count[str(2**i)] +=1
    for l in range(len(typedata[str(2**i)])):
        for k in range(len(RA)):
            if str(int(RA[k])) in typedata[str(2**i)][l] and str(int(DEC[k])) in typedata[str(2**i)][l]:
                final_counter +=1
                break
        for k in range(len(typeRA[str(2**i)])):
            if typeRA[str(2**i)][k] in typedata[str(2**i)][l] and typeDEC[str(2**i)][k] in typedata[str(2**i)][l]:
                type_presence +=1
                break
#print movement data and total counts
    print('there were',move_count[str(2**i)],'movement decisions and',nomove_count[str(2**i)],'nonmovement decisions on type',str(2**i),'targets, giving a movement ratio of', (move_count[str(2**i)])/(move_count[str(2**i)]+nomove_count[str(2**i)])*100, '%')

print('there are ',move_count[Types[0]]+move_count[Types[1]]+move_count[Types[2]]+move_count[Types[3]]+move_count[Types[4]]+nomove_count[Types[0]]+nomove_count[Types[1]]+nomove_count[Types[2]]+nomove_count[Types[3]]+nomove_count[Types[4]],'classifications counted and',ClassificationCounter,'total classifications.')
