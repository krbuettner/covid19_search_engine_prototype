import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.QueryRetreivalModelBoolean as QueryRetreivalModelBoolean
import Classes.Query as Query
from nltk.stem.porter import PorterStemmer
import datetime
import IndexingWithWhoosh.PreProcessedCorpusReader as PreprocessedCorpusReader
import IndexingWithWhoosh.MyIndexWriter as MyIndexWriter
import pickle
from tkinter import *
from PIL import Image,ImageTk
import webbrowser
import webview # pip install pywebview
import pickle

# Command line arguments for program
write_index = False
num_exact_matches = 10
num_ranked_matches = 5

###################################################################################################################################
# Code to build index if needed
###################################################################################################################################

# Removing nonalphanumeric chars may not be good if symbols are of value
def WriteIndex(type):
    count = 0
    # Initiate pre-processed collection file reader.
    corpus =PreprocessedCorpusReader.PreprocessedCorpusReader(type)
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter(type)
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc[0], doc[1])
        count+=1
        if count%1000==0:
            print("finish ", count," docs")
    print("totally finish ", count, " docs")
    indexWriter.close()
    return

###################################################################################################################################
# Code to get, set, and clean queries
###################################################################################################################################

def clean_content(query, make_lowercase=True, stem=True, remove_nonalpha=True):
    bool_ops = ['AND', 'OR', 'NOT', 'ANDNOT', 'ANDMAYBE']
    stemmer = PorterStemmer()
    query_list = query.split()
    clean_string = ''
    for term in query_list:
        if (term not in bool_ops):
            a = term
            if make_lowercase:
                a = term.lower()
            if stem:
                a = stemmer.stem(a)
            if remove_nonalpha:
                a = ''.join(filter(str.isalnum, a))
            clean_string += a + ' '
        else:
            clean_string += term + ' '
    return clean_string


def get_query():
    query = input("Enter your query: ")
    return query


def set_query(query):
    aQuery = Query.Query()
    aQuery.setQueryContent(query)
    aQuery.setTopicId('Topic 1')
    return aQuery

###################################################################################################################################
# GUI Code
###################################################################################################################################

# Show URL in external window
def callback(title, url):
    webview.create_window(title, url, width=1200, height=900)
    webview.start()

# This is main functionality that calls Boolean or language models
def searchQuery(query, model_type):
    print(query, model_type)

    # Create index reader
    index_reader = MyIndexReader.MyIndexReader("trectext")

    # Format query as necessary
    clean = clean_content(query)
    query = set_query(clean)

    # Get matching docs if Boolean (0) or ranked docs if language model (1)
    doc_list = []
    if model_type == 0:
        limit = num_exact_matches
        search = QueryRetreivalModelBoolean.QueryRetrievalModelBoolean(index_reader)
        print("Your Query is " + query.getQueryContent())
        results = search.retrieveQuery(query)
        rank = 1
        for result in results:
            print(query.getTopicId(), " Q0 ", result.getDocNo(),
                  " ", " MYRUN",)
            rank += 1
            doc_list.append(result.getDocNo()[:-5])
            if (rank == limit+1):
                break
    # Language model
    else:
        search = QueryRetreivalModel.QueryRetrievalModel(index_reader)
        results = search.retrieveQuery(query, num_ranked_matches)
        rank = 1
        for result in results:
            print(query.getTopicId(), " Q0 ", result.getDocNo(),
                  ' ', rank, " ", result.getScore(), " MYRUN",)
            doc_list.append(result.getDocNo()[:-5])
            rank += 1
    print(doc_list)

    # Open ID to URL and create URL list for docs
    with open('id_to_url.pkl', 'rb') as handle:
        id_to_url = pickle.load(handle)
    docs = [] 
    for i in doc_list:
        if i in id_to_url.keys():
            docs.append(id_to_url[i])

    # Show results based on docs retrieved
    showResults(docs)


# This is second window
def showResults(docs):
    rule_window = Toplevel(top)
    window_height = 500
    window_width = 900

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    rule_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    rule_window.title("Search Results")

    links = []

    dictionary_with_url_indices = dict()

    for i in range(len(docs)):
        links.append(Label(rule_window, text=docs[i][1], fg="blue", cursor="hand2", anchor= W))
        links[i].pack(fill=X)
        dictionary_with_url_indices[docs[i][1]] = docs[i][0]
        def make_lambda(docs, i):
            return lambda e : callback(docs[i][1], docs[i][0])
        links[i].bind("<Button-1>", make_lambda(docs, i))

# This is main function that sets up and runs GUI
def run_gui():
    
    window_height = 500
    window_width = 900

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) - (window_height/2))

    top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    top.wm_title("Covid-19 Search")

    # Entry Place
    e1=Entry(top,bd=6,width=40, fg='grey')
    e1.insert(0, '')
    e1.place(relx=0.5, rely=0.6, anchor=CENTER)
    e1.focus()

    # Radio Buttons
    var = IntVar()
    R1 = Radiobutton(top, text="Exact Match", variable=var, value=0)
    R1.pack( anchor = CENTER )
    R1.place(relx=0.5, rely=0.5, anchor=E)
    R2 = Radiobutton(top, text="Relevance Search", variable=var, value=1)
    R2.pack( anchor = CENTER )
    R2.place(relx=0.5, rely=0.5, anchor=W)

    # Search Button
    b1=Button(top,text="Search",command= lambda: searchQuery(query = e1.get(), model_type = var.get()))
    b1.place(relx=0.5, rely=0.68, anchor=CENTER)

    frame = Frame(top, width=200, height=200)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.25)

    # Create an object of tkinter ImageTk
    img = Image.open("image.png")
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)

    # Create a Label Widget to display the text or Image
    label = Label(frame, image = img)
    label.pack()

    top.mainloop()


#############################################################################################################################
# Main Code Functionality 
#############################################################################################################################

# If we need to build index, set this command line option to True
if write_index:
    WriteIndex("trectext")

# This sets up and runs GUI
top=Tk()
run_gui()

