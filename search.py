#this is a python submodule written by Enrique Castro
import logging
from log import setup_logging

setup_logging()
log = logging.getLogger("__main__.arashi_engine."+__name__)

class Transcript_Search: #handles the search functionality of the inverted index data structure
    def __init__(self, index):
        self.index = index
        self.documents = index.documents

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
    
    def _get_common_locations(self, terms): #returns the intersection of a set of all timestamps where all the terms appear
        log.info('identifying commong locations of key terms')
        term_location = []
        for term in terms:
            locations = set()
            for doc_id, timestamps in self.index.index.get(term, {}).items():
                for ts in timestamps:
                    locations.add((doc_id, ts))
            term_location.append(locations)
        
        return set.intersection(*term_location) if term_location else set()
        
    def _sliding_window_phrase_match(): # a distinct partial search funtion that maintains the order of terms but permits flexibility in their distance+
        return None

    def _partial_phrase_match(self, terms, locations, strict:int): #still have to review this funciton to make sure that its completely up to snuff
        matches = []

        for doc_id, timestamp in locations:

            try:
                position_lists = [
                    set(self.index.index[term][doc_id][timestamp]["positions"])
                    for term in terms
                ]
            except KeyError:
                continue

            first_term_positions = position_lists[0]
            
            for pos in first_term_positions:
                cur_pos = pos
                status = True

                for i in range(1, len(position_lists)):
                    next_positions = [p for p in position_lists[i] if 0 < p - cur_pos <= strict]        
                    if not next_positions:
                        status = False
                        break
                    cur_pos = next_positions[0]

                if status:
                    matches.append((doc_id,timestamp, pos))
                    break

        return matches
    
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

        matches = self._partial_phrase_match(terms, common_locations, 3)
        
        return matches

    def print_matches(self, matches):
         for doc_id, timestamp, pos in matches:
            doc_path = self.index._get_document(doc_id) or "<unknown>"
            print(f"Phrase found in doc {doc_id} ({doc_path}) at {timestamp} starting at position {pos}")