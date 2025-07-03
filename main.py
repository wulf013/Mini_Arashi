#this is a python project by Enrique Castro
#boilerplate logging setup
import logging #allows for the creation of native logs
from log import setup_logging

setup_logging()
log = logging.getLogger(__name__)

#imported libraries

#imported submodules/functions
from arashi_engine import ArashiEngine #imports the inverted index class
#controls the flow of execution

def main():
    #some  sort of checksum value that checks to see if there already exists a index
    log.info('running main')
    engine = ArashiEngine("Transcripts")
    results = engine.search_phrase("what is")
    engine.print_matches(results)

#start point of flow control
if __name__ == "__main__":
    main()  


