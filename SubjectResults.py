"""
Created on Wednesday, May 17 2023

@author: Grady Robbins

A script to find subjects from Zooniverse classification file and target file which have movement above a specified threshold.

Returns target type CSVs with movement ratio, RA, DEC, Zooniverse subject link, and WiseView link titled as 'typexresults.csv' where x is type.
"""

import numpy as np
import pandas as pd
import math
import re
import csv
import copy
from alive_progress import alive_bar; import time

#load in coordinates, classifications, and targets
ClassificationsFile = r'Launch_Classifications6_29_23.csv'

Types = ['1','4','8','16','32']#define values for type of target, here 2^(0,1,2,3,4,5) used
acceptance_threshold = 4 # define minimum number of movement votes for a target to be recorded

#Define dictionaries

CoordinateMovement = {Types[0]:{'RA': [], 'DEC': [], 'zoolink': [], 'bywlink': [], 'movement': [], 'total': []},
                      Types[1]:{'RA': [], 'DEC': [], 'zoolink': [], 'bywlink': [], 'movement': [], 'total': []},
                      Types[2]:{'RA': [], 'DEC': [], 'zoolink': [], 'bywlink': [], 'movement': [], 'total': []},
                      Types[3]:{'RA': [], 'DEC': [], 'zoolink': [], 'bywlink': [], 'movement': [], 'total': []},
                      Types[4]:{'RA': [], 'DEC': [], 'zoolink': [], 'bywlink': [], 'movement': [], 'total': []}}

def returnfloat(string):
    number = []
    for i in (string):
        if i.isdigit() or i == '.' or i == '-':
            number.append(i)
    return float(''.join(number))

#separate data by type and remove bad IDs

bad_ID = [] # these IDs should not be counted, as the targets are not verified
ClassificationText = open(ClassificationsFile, 'r')

ClassificationCounter = -1
#get all data for each type and separate them in dictionaries
for line in ClassificationText:
    ClassificationCounter +=1
count=-1
ClassificationText = open(ClassificationsFile, 'r')
with alive_bar(ClassificationCounter) as bar:
    for line in ClassificationText:
        bar()
        count += 1
        if count == 0:
            continue
        itemlist = re.split(',',line)
        for item in itemlist:
            if 'RA"":' in item:
                RA = returnfloat(item)
            if 'DEC"":' in item:
                DEC = returnfloat(item)
            if '#BITMASK"":' in item:
                Type = str(int(returnfloat(item)))
            if '""ID"":""' in item:
                ID = str(int(returnfloat(item)))
                if ID in bad_ID:
                    continue
        if str(RA) in CoordinateMovement[Type]['RA'] and str(DEC) in CoordinateMovement[Type]['DEC']:
            for i in range(len(CoordinateMovement[Type]['RA'])):
                if RA == CoordinateMovement[Type]['RA']:
                    RA_index = i
        else:
            bywlink = ('http://byw.tools/wiseview#ra='+str(RA)+'&dec='+str(DEC)+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=1&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
            zoolink = ('https://www.zooniverse.org/projects/coolneighbors/backyard-worlds-cool-neighbors/talk/subjects/'+str(ID))
            CoordinateMovement[Type]['RA'].append(str(RA))
            CoordinateMovement[Type]['DEC'].append(str(DEC))
            CoordinateMovement[Type]['bywlink'].append(bywlink)
            CoordinateMovement[Type]['zoolink'].append(zoolink)
            CoordinateMovement[Type]['movement'].append(0)
            CoordinateMovement[Type]['total'].append(0)
            RA_index = -1
        if '"Yes"' in line:
            CoordinateMovement[Type]['movement'][RA_index] += 1
            CoordinateMovement[Type]['total'][RA_index] += 1
        if '"No"' in line:
            CoordinateMovement[Type]['total'][RA_index] += 1
        
for i in Types:
    with open(r'type'+str(i)+'results.csv','w', newline = '') as file:
        writer = csv.writer(file)
        for k in range(len(CoordinateMovement[i]['bywlink'])):
            if CoordinateMovement[i]['total'][k] != 0:
                if CoordinateMovement[i]['movement'][k] >= acceptance_threshold:
                    writer.writerow([(CoordinateMovement[i]['movement'][k])/(CoordinateMovement[i]['total'][k]),CoordinateMovement[i]['RA'][k],CoordinateMovement[i]['DEC'][k],CoordinateMovement[Type]['zoolink'][k],CoordinateMovement[i]['bywlink'][k]])
