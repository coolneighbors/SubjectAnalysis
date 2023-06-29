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
from alive_progress import alive_bar; import time

Types = ['1','4','8','16','32'] # enter type values here

#load in file
ClassificationFile = r'Classifications_File'

ClassificationText = open(ClassificationFile, "r")


typeRA = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typeDEC = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typedata = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}

#generate searchable patterns for each target by type
patterntype = {Types[0]:'#BITMASK"":""'+Types[0]+'"',Types[1]:'"#BITMASK"":""'+Types[1]+'"',Types[2]:'"#BITMASK"":""'+Types[2]+'"',Types[3]:'"#BITMASK"":""'+Types[3]+'"',Types[4]:'"#BITMASK"":""'+Types[4]+'"'}

#read in data and search for specific type

ClassificationCounter = -1
move_count = {Types[0]:0,Types[1]:0,Types[2]:0,Types[3]:0,Types[4]:0}
nomove_count = {Types[0]:0,Types[1]:0,Types[2]:0,Types[3]:0,Types[4]:0}

for line in ClassificationText:
    ClassificationCounter +=1
with alive_bar(ClassificationCounter*len(Types)) as bar:
    for i in Types:
        ClassificationText = open(ClassificationFile,'r')
        for line in ClassificationText:
            time.sleep(.00001)
            bar()
            if re.search(patterntype[i], line):
                if "Yes" in line:
                    move_count[i] +=1
                elif "No" in line:
                    nomove_count[i] +=1
        ClassificationText.close()
        print('there were',move_count[i],'movement decisions and',nomove_count[i],'nonmovement decisions on type',i,'targets, giving a movement ratio of', (move_count[i])/(move_count[i]+nomove_count[i])*100, '%')

print('Classifications Read')

print('there are ',move_count[Types[0]]+move_count[Types[1]]+move_count[Types[2]]+move_count[Types[3]]+move_count[Types[4]]+nomove_count[Types[0]]+nomove_count[Types[1]]+nomove_count[Types[2]]+nomove_count[Types[3]]+nomove_count[Types[4]],'classifications counted and',ClassificationCounter,'total classifications.')
