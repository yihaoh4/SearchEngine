# SearchEngine

**Indexer**
An inverted index for the corpus with data structures.
• Tokens: all alphanumeric sequences in the dataset.
• Stop words: no stop words.
• Stemming: Porter Stemming.
• Important text: text in bold (b, strong), in headings (h1, h2, h3), and
in titles are treated as more important than the in other places.

**Search**
This program will prompt the user for a query. At the time of the query,
the program will stem the query terms, look up the index, perform ranking
(see ranking below) and give out the ranked list of pages that are
relevant for the query, with the most relevant on top. Pages are identified
at least by their URLs.
• Ranking: tf-idf.
