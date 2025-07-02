#this is a python submodule written by Enrique Castro

#boilerplate logging 
import logging
from log import setup_logging

setup_logging()
log = logging.getLogger("__main__.arashi_engine."+__name__)

#imported libraries
import os #directory navigation
from tqdm import tqdm #progress bars, because its cool but also gives visual cues and point of intercept for error and log statements. 
from collections import defaultdict #this is a standard python library ----- insert more info here
from collections import Counter #standard python library that lets me count frequency
import re # regular expressions allows for interactions beyond US ASCII standards for text manipulation in python

class Inverted_Index: #the self named class will build the searchable set of generated data from the
    def __init__(self) -> None: #object constructor that creates the index itself
        log.info('initialization of inverted index object')
        self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"count": 0, "positions": []}))) #this is a nested dictionary that stores the values that we are indexing from the podcast transcripts
        # the index will have the following format  {term: {doc_id:{[timestamp]},frequency}}
        self.documents = [] # list of documents that the init will build

    def add_documents_from_directory(self, directory) -> None: #this function adds the documents from the directory
        log.info('accessing directory')
        
        files = [f for f in os.listdir(directory) if f.endswith('.txt')] #creates the handler for handling the directory and files.
        
        for file_name in tqdm(files, desc="Processing file directory"): #tqdm updates and loading bar
            file_path = os.path.join(directory, file_name) #get the file name the directory
            self._add_document(file_path) #call the add document function from this class
    
    def _add_document(self, file_path) -> None: #adding a document, by acessing the directory and interacting directly with the file
        log.info('adding document')
        with open(file_path, 'r', encoding='utf-8') as file: #open the file using the utf-8 encoding standard
            content = file.readlines() #get the 'content' using the read lines
        doc_id = len(self.documents)  # New document ID based on the number of documents in the directory
        self.documents.append(file_path) #append the document ID that can be used to delinitate this document from others in the documents list
        log.info('document ID added to the documents list')
        self._index_document(doc_id, content) # call the index document function that starts adding the words to the index dict.

    def _index_document(self, doc_id, content) -> None:
        current_timestamp = None

        for line in tqdm(content, desc=f"Indexing document {doc_id}", leave=False): #for each line in the file,
            timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})', line) #if there is a timestamp that matches the line
            if timestamp_match:
                current_timestamp = timestamp_match.group(1)
            if  current_timestamp is None:
                continue
            
            terms = [term.strip().lower() for term in line.split() if term.strip()]

            for position, term in tqdm(enumerate(terms), leave=False):
                self.index[term][doc_id][current_timestamp]["count"] +=   1
                self.index[term][doc_id][current_timestamp]["positions"].append(position)

    def _get_document(self, doc_id) -> str: #returns the document file path, given the document ID
         return self.documents[doc_id] if 0 <= doc_id < len(self.documents) else None