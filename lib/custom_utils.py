import nltk
import re
import string
import datetime
import pandas as pd
from wordcloud import WordCloud
import collections

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

def generate_wordcloud(txt):
    # prep text
    txt = prep_text_for_wordcloud(txt)

    # get word frequencies
    counts = dict(collections.Counter(txt.split()))

    # create wordcloud
    return WordCloud(background_color="white", max_words=100, margin=10,random_state=1).generate_from_frequencies(counts)


def to_unix_time(dt):
    epoch =  datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

def get_semester_date_range(code, unix_time=False):
    year = '20'+code[-2:]
    if 's' in code:
        start_date = datetime.datetime.strptime(year+'-01-20', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(year+'-05-15', '%Y-%m-%d')
    else:
        start_date = datetime.datetime.strptime(year+'-09-01', '%Y-%m-%d')
        end_date = datetime.datetime.strptime(year+'-12-22', '%Y-%m-%d')
        
    if unix_time:
        return [to_unix_time(start_date), to_unix_time(end_date)]
    else:
        return [start_date, end_date]

def get_semester_asana(df, code):
    start_date, end_date = get_semester_date_range(code)
    return df[(df['Created At'] > start_date) & (df['Created At'] < end_date)]

def get_semester_via_col(df, col, code):
    start_date, end_date = get_semester_date_range(code)
    return df[(df[col] > start_date) & (df[col] < end_date)]

def duration_to_delta(dur):
    dur = str(dur)
    
    # pad hours
    if len(dur.split(':')) != 3:
        dur = '00:'+dur
       
    # convert to datetime
    t = datetime.datetime.strptime(dur,"%H:%M:%S")
    
    # extract duration from datetime
    return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
