''' 
June 16 2023 

@author: Grady Robbins

A script to determine if candidates are present in a subject set using a csv of IDs to check.

Subject ID is cross referenced with original subject set to find RA and DEC.

Then RA and DEC are searched for in the csv file. If present, the candidate information is returned.

'''

import csv
import re
import numpy as np

def limit_RA_DEC(RA,DEC,CharacterCount):
    '''
    This function limits the RA and DEC values to be x characters in length for subject matching.
    parameters:
    RA - list of float DEC values, should be in degrees
    DEC - list of float DEC values, should be in degrees
    returns:
    --------------------------------
    RA - shortened list of float RA values in degrees
    DEC - shortened list of float DEC values in degrees
    '''
    for k in range(len(RA)):
        RAlist = [*str(RA[k])]
        DEClist = [*str(DEC[k])]
        RA[k] = ''.join(RAlist[0:CharacterCount])
        DEC[k] = ''.join(DEClist[0:CharacterCount])
    return RA,DEC

def FindSubjectCoords(filename = str):
    '''
    This function finds the RA and DEC coordinates for all subjects in a subject csv file.

    Parameters:
    filename - path to subject csv file
    
    Returns:
    --------------------------------
    RA - list of str RA values in degrees
    DEC - list of str DEC values in degrees
    '''
    RA_subjects = []
    DEC_subjects = []
    with open(filename, 'r', newline='') as file: #load in file
        for line in file:
            line_list = re.split(',', line)
            for k in range(len(line_list)):# iterate each line and return RA and DEC for all subjects
                new_ra_list = []
                new_dec_list = []
                if '"RA"":""' in line_list[k]:
                    ra_temp_list = [*line_list[k]]
                    for l in range(len(ra_temp_list)):
                        if ra_temp_list[l].isnumeric() or ra_temp_list[l] == '.':
                            new_ra_list.append(ra_temp_list[l])
                    RA_subjects.append(''.join(new_ra_list))
                if '"DEC"":""' in line_list[k]:
                    dec_temp_list = [*line_list[k]]
                    for l in range(len(dec_temp_list)):
                        if dec_temp_list[l].isnumeric() or dec_temp_list[l] == '.':
                            new_dec_list.append(dec_temp_list[l])
                    DEC_subjects.append(''.join(new_dec_list))
    return RA_subjects, DEC_subjects

def FindTargetIDs(filename = str):
    '''
    This function finds target IDs for cross matching from csv containing only subject IDs
    
    Parameters:
    filename - path to candidate csv file
    
    Returns:
    --------------------------------
    target_IDs - a list of target IDs to match with a larger subject set
    '''
    target_IDs = []
    with open(filename, 'r') as file:
        for line in file:
            target_IDs.append(str(int(line)))
    return target_IDs

def FindCandidateCoords(larger_candidate_filename = str, target_IDs = list):
    '''
    This function grabs the RA and DEC coordinates for all candidates in a subject source csv file using subject ID.
    
    Parameters:
    larger_candidate_filename - path to larger candidate csv with all metadata
    candidate_IDs - a list of subject IDs to match with a larger subject set    
    Returns:
    --------------------------------
    RA - list of str RA values in degrees
    DEC - list of str DEC values in degrees
    '''
    RA = []
    DEC = []
    with open(larger_candidate_filename, 'r', newline='') as file:
            for line in file:
                line_list = re.split(',', line)
                for target_ID in target_IDs:
                    if target_ID == line_list[0]:
                        RA.append(line_list[1])
                        DEC.append(line_list[2])
    print(len(RA), 'candidates to check for presence')
    return RA, DEC

def MatchRADEC(RA_candidates,DEC_candidates, RA_subjects, DEC_subjects, target_IDs = None):
    '''
    This function matches the RA and DEC coordinates for all candidates to a larger subject set and prints the matching RA, DEC, and subject IDs.
    
    Parameters:
    RA_candidates - list of str RA values in degrees for smaller candidate set
    DEC_candidates - list of str DEC values in degrees for smaller candidate set
    RA_subjects - list of str RA values in degrees for larger subject set
    DEC_subjects - list of str DEC values in degrees for larger subject set
    target_IDs - a list of subject IDs to print in event of a match
    Returns:
    --------------------------------
    None
    '''
    cross_match = 0
    for k in range(len(RA_candidates)):
        if k in 500*np.arange(0,1001): #print progress
            print('step',k)
        for l in range(len(RA_subjects)): #iterate through subjects, if a subject is present in both files print subject data
            if RA_candidates[k] in RA_subjects[l] and DEC_candidates[k] in DEC_subjects[l]:
                if target_IDs is not None:
                    print('present RA, DEC, subject_ID:',RA_candidates[k],DEC_candidates[k],target_IDs[k])
                else:
                    print('present RA, DEC:',RA_candidates[k],DEC_candidates[k])
                cross_match +=1
    print(cross_match,'total matching IDs')

#use functions and change filenames
RAsubjects, DECsubjects = FindSubjectCoords(r'Subjects.csv') # Zooniverse subjects file
targetIDs = FindTargetIDs(r'CandidateIDs.csv') # list of the subject IDs to compare, can comment out if not needed
RAcandidates, DECcandidates = FindCandidateCoords(r'TargetFile.csv', targetIDs) # csv of all target (RA, DEC, target type), can delete targetIDs if needed

print(len(RAsubjects),'total subjects present')
print(len(RAcandidates),'total candidates present')

MatchRADEC(RAcandidates,DECcandidates, RAsubjects, DECsubjects, targetIDs)