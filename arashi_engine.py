#this is a search engine module for transcripts written by Enrique Castro
#boilerplate logging 
import logging
from log import setup_logging
setup_logging()
log = logging.getLogger("__main__."+__name__)

#These submodules portion out parts of the engine for planning clarity 
from search import Transcript_Search
from index import Inverted_Index


class ArashiEngine:
    def __init__(self, directory_path):
        self.index = Inverted_Index()
        self.index.add_documents_from_directory(directory_path)
        self.search = Transcript_Search(self.index)

    def search_phrase(self, phrase):
        return self.search.search_phrase(phrase)

    def print_matches(self, matches):
        self.search.print_matches(matches)