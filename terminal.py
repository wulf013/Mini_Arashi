 def index_document(self, doc_id, content) -> None: #begin the indexing of the document into termsAdd commentMore actions
        current_timestamp = None #the current time stamp to pair with the terms
        for line in tqdm(content, desc=f"indexing document {doc_id}", leave=False): #creates the loading bar for the file handler
            timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})', line) #regular expression match function assignment. regular expression is reassigned including some formatting to 'timestamp_match'
            if timestamp_match: #in the instance that there is a timestamp match
                current_timestamp = timestamp_match.group(1) #set the current time stamp to the timestamp match for the first case that is non
            else: #in the instance that there is no match
                terms = line.split() #split the document up based on new lines
                for term in terms: #for the number of terms in the terms variable
                    term = term.strip().lower() #lowercase the entire term, strip any whitespace
                    if term: #if there is a term
                        if term not in self.index: #if the term is not in the index
                            self.index[term] = {}  #create a new term in the dictionary
                        if doc_id not in self.index[term]:  #if the document is not connected to the term
                            self.index[term][doc_id] = [] #attach the document ID and term together
                            self.index[term][doc_id].append((current_timestamp, 1)) #attach the current timestamp to the term and document 