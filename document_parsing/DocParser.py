import os
import json
from nltk.stem.porter import PorterStemmer

# This will be class for parsing the JSON file data 
class DocParser:

	def __init__(self):
		self.stemmer = PorterStemmer()
		self.curr_doc_id_num = 0
		self.ids_to_title = dict()
		self.ids_to_content = dict()

	def get_title(self, data):
		return data["metadata"]["title"]

	def get_content(self, data, just_intros=True):

		# There are multiple sections such as 'metadata', 'abstract', 'body_text' - let's just start with body_text for simplicity
		# Loop through each 'text' section, strip trailing and leading whitespace, then combine all strings at end to create content
		text_secs = []
		json_body_sections = data['body_text']
		for json_sec in json_body_sections:
			json_body_sec_text = json_sec['text']
			if just_intros:
				if json_sec['section'] == "Introduction":
					text_secs.append(json_body_sec_text.strip() + " ")
			else:
				text_secs.append(json_body_sec_text.strip() + " ")
		if just_intros:
			if len(text_secs) == 0:
				for json_sec in json_body_sections:
					json_body_sec_text = json_sec['text']
					text_secs.append(json_body_sec_text.strip() + " ")
					break
		content = "".join(text_secs)
		return content 

	# Stemming, removal of citations 
	def clean_content(self, content_uncleaned, make_lowercase=True, stem=True, remove_nonalpha=True): 	# Removing nonalphanumeric chars may not be good if symbols are of value
		clean_content = content_uncleaned
		if make_lowercase:
			clean_content = clean_content.lower()
		if stem:
			new_clean_content = []
			clean_content = clean_content.split(' ')
			for term in clean_content:
				if remove_nonalpha: 
					term = ''.join(filter(str.isalnum, term))
				term = term.strip()
				new_clean_content.append(self.stemmer.stem(term))
				new_clean_content.append(' ')
			clean_content = ''.join(new_clean_content)
		#print(clean_content)
		return clean_content

	# This is going to be a main function for experimentation
	# We should have flags that specify whether to include certain sections
	# e.g. Should we have abstract? should we perform stemming? lowercase? remove proper nouns?
	# I think this will get edited a good bit 
	# The output should be doc_id and content - need to map doc_ids to title 
	def parse_doc(self, doc_name, ignore_clean=True):

		# Load JSON data for doc
		with open(doc_name, 'r') as f:
			data = json.load(f)

		# Assign doc id, will increment at end
		doc_id = self.curr_doc_id_num

		# Get title, (do not clean it for now)
		title = self.get_title(data)
		self.ids_to_title[doc_id] = title              							# Store info in master list
		
		# Get content, clean it, store it to doc id
		content_uncleaned = self.get_content(data)
		if ignore_clean:
			content_cleaned = content_uncleaned
		else:
			content_cleaned = self.clean_content(content_uncleaned)
		self.ids_to_content[doc_id] = content_cleaned 							# Store info in master list

		# Increment doc ids
		self.curr_doc_id_num = self.curr_doc_id_num + 1             

		return [doc_id, content_cleaned]

parser = DocParser()

# Here is code to generate single doc file
with open('all_docs_orig.txt', 'w') as all_file:
    counter = 0
    for f in os.listdir('./random_document_parses_10000/'):
        doc_name = f
        content = parser.parse_doc('./random_document_parses_10000/' + str(doc_name))
        all_file.write(f)
        all_file.write('\n')
        all_file.write(content[1])
        all_file.write('\n')
        #print(f)
        #print(content)
        print(counter)
        counter = counter + 1

