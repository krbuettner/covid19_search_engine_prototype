## Running the Search Engine

Some files are needed for operation. Data is downloaded from https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge. 

The data folder needs to have the following files added:
* doc_surr.txt - this represents a list of document names and extracted surrogates
* id_to_url.pkl - this contains dictionary of 
* docs_w_dates.txt - this contains document titles, doc date, and processed doc content

These files for our prototype set of documents can be found at: 

These files can also be made by referring to scripts in the document_parsing folder. 

To run program: python query_index.py 
