import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns; sns.set()

# packages for NLP preprocessing
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
#nltk.download('all')
from nltk.collocations import *
from nltk.stem import WordNetLemmatizer 
from nltk.probability import FreqDist
from nltk.corpus import stopwords

import pickle

#loading in the clean dataframe from datacleaning.py
# this is our corpus
pickle_in = open("pickle/clean_df.pkl","rb")
clean_df = pickle.load(pickle_in)
print(clean_df.head())

#creating tweets df with only cleaned tweets column
tweet_df = clean_df[['clean_tweets', 'label']].copy()
print(tweet_df.head())

data = tweet_df['clean_tweets']
target = tweet_df['label']


# function to tokenize without removing stop words
def unfiltered_tokens(text):
        dirty_tokens = nltk.word_tokenize(text)
        return dirty_tokens

  

# applying this function to the 'clean_tweets' column

unfilterd_data = list(map(unfiltered_tokens, data))

# morphing `unfiltered_data` into a readable list
flat_unfiltered = [item for sublist in unfilterd_data for item in sublist]

# getting frequency distribution
dirty_corpus_freqdist = FreqDist(flat_unfiltered)
# top 20 words in the corpus
print(dirty_corpus_freqdist.most_common(20))

#removing stopwords in tokenization
stop_words = set(stopwords.words('english'))
def process_tweet(text):
    tokens = nltk.word_tokenize(text)
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in stop_words]
    return stopwords_removed 

# applying the above function to our data/features 
processed_data = list(map(process_tweet, data))

total_vocab = set()
for comment in processed_data:
    total_vocab.update(comment)
len(total_vocab)



# morphing `processed_data` into a readable list
flat_filtered = [item for sublist in processed_data for item in sublist]
# getting frequency distribution
clean_corpus_freqdist = FreqDist(flat_filtered)
# top 20 words in cleaned corpus
print(clean_corpus_freqdist.most_common(20))

#lemmatization
# creating a list with all lemmatized outputs
lemmatizer = WordNetLemmatizer() 
lemmatized_output = []

for listy in processed_data:
    lemmed = ' '.join([lemmatizer.lemmatize(w) for w in listy])
    lemmatized_output.append(lemmed)

X_lem = lemmatized_output
y_lem = target


# creating bigrams
bigram_measures = nltk.collocations.BigramAssocMeasures()
# creating a finder & passing in tokenized corpus
bigram_finder = BigramCollocationFinder.from_words(flat_filtered)

# computing bigram scores
corpus_scored = bigram_finder.score_ngrams(bigram_measures.raw_freq)

# top 20 bigrams
print(corpus_scored[:20])


# Calculating mutual information scores
# most are nonsensical phrases that may indicate that the data is still dirty ,we can use mutual information scores to show the best biagrams
# creating a finder for pmi & passing in torkenized corpus
pmi_finder = BigramCollocationFinder.from_words(flat_filtered)

# applying frequency filter that only examines bigrams that occur more than 5 times
pmi_finder.apply_freq_filter(5)

# using finder to calculate pmi scores
pmi_scored = pmi_finder.score_ngrams(bigram_measures.pmi)

# first 30 elements in this list
print(pmi_scored[:30])

#We can implement the bigrams using ngram-range during the tdif vectorization stage
bigrams_list = pmi_scored[:30]
print(bigrams_list)


# visualizing bigram frequency
bigrams_series = (pd.Series(nltk.ngrams(flat_filtered, 2)).value_counts())[:20]
bigrams_series.sort_values().plot.barh(color=cm.viridis_r(np.linspace(.4,.8, 30)), width=.9, figsize=(12, 8))
plt.title('20 Most Frequently Occurring Bigrams', fontsize=18)
plt.ylabel('Bigram', fontsize=18)
plt.xlabel('Number of Occurances', fontsize=18)
plt.show()
plt.savefig('Visualizations/Bigram Frequency')

#converting list to df so that we can sensor the bigrams
bigrams_df = pd.DataFrame(bigrams_list,columns=['bigram', 'pmi_score'])
print(bigrams_df.head())

# pickling procesed_data for later use
pickle_out = open("pickle/processed_data.pkl",'wb')
pickle.dump(processed_data, pickle_out)
pickle_out.close()

# pickle these for modeling
pickle_out = open("pickle/X_lem.pkl",'wb')
pickle.dump(X_lem, pickle_out)
pickle_out.close()


pickle_out = open("pickle/y_lem.pkl",'wb')
pickle.dump(y_lem, pickle_out)
pickle_out.close()