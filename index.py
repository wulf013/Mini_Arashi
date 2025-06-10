#this is an index module written by Enrique Castro

#boilerplate logging 
import logging
from log import setup_logging
setup_logging()
log = logging.getLogger('__main__.'+__name__)

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
        
        for file_name in tqdm(files, desc="Processing directory"): #tqdm updates and loading bar
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

    def search_term(self, term):
        term = term.lower().strip() #lowercase and strip
        data = self.index.get(term, None)

        if not data:
            print(f"'{term}' not found in index.")
            return

        print(f"'{term}' found in {len(data)} document(s):") #length of the term dictionary which should match the number of transcripts we a re using

        for doc_id, timestamp_data in data.items():
            doc_path = self.documents[doc_id] if doc_id < len(self.documents) else "<unknown document>"
            total_freq = sum(info["count"] for info in timestamp_data.values())

            print(f" Document ID: {doc_id}")
            print(f"  File Path: {doc_path}")
            print(f"  Total Occurrences in Document: {total_freq}")
            print(f"  Occurrences by Timestamp:")

            for timestamp, info in timestamp_data.items():
                count = info["count"]
                positions = info["positions"]
                print(f"    {timestamp} - {count} time(s), positions: {positions}")

    def search_phrase(self, phrase: str): # a cascading search function that allows the user to look up phrases.
        log.info('executing phrase search')
        terms =  [term.strip().lower() for term in phrase.split()]
       
        if not terms:
            log.error('Empty Phrase')
            return[]

        common_locations = self._get_common_locations(terms)
        if not common_locations:
            log.info('No locations with all terms present')
            return[]

        matches = self._check_phrase_match(terms, common_locations)

        for doc_id, timestamp, pos in matches:
            doc_path = self._get_document(doc_id) or "<unknown>"
            #print(f"Phrase found in doc {doc_id} ({doc_path}) at {timestamp}  starting at position {position}")

        return matches

    def _check_phrase_match(self, terms, locations):
        matches = []

        for doc_id, timestamp in locations:
            # Build a list of position sets per term in order
            try:
                position_lists = [
                    set(self.index[term][doc_id][timestamp]["positions"])
                    for term in terms
                ]
            except KeyError:
                continue  # Skip if any term is missing here

            # Identify possible starting positions for the phrase
            first_term_positions = position_lists[0]

            for pos in first_term_positions:
                if all((pos + i) in position_lists[i] for i in range(len(terms))):
                    matches.append((doc_id, timestamp, pos))
                    break  # Optional: stop at first match for this location

        return matches

    def _get_common_locations(self, terms): #returns the intersection of a set of all timestamps where all the terms appear
        log.info('identifying commong locations of key terms')
        term_location = []
        for term in terms:
            locations = set()
            for doc_id, timestamps in  self.index.get(term, {}).items():
                for ts in timestamps:
                    locations.add((doc_id, ts))
            term_location.append(locations)
        
        return set.intersection(*term_location) if term_location else set()

    def print_matches(self, matches):
        if not matches:
            print("No matches found.")
            return

        print(f"\nFound {len(matches)} match(es):\n")
        for i, (doc_id, timestamp, start_pos) in enumerate(matches, 1):
            doc_path = self._get_document(doc_id) or "<unknown file>"
            print(f"{i}. Document ID: {doc_id}")
            print(f"   File Path:   {doc_path}")
            print(f"   Timestamp:   {timestamp}")
            print(f"   Start Pos:   {start_pos}\n")

    def _get_document(self, doc_id) -> str: #returns the document file path, given the document ID
        if 0 <= doc_id < len(self.documents):
            return self.documents[doc_id]
        else:
            return None