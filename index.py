#this is an index module written by Enrique Castro

#boilerplate logging 
from importlib.resources import contents
import logging
from log import setup_logging
setup_logging()
log = logging.getLogger('__main__.'+__name__)

#imported libraries
import os #directory navigation
from tqdm import tqdm #progress bars, because its cool but also gives visual cues and point of intercept for error and log statements. 
import re # regular expressions allows for interactions beyond US ASCII standards for text manipulation in python

class inverted_index: #the self named class will build the searchable set of generated data from the
    def __init__(self) -> None: #object constructor that creates the index itself
        log.info('initialization of inverted index object')
        ### set some sort of checksum here so that the initalization can tell if it needs to build the index or just search it I imagine this might just be a developer function anyways
        self.index = {} # the index will have the following format  {term: {doc_id:{[timestamp]},frequency}}
        self.documents = [] # list of documents that the init will build

    def add_documents_from_directory(self, directory) -> None: #this function adds the documents from the directory
        log.info('accessing directory')
        files = [f for f in os.listdir(directory) if f.endswith('.txt')] #creates the handler for handling the directory and files.
        for file_name in tqdm(files, desc="processing directory"): #tqdm updates and loading bar
            file_path = os.path.join(directory, file_name) #get the file name the directory
            self.add_document(file_path) #call the add document function from this class
    
    def add_document(self, file_path) -> None: #adding a document, by acessing the directory and interacting directly with the file
        log.info('adding document')
        with open(file_path, 'r', encoding='utf-8') as file: #open the file using the utf-8 encoding standard
            content = file.readlines() #get the 'conent' using the read lines
        doc_id = len(self.documents)  # New document ID
        self.documents.append(file_path) #append the document ID that can be used to delinitate this document from others in the documents list
        log.info('document ID added to the documents list')
        self.index_document(doc_id, content)

    def index_document(self, doc_id, content) -> None:
        from collections import Counter

        current_timestamp = None

        for line in tqdm(content, desc=f"indexing document {doc_id}", leave=False):
            timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})', line)
            if timestamp_match:
                current_timestamp = timestamp_match.group(1)
            else:
                terms = [term.strip().lower() for term in line.split() if term.strip()]
                term_counts = Counter(terms)  # Count each term on the line

                for term, count in term_counts.items():
                    if term not in self.index:
                        self.index[term] = {}
                    if doc_id not in self.index[term]:
                        self.index[term][doc_id] = []
                
                    self.index[term][doc_id].append((current_timestamp, count))


    def inspect_term(self, term):
        term = term.lower().strip()
        data = self.index.get(term, None)
    
        if not data:
            print(f"'{term}' not found in index.")
            return

        print(f"'{term}' found in {len(data)} document(s):")
    
        for doc_id, occurrences in data.items():
            doc_path = self.documents[doc_id] if doc_id < len(self.documents) else "<unknown document>"
            total_freq = sum(freq for _, freq in occurrences)

            print(f" Document ID: {doc_id}")
            print(f"  File Path: {doc_path}")
            print(f"  Total Occurrences in Document: {total_freq}")
            print(f"  Occurrences by Timestamp:")

            for timestamp, freq in occurrences:
                print(f"    {timestamp} - {freq} time(s)")

    def search(self, term:str) -> dict: #search through the dict
        return self.index.get(term, {}).keys()  # get the term along wiht the keys associated with the term
    
    def get_document(self, doc_id) -> str: #returns the document file path, given the document ID
        return self.documents.get(doc_id, None)