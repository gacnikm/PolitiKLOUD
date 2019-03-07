import os
import pickle
import argparse

import matplotlib

#interactive, wants tkinter, we do not have it
matplotlib.use('agg')

from wordcloud import WordCloud
from settings import STRANKE, PROCESSED_DATA_PATH, WORD_CLOUD_PATH

parser = argparse.ArgumentParser()
parser.add_argument("stranka", choices=STRANKE,
                    help="izberi stranko")

args = parser.parse_args()
STRANKA = args.stranka
wordcloud = WordCloud(width=1600, height=900, max_words=30)

with open(os.path.join(PROCESSED_DATA_PATH,'%s_all.pickle'%(STRANKA,)), 'rb') as inputfile:
    p = pickle.load(inputfile)

    wordcloud = wordcloud.generate_from_frequencies(p)
    wordcloud.to_file(os.path.join(WORD_CLOUD_PATH,'%s_all.png'%(STRANKA,)))


with open(os.path.join(PROCESSED_DATA_PATH,'%s_lemmatized.pickle'%(STRANKA,)), 'rb') as inputfile:
    p = pickle.load(inputfile)

    wordcloud = wordcloud.generate_from_frequencies(p)
    wordcloud.to_file(os.path.join(WORD_CLOUD_PATH, '%s_lemmatized.png' % (STRANKA,)))

with open(os.path.join(PROCESSED_DATA_PATH,'%s_ner.pickle'%(STRANKA,)), 'rb') as inputfile:
    p = pickle.load(inputfile)

    wordcloud = wordcloud.generate_from_frequencies(p)
    wordcloud.to_file(os.path.join(WORD_CLOUD_PATH, '%s_ner.png' % (STRANKA,)))