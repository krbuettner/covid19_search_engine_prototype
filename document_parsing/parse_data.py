
# This is tailored to my repo, but the general idea is there

import os
import csv
import random
import shutil

# Import configs
path_to_data = '/archive2/kyle/cord19/document_parses/pdf_json/'
new_path = '/archive2/kyle/cord19/document_parses_10000/'
list_of_file_names = []
num_samples = 10000

# Get all pdf files in folder
for doc_file_name in os.listdir(path_to_data):
    list_of_file_names.append(doc_file_name)

# Sample subset of them
random_sample = random.sample(list_of_file_names, num_samples)

# Copy to new folder
for f in random_sample:
    print(f)
    shutil.copyfile(path_to_data + f, new_path + f)

# Some functionality for reading csv files
#for csv_file_name in os.listdir(path_to_data):
#    print(csv_file_name)
#    with open(path_to_data + csv_file_name, newline='') as csvfile:
#        reader = csv.reader(csvfile, delimiter=' ',quotechar='|')
#        for row in reader:
#            print(row)
#        exit()
