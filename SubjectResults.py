"""
Created on Wednesday, May 17 2023

@author: Grady Robbins

A script to return specific subjects from Zooniverse classification file and target file which have movement above a specified threshold.

Returns target type CSVs with movement ratio, RA, DEC, and WiseView link titled as 'typexresults.csv' where x is type.
"""

import numpy as np
import re
import csv

#load in coordinates, classifications, and targets
ClassificationsFile = r'Classifications.csv'
TargetFile = r'Targets.csv'
coord_data = np.loadtxt(TargetFile,delimiter=',',usecols=(0,1)).astype(float)

Types = ['1','2','4','8','16']# define values for type of target, here 2^(0,1,2,3,4,5) used
acceptance_ratio = 0.0 # define minimum movement ratio for a target to be considered

#Find RA and DEC of desired subjects
RA = coord_data[:,0]
DEC = coord_data[:,1]
#Define dictionaries

typeRA = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typeDEC = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typeShortRA = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typeShortDEC = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
typedata = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}

def limit_RA_DEC(RA,DEC,CharacterCount):
    '''
    This function limits the RA and DEC values to be a certain amount of characters in length for subject matching.
    parameters:
    RA - list of DEC values, should be in degrees
    DEC - list of DEC values, should be in degrees
    CharacterCount - integer value of number of characters
    returns:
    --------------------------------
    ShortRA - shortened list of str RA values in degrees
    ShortDEC - shortened list of str DEC values in degrees
    '''
    for k in range(len(RA)):
        ShortRA = RA.copy()
        ShortDEC = DEC.copy()
        RAlist = [*str(RA[k])]
        DEClist = [*str(DEC[k])]
        ShortRA[k] = ''.join(RAlist[0:CharacterCount])
        ShortDEC[k] = ''.join(DEClist[0:CharacterCount])
    return ShortRA,ShortDEC

#separate RA and DEC by target type
text_filecoord = open(TargetFile,'r')
for line in text_filecoord:
    linesplit = re.split(',',line)
    for i in Types:
        if i+'\n' in linesplit[2]:
            typeRA[i].append(str(linesplit[0]))
            typeDEC[i].append(str(linesplit[1]))

type_presence = 0
#define patterns by type
patterntype = {Types[0]:'"#Type"":""'+Types[0]+'"',Types[1]:'"#Type"":""'+Types[1]+'"',Types[2]:'"#Type"":""'+Types[2]+'"',Types[3]:'"#Type"":""'+Types[3]+'"',Types[4]:'"#Type"":""'+Types[4]+'"'}
#separate data by type and remove bad IDs
final_counter = 0
bad_ID = [78412786,78412838,78517043,78517056,79925646,79925663,78412820,78517052,79925658] # these IDs should not be counted, as the targets are not verified
classificationsFile = open(ClassificationsFile, 'r')
k=-1
#get all data for each type and separate them in dictionaries
for line in classificationsFile:
    if re.search(patterntype[Types[0]], line):
        k+=1
        typedata[Types[0]].append(line)
    if re.search(patterntype[Types[1]], line):
        typedata[Types[1]].append(line)
    if re.search(patterntype[Types[2]], line):
        p = 0
        for n in range(len(bad_ID)):
            if str(bad_ID[n]) in line:
                p = 1
        if p != 1:
            typedata[Types[2]].append(line)
    if re.search(patterntype[Types[3]], line):
        typedata[Types[3]].append(line)
    if re.search(patterntype[Types[4]], line):
        typedata[Types[4]].append(line)

#calculate RA,DEC,link, and accuracy per target by type and write on csv
RA_csv = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
DEC_csv ={Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
link_csv = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
count_csv = {Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}
totalcount_csv ={Types[0]:[],Types[1]:[],Types[2]:[],Types[3]:[],Types[4]:[]}

for i in Types: #repeat for each data type
    typeShortRA[i],typeShortDEC[i] = limit_RA_DEC(typeRA[i],typeDEC[i],6) #shorten RA and DEC to search correctly
    for n in range(len(typeShortRA[i])): #iterate through each RA and DEC in the classifications file and separate by movement values
        move_values = 0
        total_values = 0
        for k in range(len(typedata[i])):
            if '""RA"":""'+str(typeShortRA[i][n]) in typedata[i][k]:
                if '""DEC"":""'+str(typeShortDEC[i][n]) in typedata[i][k]:
                    total_values +=1
                    if 'Yes' in typedata[i][k]:
                        move_values +=1
                        data_temp = typedata[i][k]
        if total_values != 0: # remove division error
            if move_values/total_values >= acceptance_ratio: # only keep subjects which are above a specified threshold
                totalcount_csv[i].append(int(total_values))
                count_csv[i].append(int(move_values))
                value_list = re.split(',',data_temp)
                for l in value_list:
                    if 'byw' in l: # generate full RA,DEC, and link for each accepted target
                        RA_csv[i].append(typeRA[i][n])
                        DEC_csv[i].append(typeDEC[i][n])
                        link_csv[i].append('http://byw.tools/wiseview#ra='+typeRA[i][n]+'&dec='+typeDEC[i][n]+'&size=176&band=3&speed=20&minbright=-50.0000&maxbright=500.0000&window=0.5&diff_window=1&linear=1&color=&zoom=9&border=0&gaia=1&invert=1&maxdyr=0&scandir=0&neowise=0&diff=0&outer_epochs=0&unique_window=1&smooth_scan=0&shift=0&pmra=0&pmdec=0&synth_a=0&synth_a_sub=0&synth_a_ra=&synth_a_dec=&synth_a_w1=&synth_a_w2=&synth_a_pmra=0&synth_a_pmdec=0&synth_a_mjd=&synth_b=0&synth_b_sub=0&synth_b_ra=&synth_b_dec=&synth_b_w1=&synth_b_w2=&synth_b_pmra=0&synth_b_pmdec=0&synth_b_mjd=')
    #write on files labeled 'typexresults.csv' (x) is type
    with open(r'type'+str(i)+'results.csv','w', newline = '') as file:
        writer = csv.writer(file)
        for k in range(len(link_csv[i])):
            writer.writerow([(count_csv[i][k])/(totalcount_csv[i][k]),RA_csv[i][k],DEC_csv[i][k],link_csv[i][k]])
