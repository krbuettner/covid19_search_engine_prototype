## Running the Search Engine

Some files are needed for operation. CORD-19 data is downloaded from https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge. 

The data folder needs to have the following files added from https://drive.google.com/drive/folders/1e7anBSQcg-bNM0_7AIPfZIVNF7cEKWAH?usp=sharing:
* doc_surr.txt - this represents a list of document names and extracted surrogates
* id_to_url.pkl - this contains dictionary of image ids mapped to their corresponding URLs
* docs_w_dates.txt - this contains document titles, doc date, and processed doc content

These data files are created for a small sample of corpus (<10,000 documents), but we provide scripts to create own versions of these files in the document_parsing folder.

To run program: python query_index.py 
