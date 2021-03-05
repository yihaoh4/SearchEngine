import nltk, json
from collections import defaultdict

ps = nltk.stem.PorterStemmer()

def process_query(raw_query):
    return [ps.stem(token) for token in nltk.word_tokenize(raw_query)]

def rank(stemmed_query):
    ranking = defaultdict(float)
    for token in stemmed_query:
        query_data = data[token]
        for url in query_data:
            ranking[url] += query_data[url]
    return [url for url in sorted(ranking, key=ranking.get, reverse=True) if "#" not in url][:5]


if __name__ == "__main__":
    with open('/Users/YiHaoHuang/Desktop/college/ics/121/Assignment 3/analyst_inverted_index.json') as f:
        data = json.load(f)

    user_query = input("Search Up:")
    n = 1
    for result in rank(process_query(user_query)):
        print(n, result)
        n += 1
