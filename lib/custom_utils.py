import nltk
import re
import string
import datetime
import pandas as pd

nltk.download('stopwords')
cachedStopWords = nltk.corpus.stopwords.words("english")
punct = set(string.punctuation)

def prep_text_for_wordcloud(txt):
    # lower case
    txt = txt.lower()

    # remove any punctuation
    txt = ''.join(ch for ch in txt if ch not in punct)

    # remove stopwords
    txt = ' '.join([word for word in txt.split() if word not in cachedStopWords])

    # remove numbers
    txt = ''.join([ch for ch in txt if not ch.isdigit()])

    # remove extra spaces
    txt = re.sub(' +', ' ', txt)

    # return word frequencies
    return txt

def get_semester_asana(df, code):
    year = '20'+code[-2:]
    if 's' in code:
        start_date = datetime.datetime.strptime(year+'-01-20', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(year+'-05-15', '%Y-%m-%d')
    else:
        start_date = datetime.datetime.strptime(year+'-09-01', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(year+'-12-22', '%Y-%m-%d')
    
    return df[(df['Created At'] > start_date) & (df['Created At'] < end_date)]