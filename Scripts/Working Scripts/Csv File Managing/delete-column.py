import pandas as pd
f=pd.read_csv("../../../Data/Non-GIS Data/cleaned/park_location_cleaned.csv")
keep_col = ['district_tr']
new_f = f[keep_col]
new_f.to_csv("trdistrict.csv", index=False)

#keep_col = ['institution_id', 'district_tr', 'institution_name', 'latitude', 'longitude', 'neighborhood_tr']
