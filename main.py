#this is a python project by Enrique Castro
#boilerplate logging setup
import logging #allows for the creation of native logs
from log import setup_logging
setup_logging()
log = logging.getLogger(__name__)

#this is a test
#imported libraries
import os # allows interface with directory commands
import tqdm #creates terminal loading bars
import openai #interface for OpenAI

#imported submodules/functions
from index import inverted_index #imports the inverted index class
from gpt_interface import interface
#controls the flow of execution

def main():
    log.info('running main')
    directory_path = "Transcripts"
    content_index = inverted_index()
    inverted_index.add_documents_from_directory(content_index, directory_path)
    log.info('inspecting term')
    inverted_index.inspect_term(content_index,'Joe')

#start point of flow control
if __name__ == "__main__":
    main()  