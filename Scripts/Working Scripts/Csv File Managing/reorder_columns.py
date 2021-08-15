import csv

with open("newFile.csv", 'r') as infile, open('reordered.csv', 'a') as outfile:
    # output dict needs a list for new column ordering
    fieldnames = ['institution_id', 'district_tr2', 'district_eng', 'institution_name', 'latitude', 'longitude', 'neighborhood_tr', 'neighborhood_eng', 'institution_type_abbrv_tr']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
   # institution_id, district_tr2, district_eng, institution_name, latitude, longitude, neighborhood_tr, neighborhood_eng, institution_type_tr, institution_type_eng, care_type, district_tr
    # reorder the header first
    writer.writeheader()
    for row in csv.DictReader(infile):
        # writes the reordered rows to the new file
        writer.writerow(row)

#    fieldnames = ['institution_id', 'district_tr', 'district_eng', 'institution_name', 'latitude', 'longitude', 'neighborhood_tr', 'neighborhood_eng', 'institution_type_abbrv_tr', 'institution_type_abbrv_eng']

