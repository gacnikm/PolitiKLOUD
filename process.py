import os
import pickle
import argparse
import nltk
import urllib.request
import json
from collections import Counter
from itertools import groupby
import time

import lemmagen.lemmatizer
from lemmagen.lemmatizer import Lemmatizer

from pajki.db import db,URL
from settings import DB_DATA_PATH, DATA_PATH, STRANKE, PROCESSED_DATA_PATH, NER_URL

parser = argparse.ArgumentParser()
parser.add_argument("stranka", choices=STRANKE,
                    help="izberi stranko")
parser.add_argument("-w","--words", action="store_true",
                    help="procesiraj samo besede")
parser.add_argument("-l","--lem",action="store_true",
                    help="procesiraj samo lematizacijo")
parser.add_argument("-n","--ner", action="store_true",
                    help="procesiraj samo NER")

args = parser.parse_args()
STRANKA = args.stranka
all = False if (args.words or args.lem or args.ner) else True

db.init(os.path.join(DB_DATA_PATH, '%s.sqlite'%(STRANKA,)))
db.connect()

lemmatizer = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)
stopwords = set([word.strip() for word in open(os.path.join(DATA_PATH,'stopwords.txt'),encoding='utf-8').readlines()])
stopwords = stopwords.union(set([word.strip() for word in open(os.path.join(DATA_PATH,'SloStopWords.txt'),encoding='utf-8').readlines()]))

all_words = []
lemmatized_words = []
ner_words = []

urls = URL.select()
cnt = urls.count()

def do_output(stranka, file, content):
    with open(os.path.join(PROCESSED_DATA_PATH, '%s_%s.pickle' % (stranka,file,)), 'wb') as outputfile:
        counter = Counter()
        for n in content:
            counter += n

        pickle.dump(counter, outputfile)

def do_ner(sentence):
    global ner_words
    words = []

    body = {'text': sentence}
    req = urllib.request.Request(NER_URL)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)

    for key, group in groupby(json.loads(response.read()), lambda tag: tag.get('tag', None)):
        if key in ["PERSON", "OTHER", "LOCATION"]:
            full_item = " ".join([tag['word'] for tag in group])
            words.append(full_item)
    return words

start = time.time()

for i,url in enumerate(URL.select()):
    text = url.content
    sent_text = nltk.sent_tokenize(text,'slovene')
    for sentence in sent_text:
        if args.ner or all:
            words = do_ner(sentence)
            ner_words.append(Counter(words))

        if args.words or args.lem or all:
            tokenized_text = nltk.word_tokenize(sentence)
            words = []
            lem_words = []
            for word in tokenized_text:
                word = word.lower()
                if word.isalpha() and (word not in stopwords):
                    if args.words or all:
                        words.append(word)
                    if args.lem or all:
                        lem_words.append(lemmatizer.lemmatize(word))

            if args.words or all:
                all_words.append(Counter(words))
            if args.lem or all:
                lemmatized_words.append(Counter(lem_words))

    if i%100==0:
        print("Processed",i,"elements")
        e = int(time.time() - start)
        print('{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

if args.words or args.lem or all:
    do_output(STRANKA,"all",all_words)

if args.lem or all:
    do_output(STRANKA,"lemmatized",lemmatized_words)

if args.ner or all:
    do_output(STRANKA,"ner",ner_words)