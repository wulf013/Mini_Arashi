#this is a python project by Enrique Castro

#boilerplate logging setup
import logging #allows for the creation of native logs
from log import setup_logging
setup_logging()
log = logging.getLogger(__name__)


#imported libraries
import os # allows interface with directory commands
import tqdm #creates terminal loading bars
import openai #interface for OpenAI

#imported submodules/functions
import index

#controls the flow of execution
def main():
    log.info('running main')

#start point of flow control
if __name__ == "__main__":
    main()