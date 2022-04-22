import os
import csv
import random
import shutil

# Replace these with your paths of interest, assuming cord19 is downloaded into cord19 directory
path_to_data = '/archive2/kyle/cord19/document_parses/pdf_json/'
new_path = '/archive2/kyle/cord19/document_parses_10000/'

# Set up variables
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
