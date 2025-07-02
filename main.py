#this is a python project by Enrique Castro
#boilerplate logging setup
import logging #allows for the creation of native logs
from log import setup_logging

setup_logging()
log = logging.getLogger(__name__)

#this is a test
#imported libraries
import os # allows interface with directory commands
import tqdm #creates terminal loading bars just wrap any iteration with this module and you should get a lightweight terminal progress bar
import openai #interface for OpenAI

#imported submodules/functions
from arashi_engine import ArashiEngine #imports the inverted index class
#controls the flow of execution

def main():
    #some  sort of checksum value that checks to see if there already exists a index
    log.info('running main')
    directory_path = "Transcripts"

    engine = ArashiEngine(directory_path)
    results = engine.search_phrase("what is")
    engine.print_matches(results)

#start point of flow control
if __name__ == "__main__":
    main()  


