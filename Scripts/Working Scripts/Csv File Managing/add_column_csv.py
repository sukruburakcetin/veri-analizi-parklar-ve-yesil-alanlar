import csv

with open("trdistrict.csv", 'r') as score, open("../../../Data/Non-GIS Data/cleaned/park_location_cleaned.csv", 'r') as marklist, \
    open("../../../Data/Non-GIS Data/cleaned/merged.csv", 'w') as result:
    score_reader = csv.reader(score)
    marklist_reader = csv.reader(marklist)
    result = csv.writer(result)
    result.writerows(x + y for x, y in zip(marklist_reader, score_reader))




import pandas as pd
import os
import csv

#my_file = "../../../Data/Non-GIS Data/cleaned/park_location_cleaned.csv"
#df = pd.read_csv(my_file)
#for col in df.columns:
    #df[col].to_csv("../../../Data/Non-GIS Data/cleaned/park_location_cleaned{col}.csv")
