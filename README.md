## COVID-19 Information Retrieval Search Engine Prototype

Contributors: Kyle Buettner, Cagri Gungor, Benjamin Truckenbrod

Quick Run: Visit index_engine folder and type python query_index.py

Since the COVID-19 pandemic's start, it has been difficult for people to identify reliable, trustworthy information about COVID-19. The creation of the CORD-19 dataset (https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge) has provided a comprehensive source of scholarly articles regarding COVID-19. We aim to provide a search engine prototype tool to help users parse through such articles. In effect, people can achieved higher scientific literacy and be better informed to affect change.  

![view1](https://user-images.githubusercontent.com/78238895/164766550-08a2436f-411f-4f1b-be42-079f3e232b5e.PNG)
![view2](https://user-images.githubusercontent.com/78238895/164766562-917c39ce-3507-45b5-a705-0a7b9340d3b8.PNG)

### Our project includes functionality for the following

* Exact match search - Identify scholarly articles including exact terms specified in search using Boolean operators (AND, OR, etc.)
* General info search - Identify scholarly articles considered "relevant" to a user's query
* Search by date - Include articles from last 1, 2, 3, 4, 5, 10, 20 years or all time
* Document surrogate - Document surrogate provided as part of search
* Document retrieval - Ability to open document within application 

### Areas for Improvement

* We provide document surrogates by taking introduction paragraphs out of each scholarly article. If not introduction paragraph is found, then first paragraph is taken. Sometimes these paragraphs are not informative or contain weird symbols. 

### Methods

* Python packages: Whoosh, Tkinter
* Retrieval models: Boolean, query likelihood with Dirichlet smoothing 

Project completed as part of Dr. Daqing He's Information Retreival and Storage course at the University of Pittsburgh. Indexing code was built on code created during that course. 


