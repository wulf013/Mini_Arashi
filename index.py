#this is an index module written by Enrique Castro

#boilerplate logging 
from importlib.resources import contents
import logging
from log import setup_logging
setup_logging()
log = logging.getLogger('__main__.'+__name__)

#imported libraries
import os #directory navigation
import tqdm #progress bars, because its cool but also gives visual cues and point of intercept for error and log statements. 
import re # regular expressions allows for interactions beyond US ASCII standards for text manipulation in python

class inverted_index: #the self named class will build the searchable set of generated data from the
    def __init__(self) -> None: #object constructor that creates the index itself
        ### set some sort of checksum here so that the initalization can tell if it needs to build the index or just search it I imagine this might just be a developer function anyways
        self.index = {} # the index will have the following format  {term: {doc_id:{[timestamp]},frequency}}
        self.documents = [] # list of documents that the init will build

    def add_documents_from_directory(self, directory) -> None: #this function adds the documents from the directory
        files = [f for f in os.listdir(directory) if f.endswith('.txt')] #creates the handler for handling the directory and files.
        for file_name in tqdm(files, desc="processing directory"): #tqdm updates and loading bar
            file_path = os.path.join(directory, file_name) #get the file name the directory
            self.add_document(file_path) #call the add document function from this class
    
    def add_document(self, file_path) -> None: #adding a document, by acessing the directory and interacting directly with the file
        with open(file_path, 'r', encoding='utf-8') as file: #open the file using the utf-8 encoding standard
            content = file.readlines() #get the 'conent' using the read lines
        doc_id = len(self.documents)  # New document ID
        self.documents[doc_id] = file_path #create a document ID that can be used to delinitate this document from others
        self.index_document(doc_id, content)

    def index_document(self, doc_id, content) -> None: #begin the indexing of the document into terms
        current_timestamp = None #the current time stamp to pair with the terms
        for line in tqdm(content, desc=f"indexing document {doc_id}", leave=False): #creates the loading bar for the file handler
            timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})', line) #regular expression match function assignment. regular expression is reassigned including some formatting to 'timestamp_match'
            if timestamp_match: #in the instance that there is a timestamp match
                current_timestamp = timestamp_match.group(1) #set the current time stamp to the timestamp match
            else: #in the instance that there is no match
                terms = line.split() #split the string along any whitespace
                for term in terms: #for the number of terms in the terms variable
                    term = term.strip().lower() #lowercase the entire term, strip any whitespace
                    if term: #if there is a term
                        if term not in self.index: #if the term is not in the index
                            self.index[term] = {}  #create a new term in the dictionary
                        if doc_id not in self.index[term]:  #if the document is not connected to the term
                            self.index[term][doc_id] = [] #attach the document ID and term together
                            self.index[term][doc_id].append((current_timestamp, 1)) #attach the current timestamp to the term and document ID string.

    def search(self, term) -> dict: #search through the dict
        return self.index.get(term, {}).keys()  # get the term along wiht the keys associated with the term
    
    def get_document(self, doc_id) -> str: #returns the document file path, given the document ID
        return self.documents.get(doc_id, None)