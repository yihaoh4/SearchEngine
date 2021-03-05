"""
The Token class will tokenize a json file including calculating the tf-idf score
"""

import nltk, re, json
from bs4 import BeautifulSoup
from collections import defaultdict

# Uncomment for running the first time
nltk.download("punkt")
ps = nltk.stem.PorterStemmer()


class Token:

    def __init__(self, path):
        with open(path) as json_path:
                self.content = json.load(json_path)
        self.url = self.content["url"]
        self.cleaned_content = BeautifulSoup(self.content["content"].lower(), "html.parser")
        self.stemmed_important_tokens = []
        self.stemmed_tokens = []
        self.token_counter = defaultdict(float)
        self.emails = []
        self.total_count = 0

    def process(self):
        self.find_important_words()
        self.find_email()
        self.tokenize()
        self.stemmed_tokens.extend(self.emails)
        # This return a token counter with its tf socre
        for token in self.token_counter:
            self.token_counter[token] = self.tf(token)
        # All important token (i.e) those in headings and bold get 1.1 time weight
        for token in self.stemmed_important_tokens:
            self.token_counter[token] *= 1.1

    def find_important_words(self):
        # Record all the words within h1, h2, h3 and b markup
        # These words will weigh more
        important_text = self.cleaned_content.find_all(["h1", "h2", "h3", "b"])
        for sentence in important_text:
            sentence = self.remove_markup(str(sentence))
            tokens = nltk.word_tokenize(sentence)
            self.stemmed_important_tokens.extend([ps.stem(token) for token in tokens if len(token) > 1 and token not in ("''", "``")])

    def find_email(self):
        # Record all the emails within h1, h2, h3 and b markup
        self.emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", self.cleaned_content.text)
        for email in self.emails:
            self.cleaned_content.text.replace(email, "")

    def tokenize(self):
        # Tokenize and stem the words
        tokens = nltk.word_tokenize(self.cleaned_content.text)
        self.stemmed_tokens = [ps.stem(token) for token in tokens if len(token) > 1 and token not in ("''", "``")]

        # Token counter. Will because the tf score for each token later
        for token in self.stemmed_tokens:
            self.token_counter[token] += 1
        self.total_count = len(self.stemmed_tokens) + len(self.emails)

    def remove_markup(self, sentence):
        markups = ["<h1>", "</h1>", "<h2>", "</h2>", "<h3>", "</h3>", "<b>", "</b>"]
        for tag in markups:
            removed = sentence.replace(tag, "")
        return removed

    def tf(self, token):
        # first step of tf-idf score
        return self.token_counter[token] / self.total_count