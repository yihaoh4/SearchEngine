import nltk
import PorterStemmer
import json
import os
from bs4 import BeautifulSoup
import re
from collections import defaultdict

# nltk.download('punkt')
ps = nltk.stem.PorterStemmer()


def open_file(dir):
        # dir --> paths = '/Users/YiHaoHuang/Desktop/college/ics/121/Assignment 3/ANALYST/www-db_ics_uci_edu'#
        json_files = [j for j in os.listdir(dir) if j.endswith('.json')]
        test = json_files[0]

        with open(os.path.join(paths, test)) as json_file:
                json_text = json.load(json_file)

        return json_text['url'], BeautifulSoup(json_text['content'], "lxml")

def find_important(clean_json):
        ### FIND IMPORTANT WORDS AND RECORD THEM ###
        important = clean_json.find_all(['h1', 'h2', 'h3', 'b'])
        stemmed_x = []
        for x in important:
                # clean_x = BeautifulSoup(str(x), "lxml")
                x = str(x).replace('<b>', '')
                x = x.replace('</b>', '')
                x = nltk.word_tokenize(x)
                stemmed_x.extend([ps.stem(word) for word in x if len(word) > 1 and word not in ("''", '``')])
        return stemmed_x

def find_email(clean_json):
        #### RECORD EMAIL ####
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", clean_json.text)
        for email in emails:
                clean_json = clean_json.text.replace(email, "")
        return clean_json, emails

def tokenize(clean_json):
        ### TOKENIZE AND STEM THE TEXT
        tokens = nltk.word_tokenize(clean_json)
        stemmed = [ps.stem(word) for word in tokens if len(word) > 1]
        return stemmed

def index_tokens(url, tokens, important, emails):
        #important words get more points
        token_counter = defaultdict(int)
        tokens.extend(important)
        tokens.extend(emails)
        for token in tokens:
                token_counter[token] += 1
        #
        # inverted_index = defaultdict(lambda: defaultdict(int))
        # for token in tokens:
        #         inverted_index[token][url] = token_counter[token]
        #
        # return inverted_index

if __name__ == "__main__":
        paths = '/Users/YiHaoHuang/Desktop/college/ics/121/Assignment 3/ANALYST/www-db_ics_uci_edu'
        url, text = open_file(paths)
        important_word = find_important(text)
        print(important_word)
        text, emails = find_email(text)
        print(emails)
        tokens = tokenize(text)
        print(tokens)
        dicct = index_tokens(url, tokens, important_word, emails)
        print(dicct)