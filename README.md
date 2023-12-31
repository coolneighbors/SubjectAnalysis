# SubjectAnalysis

This repository contains:

A script to cross match subjects between two Zooniverse subjects csvs.

A script to evaluate the total classifications of a Zooniverse workflow by target type.

A script to evaluate the classifications of a Zooniverse workflow, creating csvs for subjects which were voted as 'movers' above a specified amount.

Simply change edit the Zooniverse filenames and object types in the desired python files and run.
##  Dependencies
csv, re, alive_progress, time, and numpy libraries (use pip install or similar installation)

##  File Usage
SubjectResults.py:

Edit the acceptance ratio, target types, and filename depending on analysis needs,, can optionally include IDs to ignore

References Zooniverse workflow classification csv (containing metadata)

Returns:
* five csvs by target type. Within are yes votes/total votes, RA, DEC, Zooniverse subject link, and WiseView link for each individual subject.
          
TypeEvaluation.py:

Edit target types and filenames depending on analysis needs,, can optionally include IDs to ignore

References Zooniverse workflow classification csv (containing metadata)

Returns:
* prints movement and non-movement decisions for every target type
* prints number of classifications in file and number of classifications used

CrossMatch.py

Edit filenames depending on analysis needs

References Zooniverse subjects csv (containing metadata), csv of subject IDs to compare, and csv of targets (RA, DEC, target type)

Returns:
* The total number of subjects present in the Zooniverse subjects csv
* The total number of targets present in the subject IDs csv
* prints subject information (RA, DEC, Target ID) if there is a subject present in both of the two subject files.

Note: You can comment out the target ID function and remove the target ID variable if you have a list of the target RAs and DECs already, you just need to include it in CrossMatch.py

SubjectAnalysis.ipynb:

Contains the three previous python scripts as easily-accessable code cells