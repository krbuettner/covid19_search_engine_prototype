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
import tkinter

# Global arguments to set for running program
write_index = False
num_exact_matches = 30
num_ranked_matches = 30
dropdown_range = [1,2,3,4,5,10,20]

###################################################################################################################################
# Code to build index if needed
###################################################################################################################################

# Removing nonalphanumeric chars may not be good if symbols are of value
def WriteIndex(type):
    count = 0
    # Initiate pre-processed collection file reader.
    corpus = PreprocessedCorpusReader.PreprocessedCorpusReader(type)
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter(type)
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc[0], doc[1], doc[2])
        count += 1
        if count % 1000 == 0:
            print("finish ", count, " docs")
    print("totally finish ", count, " docs")
    indexWriter.close()

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

def set_query(query):
    aQuery = Query.Query()
    aQuery.setQueryContent(query)
    aQuery.setTopicId('Topic 1')
    return aQuery

###################################################################################################################################
# GUI and Search Code
###################################################################################################################################

# Show URL in external window
def callback(title, url):
    webview.create_window(title, url, width=1200, height=900)
    webview.start()

# MAKE FUNCTION FOR QUERY SEARCH
def searchQuery(query, time, model_type):

    # create object to read through corpus 
    index_reader = MyIndexReader.MyIndexReader("trectext")

    time_restricted_search = False
    if time == "Restrict Search to Timeframe" or time == "All Time":
        time_restricted_search = False
        min_valid_time = index_reader.min_year
    else:
        time_restricted_search = True
        time_split = time.split()
        year = int(time_split[1])
        print(year)
        min_valid_time = index_reader.max_year - year
        print(min_valid_time)




    # store original query, and clean query for processing
    orig_query = query
    clean = clean_content(query)
    query = set_query(clean)

    




    # Get matching docs if Boolean (0) or ranked docs if language model (1)
    doc_list = []
    doc_dates = []
    if model_type == 0:
        limit = num_exact_matches
        search = QueryRetreivalModelBoolean.QueryRetrievalModelBoolean(index_reader)
        print("Your Query is " + query.getQueryContent())
        results = search.retrieveQuery(query, min_valid_time)
        print(results)
        print(len(results))
        rank = 1
        for result in results:
            print(query.getTopicId(), " Q0 ", result.getDocNo(),
                  " ", " MYRUN",)
            rank += 1
            doc_list.append(result.getDocNo()[:-5])
            doc_dates.append(result.getDocDate())
            if (rank == limit+1):
                break
    # Language model
    else:
        search = QueryRetreivalModel.QueryRetrievalModel(index_reader)
        results = search.retrieveQuery(query, num_ranked_matches, min_valid_time)
        rank = 1
        for result in results:
            print(query.getTopicId(), " Q0 ", result.getDocNo(),
                  ' ', rank, " ", result.getScore(), " MYRUN",)
            doc_list.append(result.getDocNo()[:-5])
            doc_dates.append(result.getDocDate())
            rank += 1
    print(doc_list)
    print(doc_dates)

    # Open ID to URL and create URL list for docs
    with open('id_to_url.pkl', 'rb') as handle:
        id_to_url = pickle.load(handle)
    docs = [] 
    for i in doc_list:
        if i in id_to_url.keys():
            docs.append(id_to_url[i])

    # Show results based on docs retrieved
    showResults(docs, doc_list, orig_query, doc_dates)


# This is second window
def showResults(docs, doc_list, query, doc_dates):

    # This gets doc_surrogates from this "orig" file
    # Took introduction paragraphs and stored them in file
    doc_surr_dict = dict()
    with open('data/all_docs_orig.txt', 'r', newline='', encoding="utf8") as f:
        lines = f.readlines()
        counter = 0
        while counter < len(lines):
            doc_surr_dict[lines[counter].strip()] = lines[counter + 1].strip()
            counter = counter + 2
   
    # This is setting up window with scrollbar
    rule_window = Toplevel(top)
    window_height = 500
    window_width = 1200
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    rule_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    rule_window.title("Search Results")
    main_frame = Frame(rule_window)
    main_frame.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    my_scrollbar = tkinter.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")) )
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    # Add appropriate links and doc surrogates to screen
    links = []
    doc_surrogates = []
    dates = []
    search_label = Label(second_frame, text="Search: " + str(query), fg="green", cursor="hand2", font='Helvetica 12 bold', anchor= W, wraplengt=1500)
    search_label.pack(fill=X)
    for i in range(len(docs)):
        links.append(Label(second_frame, text=docs[i][1], fg="blue", cursor="hand2", font='Helvetica 10 bold', anchor= W))
        dates.append(Label(second_frame, text=doc_dates[i], fg="purple", cursor="hand2", font="Helvetica 10 bold", anchor=W))
        doc_surrogate_text = doc_surr_dict[doc_list[i] + '.json'][0:500]
        doc_surrogates.append(Label(second_frame, text=doc_surrogate_text+"...", fg="black", cursor="hand2", anchor= W, justify=LEFT, wraplengt=500))
        links[i].pack(fill=X)
        dates[i].pack(fill=X)
        doc_surrogates[i].pack(fill=X)
        def make_lambda(docs, i):
            return lambda e : callback(docs[i][1], docs[i][0])
        links[i].bind("<Button-1>", make_lambda(docs, i))


# Function that sets up GUI from start
def run_gui():
    
    # Window dimensions and basics set up
    window_height = 500
    window_width = 900
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) - (window_height/2))
    top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    top.wm_title("Covid-19 Search")

    # Entry place for search
    e1=Entry(top,bd=6,width=40, fg='black')
    e1.insert(0, '')
    e1.place(relx=0.5, rely=0.6, anchor=CENTER)
    e1.focus()

    # Radio Buttons

    var = IntVar()
    R1 = Radiobutton(top, text="Exact Match", variable=var, value=0)
    R1.pack( anchor = CENTER)
    R1.place(relx=0.5, rely=0.5, anchor=E)

    R2 = Radiobutton(top, text="General Info", variable=var, value=1)
    R2.pack(anchor = CENTER)
    R2.place(relx=0.5, rely=0.5, anchor=W)

    # Timeframe
    menu= StringVar()
    menu.set("Restrict Search to Timeframe")
    index_reader = MyIndexReader.MyIndexReader("trectext")
    menu_options = []


    

    # Make frame
    frame = Frame(top, width=200, height=200)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.25)

    # Create an object of tkinter ImageTk
    img = Image.open("image.png")
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)

    # Create a Label Widget to display the text or Image
    label = Label(frame, image=img)
    label.pack()

    for i in dropdown_range:
        if i == 1:
            menu_options.append("Last year")
        else:
            menu_options.append("Last " + str(i) + " years")
    menu_options.append("All Time")
    drop= OptionMenu(top, menu,*menu_options)
    drop.place(relx=0.5, rely=0.78, anchor=CENTER)

    # Search Button
    b1=Button(top,text="Search",command= lambda: searchQuery(query = e1.get(), time=menu.get(), model_type = var.get()))
    b1.place(relx=0.5, rely=0.68, anchor=CENTER)


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

