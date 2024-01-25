import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO

import pandas as pd
import numpy as np
import os
import regex as re
import nltk
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet 
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import random
from random import shuffle
from collections import OrderedDict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text


def misc_cleaning(text):
    text = re.sub('\n', ' ', text)
    text = re.sub('√¢¬Ä¬¢', ' ', text)
    text = re.sub('√¢¬ù¬ñ', ' ', text)
    text = re.sub('○␣', ' ', text)
    text = re.sub(" rt ", " ", text)
    text = re.sub("@\S+", "", text)
    text = re.sub(' y ', '', text) # gets rid of random y accent stuff scattered through the text
    text = re.sub('yyy', 'y', text)
    text = re.sub('\n', '', text)
    text = text.replace("("," ").replace(")"," ")
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub(' +', ' ', text)
    return text

def tokenize_text(text):
    return [w for s in sent_tokenize(text) for w in word_tokenize(s)]

def clean_text(text, remove_punctuation = False, stem_text = False, 
               remove_stopwords = False, remove_num = False):
        default_stemmer = PorterStemmer()
        default_stopwords = stopwords.words('english') # or any other list of your choice
        default_stopwords = list(string.ascii_lowercase) + default_stopwords
        text = " " + text + " "
        text = text.lower()
        text = misc_cleaning(text) # look at function, random cleaning stuff
        # removes punctuation
        if remove_punctuation:
            text = "".join([(ch if ch not in string.punctuation else " ") for ch in text]).strip()
        # optional: stems text using Porter Stemmer
        if stem_text:
            stemmer = default_stemmer
            tokens = tokenize_text(text)
            text = " ".join([stemmer.stem(t) for t in tokens])
        # removes stop words such as "a", "the", etc.
        if remove_stopwords:
            stop_words = default_stopwords
            tokens = [w for w in tokenize_text(text) if w not in stop_words]
            text = " ".join(tokens)
        # optional: removes numbers completely from the ext
        if remove_num:
            text=text.split()
            text=[x for x in text if not x.isnumeric()]
            text= " ".join(text)
        text = " " + text + " "
        text = _reduce_redundancy(text)
        
        return text


def _reduce_redundancy(text):
    """
    Takes in text that has been cleaned by the _base_clean and uses set to reduce the repeating words
    giving only a single word that is needed.
    """
    words = text.split(' ')
    return " ".join(list(set(words)))


## Similarity Functions

def calculate_jaccard(word_tokens1, word_tokens2):
    # Combine both tokens to find union.
    both_tokens = word_tokens1 + word_tokens2
    union = set(both_tokens)
    # Calculate intersection.
    intersection = set()
    for w in word_tokens1:
        if w in word_tokens2:
            intersection.add(w)
    jaccard_score = len(intersection)/len(union)
    return jaccard_score


def jaccard_similarity(resume_dictionary):
    base_resume = list(resume_dictionary.values())[0]
    other_resumes = list(resume_dictionary.values())[1:]
    score_dictionary = {}
    highest_individual = None
    highest_score = 0
    for i, other in enumerate(other_resumes):
        score = calculate_jaccard(base_resume.split(' '), other.split(' '))
        score_dictionary[list(resume_dictionary.keys())[i+1]] = score
        if score > highest_score:
            highest_score = score
            highest_individual = list(resume_dictionary.keys())[i+1]
    return score_dictionary, highest_individual


def process_tfidf_similarity(resume_dictionary):
    # First key of dictionary should b resume of comparison
    documents = list(resume_dictionary.values())
    vectorizer = TfidfVectorizer()
    # To make uniformed vectors, both documents need to be combined first.
    embeddings = vectorizer.fit_transform(documents)
    cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()
    score_dictionary = {}
    highest_individual = None
    highest_score = 0
    for i, score in enumerate(cosine_similarities):
        score_dictionary[list(resume_dictionary.keys())[i+1]] = score
        if score > highest_score:
            highest_score = score
            highest_individual = list(resume_dictionary.keys())[i+1]
    return score_dictionary, highest_individual


def find_match(fname, lname, fpass_users):
    pass