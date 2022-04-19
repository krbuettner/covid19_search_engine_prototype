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

def callback(title, url):
    webview.create_window(title, url, width=1200, height=900)
    webview.start()

def searchQuery(query, model_type):
    print(query, model_type)
    # Query input variable holds query and model types hold the model (0: Boolean, 1: BM25).
    # Run model here and get docs results such that: [[doc1_title,doc1_url],[doc2_title,doc2_url],[doc3_title,doc3_url],.....]
    # Put the list I mentioned above to 'docs' variable

    index_reader = MyIndexReader.MyIndexReader("trectext")


    clean = clean_content(query)
    query = set_query(clean)

    doc_list = []

    if model_type == 0:
        limit = 10
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
    else:
        search = QueryRetreivalModel.QueryRetrievalModel(index_reader)
        results = search.retrieveQuery(query, 20)
        rank = 1
        for result in results:
            print(query.getTopicId(), " Q0 ", result.getDocNo(),
                  ' ', rank, " ", result.getScore(), " MYRUN",)
            doc_list.append(result.getDocNo()[:-5])
            rank += 1
    print(doc_list)


    with open('gui/id_to_url.pkl', 'rb') as handle:
        id_to_url = pickle.load(handle)

    docs = [] 
    for i in doc_list:
        if i in id_to_url.keys():
            docs.append(id_to_url[i])

    showResults(docs)

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
    for i in range(len(docs)):
        links.append(Label(rule_window, text=docs[i][1], fg="blue", cursor="hand2", anchor= W))
        links[i].pack(fill=X)
        links[i].bind("<Button-1>", lambda e: callback(docs[i][1],docs[i][0]))


    # #link1 = Label(rule_window, text=docs[0][1], fg="blue", cursor="hand2", anchor= W)
    # #link1.pack(fill=X)
    # #link1.bind("<Button-1>", lambda e: callback(docs[0][1],docs[0][0]))
    
    # link2 = Label(rule_window, text=docs[1][1], fg="blue", cursor="hand2", anchor= W)
    # link2.pack(fill=X)
    # link2.bind("<Button-1>", lambda e: callback(docs[1][1],docs[1][0]))

    # link3 = Label(rule_window, text=docs[2][1], fg="blue", cursor="hand2", anchor= W)
    # link3.pack(fill=X)
    # link3.bind("<Button-1>", lambda e: callback(docs[2][1],docs[2][0]))

    # link4 = Label(rule_window, text=docs[3][1], fg="blue", cursor="hand2", anchor= W)
    # link4.pack(fill=X)
    # link4.bind("<Button-1>", lambda e: callback(docs[3][1],docs[3][0]))

    # link5 = Label(rule_window, text=docs[4][1], fg="blue", cursor="hand2", anchor= W)
    # link5.pack(fill=X)
    # link5.bind("<Button-1>", lambda e: callback(docs[4][1],docs[4][0]))

    # link6 = Label(rule_window, text=docs[5][1], fg="blue", cursor="hand2", anchor= W)
    # link6.pack(fill=X)
    # link6.bind("<Button-1>", lambda e: callback(docs[5][1],docs[5][0]))

    # link7 = Label(rule_window, text=docs[6][1], fg="blue", cursor="hand2", anchor= W)
    # link7.pack(fill=X)
    # link7.bind("<Button-1>", lambda e: callback(docs[6][1],docs[6][0]))

    # link8 = Label(rule_window, text=docs[7][1], fg="blue", cursor="hand2", anchor= W)
    # link8.pack(fill=X)
    # link8.bind("<Button-1>", lambda e: callback(docs[7][1],docs[7][0]))

    # link9 = Label(rule_window, text=docs[8][1], fg="blue", cursor="hand2", anchor= W)
    # link9.pack(fill=X)
    # link9.bind("<Button-1>", lambda e: callback(docs[8][1],docs[8][0]))

    # link10 = Label(rule_window, text=docs[9][1], fg="blue", cursor="hand2", anchor= W)
    # link10.pack(fill=X)
    # link10.bind("<Button-1>", lambda e: callback(docs[9][1],docs[9][0]))


def run_gui():
    
    window_height = 500
    window_width = 900

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    top.wm_title("Covid Search")

    # Entry Place
    e1=Entry(top,bd=6,width=40, fg='grey')
    e1.insert(0, '')
    e1.place(relx=0.5, rely=0.55, anchor=CENTER)
    e1.focus()

    #Radio Buttons
    var = IntVar()
    R1 = Radiobutton(top, text="Exact Match", variable=var, value=0)
    R1.pack( anchor = CENTER )
    R1.place(relx=0.52, rely=0.62, anchor=E)
    R2 = Radiobutton(top, text="Relevance Search", variable=var, value=1)
    R2.pack( anchor = CENTER )
    R2.place(relx=0.52, rely=0.62, anchor=W)

    #Search Button
    b1=Button(top,text="Search",command= lambda: searchQuery(query = e1.get(), model_type = var.get()))
    b1.place(relx=0.5, rely=0.68, anchor=CENTER)

    frame = Frame(top, width=200, height=200)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.25)

    # Create an object of tkinter ImageTk
    img = Image.open("gui/image.png")
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

with open('gui/id_to_url.pkl', 'rb') as handle:
    id_to_url = pickle.load(handle)

top=Tk()
run_gui()




# This is needed to build index
index_reader = MyIndexReader.MyIndexReader("trectext")

model = input("Boolean (B) or Query Likelihood (Q)? ")
q = get_query()
clean = clean_content(q)
query = set_query(clean)

doc_list = []

if model == "B":
    limit = int(input("How many documents would you like returned? "))
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
else:
    search = QueryRetreivalModel.QueryRetrievalModel(index_reader)
    results = search.retrieveQuery(query, 20)
    rank = 1
    for result in results:
        print(query.getTopicId(), " Q0 ", result.getDocNo(),
              ' ', rank, " ", result.getScore(), " MYRUN",)
        doc_list.append(result.getDocNo()[:-5])
        rank += 1
print(doc_list)
