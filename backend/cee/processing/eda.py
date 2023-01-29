#perform on clean data before modelling
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
plt.style.use('bmh')
# NLP libraries
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
#from matplotlib_venn import venn2
import matplotlib.pyplot as plt
from wordcloud import WordCloud
#import stylecloud
import pickle

# loading in clean_df
pickle_in = open("pickle/clean_df.pkl","rb")
clean_df = pickle.load(pickle_in)
print(clean_df.head(3))



#censoring words
replacements = { 'bitch':'b**ch', 'bitches':'b**ches', 'nigga':'n***a', 'nigger':'ni**er', 'ass':'a**', 'hoe':'h**', 'hoes':'h**s', 'faggot':'fa***t', 'faggots':'fa***ts', 'fuck':'f**k','fucking':'f**king', 'pussy':'p**sy', 'fag':'f**', 'shit':'sh*t' }

for k, v in replacements.items():
    clean_df['clean_tweets'] = clean_df['clean_tweets'].str.replace(k, v)

# checking that worked
print(clean_df.head(3))

# creating new dfs for each classification
df_freq_hate = clean_df[clean_df['label']==1]
df_freq_not_hate = clean_df[clean_df['label']==0]

# pulling out the text data for cleaned tweets
data_hate = df_freq_hate['clean_tweets']
data_not_hate = df_freq_not_hate['clean_tweets']

# function to tokenize tweets and remove stop words with NLTK built-in library
stop_words = set(stopwords.words('english'))
def process_tweet(text):
    tokens = nltk.word_tokenize(text)
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in stop_words]
    return stopwords_removed 

# creating lists for processed hate & not hate data
process_hate = list(map(process_tweet, data_hate))
process_not_hate = list(map(process_tweet, data_not_hate))

# exact amount of hate speech
total_vocab_hate = set()
for comment in process_hate:
    total_vocab_hate.update(comment)
print("amount of hate speech", len(total_vocab_hate))

# exact amount of not hate speech
total_vocab_NOT_hate = set()
for comment in process_not_hate:
    total_vocab_NOT_hate.update(comment)
print("amount of not hate speech", len(total_vocab_NOT_hate))

#most common words for each category
flat_hate = [item for sublist in process_hate for item in sublist]
flat_not_hate = [item for sublist in process_not_hate for item in sublist]

hate_freq = FreqDist(flat_hate)
not_hate_freq = FreqDist(flat_not_hate)
# Top 20 Hate Speech words:
print(hate_freq.most_common(20))

print(not_hate_freq.most_common(20))

#normalizing word frequency
hate_total_word_count = sum(hate_freq.values())
hate_top_25 = hate_freq.most_common(25)
print("Hate Word \t Normalized Frequency")
print()
for word in hate_top_25:
    normalized_frequency = word[1]/hate_total_word_count
    print("{} \t\t {:.4}".format(word[0], normalized_frequency))

not_hate_total_word_count = sum(not_hate_freq.values())
not_hate_top_25 = not_hate_freq.most_common(25)
print("Not Hate Word \t Normalized Frequency")
print()
for word in not_hate_top_25:
    normalized_frequency = word[1]/not_hate_total_word_count
    print(":{} \t\t {:.4}".format(word[0], normalized_frequency))


#visualizing top word frequencies
# create counts of hate and not hate with values and words
hate_bar_counts = [x[1] for x in hate_freq.most_common(20)]
hate_bar_words = [x[0] for x in hate_freq.most_common(20)]

not_hate_bar_counts = [x[1] for x in not_hate_freq.most_common(20)]
not_hate_bar_words = [x[0] for x in not_hate_freq.most_common(20)]

# set the color of the bar graphs
color = cm.magma(np.linspace(.4,.8, 30))

new_figure = plt.figure(figsize=(14,6))

ax = new_figure.add_subplot(121)
ax.invert_yaxis()

ax2 = new_figure.add_subplot(122)
ax2.invert_yaxis()

# generating a bar chart on each axes
ax.barh(hate_bar_words, hate_bar_counts, color=color)
ax2.barh(not_hate_bar_words, not_hate_bar_counts, color=color)

ax.title.set_text('Hate Speech')
ax2.title.set_text('Not Hate Speech')

for ax in new_figure.axes:
    plt.sca(ax)
    plt.xticks(rotation=60, fontsize=14)
    plt.xlabel("Word Count")
    plt.yticks(fontsize=14)
plt.tight_layout(pad=2)

new_figure.suptitle('Top 20 Most Frequent Words per Label', fontsize=16)

plt.savefig('Visualizations/label_word_count_y.png', bbox_inches = "tight", pad_inches=.5)
plt.show()

#check the words unique to hate speech label are threanening or especially degrading
def returnNotMatches(a, b):
    return [x for x in a if x not in b]

print(returnNotMatches(flat_hate, flat_not_hate))

#visualizing unique word with venn diagram

#venn2([set(flat_hate), set(flat_not_hate)], set_labels = ('Hate Speech', 'Not Hate Speech'), set_colors =('purple','skyblue'))
#plt.title('Comparison of Unique Words in Each Corpus Label')
#plt.savefig('Visualizations/word_venn.png', bbox_inches = "tight", pad_inches=.5)
#plt.show()

#wordcloud
hate_dict = dict(zip(hate_bar_words, hate_bar_counts))
not_hate_dict = dict(zip(not_hate_bar_words, not_hate_bar_counts))

# create the word cloud:
wordcloud = WordCloud(colormap='Spectral').generate_from_frequencies(hate_dict)

# Display the generated image w/ matplotlib:
plt.figure(figsize=(6,6), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)

plt.savefig('Visualizations/satire_wordcloud.png')

plt.show()

wordcloud = WordCloud(colormap='Spectral').generate_from_frequencies(not_hate_dict)

plt.figure(figsize=(6,6), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('Visualizations/not_satire_wordcloud.png')

plt.show()

#stylecloud.gen_stylecloud(
                         #file_path = 'D:\chelangat\scr/corpus.txt', 
                         #icon_name= 'fab fa-twitter', 
                         #collocations=False,
                         #palette='colorbrewer.sequential.Blues_5',
                         #output_name = 'icon_cloud.png',
                         #background_color='white')

#plt.savefig('Visualizations/icon_cloud.png')
#plt.show()
#crowd flower votes
print(clean_df.head(3))
# distribution of vote counts for hate_speech_votes
clean_df.hate_speech_votes.hist()
plt.savefig('Visualizations/hatespeech_votes.png')
plt.show()
# distribution of vote counts for other_votes
clean_df.other_votes.hist()
plt.savefig('Visualizations/other_votes.png')
plt.show()

#EDA on total votes column
clean_df.total_votes.hist()
plt.savefig('Visualizations/total_votes.png')
plt.show()

