This is a readme file that will be both a planning and documentation document  

The scope of this project will evolve over time as the integration of new features will eventually expand what its capable of and what it can be used for. Leveraging the OpenAI API, and piping documents 
and texts into it, this project will seek provide basic senitment analysis and searchable phrases. The idea being that you can use this project to process and provide additional accessablilty to your podcast.
This is especially useful, for people who have trouble with auditory mediums or if they have auditory sensory issues.

The inverted index class, and submodule is intended to be the entrypoint for a number of functions related to the navitation, entry and management of the data set that is going to be pushed and to GPT

--- ISSUES ON INDEXING THE DOCUMENT ---
The primary issue with the indexing function for the documents is that it would only add on timestamp-term pair per document line, even if the term appeared more than once on that line.

Here is the old structure of the index_documents function:
 
 def index_document(self, doc_id, content) -> None: 
        current_timestamp = None
        for line in tqdm(content, desc=f"indexing document {doc_id}", leave=False): 
            timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})', line) 
            if timestamp_match: 
                current_timestamp = timestamp_match.group(1) 
            else: 
                terms = line.split()
                for term in terms:
                term = term.strip().lower() 
                    if term: #if there is a term
                        if term not in self.index: 
                            self.index[term] = {}  
                        if doc_id not in self.index[term]:  
                            self.index[term][doc_id] = [] 
                            self.index[term][doc_id].append((current_timestamp, 1))

So lets break down what happens we run the firs itteration of indexing the documents.
    1. Pull the read file from the add_document function, which pulls from the designated directory, with the content that is opened by it, this is for document 0
    2. The next step we set the variable 'current timestamp' to a null value, we will extract the timestamp later from the document
    3. Now this is where we have the first issue, with the regular expression of match(). The problem here is that match only observes the beginning of the string, and the group(1) specifies that we are 
    only looking at the first parenthesised subgroup, in this case that would be the formatter: (\d{2}:\d{2}:\d{2}\.\d{3}). This means that we're looking for matches to the current time stamp, 
    which is NULL, on the timestamp format.
    4. In our first itteration of this function, there is not matching timestamp, so we start at the 'else' portion of the evalutation. 
        a. split the lines on whitespace again..
        b. for term in terms is confusing at first, but look at the step above. We are splitting the lines in the document based on newline whitespace, this is what we're calling terms. It might be better to 
        conceptualize it as segments of content.
        c. Now looking at the next line we see that there is line that converts the line of content that is a string into a set of strings that comprised of words, this line of code also converts the text into lower case.
        d. Now we have a series of 'if' statements that are going work through adding the term to the dict that was initalized when the object was created.
            d1. In this segment of code the if statments first inquire if the term is or is not in the index. In the instance that there isn't a term that matches the observed one in the index, 
            then the index has a new term added to it.
            d2. Then the entry is added with a timestamp and HARDCODED 1 on the last line. This creates the issue where the indexer is ignoring the possibility that there might be more than one occurance 
            of a word in a line.

So how was this fixed? By introducing the Counter module, we're able to build a map that counts the frequency of each term in the line.  The timestamp is at the beginning of the map, which allows us to
count the true frequency of terms in the transcript. 
