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
from index import Inverted_Index #imports the inverted index class
from gpt_interface import interface
#controls the flow of execution

def main():
    #some  sort of checksum value that checks to see if there already exists a index
    log.info('running main')
    directory_path = "Transcripts"

    index = bootup(directory_path)  #establisting the index object
    #log.info('searching for term')
    #Inverted_Index.search_term(index,'Joe') #just testing user input
    log.info('searching for phrase')
    results = Inverted_Index.search_phrase(index,'That happened')
    Inverted_Index.print_matches(index, results)

def bootup(directory_path) -> dict: #handle the bootup and initalization process of the index
    log.info('booting up index')
    content_index = Inverted_Index()
    Inverted_Index.add_documents_from_directory(content_index, directory_path)
    return content_index


#start point of flow control
if __name__ == "__main__":
    main()  


    #PODCAST STOP TIME 1:38:49