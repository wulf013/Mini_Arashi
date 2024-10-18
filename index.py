#this is an index module written by Enrique Castro

#boilerplate logging 
import logging
from log import setup_logging
setup_logging()
log = logging.getLogger('__main__.'+__name__)

#imported libraries
import os
import tqdm
import re

def create_index():
    print("creating index")

class Inverted_Index:
    def __init__(self):
        self.index = {} #{term: {doc_id:{[timestamp]},frequency}}
        self.docuemts = [] #list of document contents

    def add_documents_from_directory(self, directory): #adding documents to the index
        files = [f for f in os.listdir(directory) if f.endswtih('.txt')]
        for file_name in tqdm(files, desc="processing files"):
            file_path = os.path.join(directory, file_name)
            self.add_document(file_path) #makes a call to add_document function that does the 'dirty work'

    def add_document(self, file_path): #adding a document, by accessing the directory and interacting directly with the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        doc_id = len(self.documents)  # New document ID
        self.documents[doc_id] = file_path
        self.index_document(doc_id, content)

    def index_document(self, doc_id, content):
        current_timestamp = None

        for line in tqdm(content, desc=f"indexing document {doc_id}", leave=False):
            timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})', line)
            if timestamp_match:
                current_timestamp = timestamp_match.group(1)
            else:
                terms = line.split()
                for term in terms:
                    term = term.strip().lower()
                    if term:
                        if term not in self.index:
                            self.index[term] = {}
                        if doc_id not in self.index[term]:
                            self.index[term][doc_id] = []
                            self.index[term][doc_id].append((current_timestamp, 1))

    def search(self, term): #this might have to be worked on
        return self.index.get(term, {}).keys()  # Returns document IDs
    
    def get_document(self, doc_id):
        return self.documents.get(doc_id, None)