This is a readme file that will be both a planning and documentation document  

The scope of this project will evolve over time as the integration of new features will eventually expand what its capable of and what it can be used for. Leveraging the OpenAI API, and piping documents and texts into it, this project will seek provide basic senitment analysis and searchable phrases. The idea being that you can use this project to process and provide additional accessablilty to your podcast. This is especially useful, for people who have trouble with auditory mediums or if they have auditory sensory issues.

The inverted index class, and submodule is intended to be the entrypoint for a number of functions related to the navitation, entry and management of the data set that is going to be pushed and to GPT

--- issues on the index document function ---
The primary issue with the indexing function for the documents is that it would only add on timestamp-term pair per document line, even if the term appeared more than once on that line.