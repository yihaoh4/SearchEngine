"""
The Indexer class will contain the inverted_index and a list of jsons file to be read through
"""
import os, glob, math, sys, json
from collections import defaultdict
from Token import Token


class Indexer:
    def __init__(self, directory):
        # directory: a str stating the path to a directory that contains json files
        # initiate an inverted_index to record all the tokenized json files
        self.json_files = glob.glob(directory+"/**/*.json", recursive=True)
        # self.json_files = [os.path.join(directory, item) for item in os.listdir(directory) if item.endswith('.json')]
        self.current = 0
        self.end = len(self.json_files)
        self.inverted_index = defaultdict(lambda: defaultdict(float))

    def read_json(self):
        # Read and tokenize all json until done
        while self.current != self.end:
            self.tokenize_json()
            self.current += 1

        for token in self.inverted_index:
            self.tf_idf(token)

        json_object = json.dumps(self.inverted_index, indent=4)
        with open("analyst_inverted_index.json", "w") as outfile:
            outfile.write(json_object)

    def tokenize_json(self):
        # Use Token Class on all json files
        current_token = Token(self.json_files[self.current])
        current_token.process()
        for token in current_token.token_counter.keys():
            self.inverted_index[token][current_token.url] = current_token.token_counter[token]

    def tf_idf(self, token):
        # Further steps of tf_idf
        df_t = len(self.inverted_index[token]) + 1
        log_N_df = math.log(self.end/df_t)
        for url in self.inverted_index[token]:
            self.inverted_index[token][url] *= log_N_df


    def __repr__(self):
        result = f"""Number of Document: {self.end}
Number of Unique Tokens: {len(self.inverted_index.keys())}
Size of Index: {sys.getsizeof(self.inverted_index)/1000} KB\n"""
        result += "{"
        for token in self.inverted_index.keys():
            result += token + ": {"
            for index, url in enumerate(self.inverted_index[token].keys()):
                if index != len(self.inverted_index[token].keys())-1:
                    result += f"{url}: {self.inverted_index[token][url]},\n"
                else:
                    result += f"{url}: {self.inverted_index[token][url]}"
            result += "}\n"
        return result + "}"

if __name__ == "__main__":
    paths = "/Users/YiHaoHuang/Desktop/college/ics/121/Assignment 3/ANALYST"
    test = Indexer(paths)
    test.read_json()
    print(test)

