import nltk
import re
import string

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