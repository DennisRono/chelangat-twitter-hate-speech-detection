import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns; sns.set()
from wordcloud import WordCloud

# packages for NLP preprocessing
import nltk
from sklearn.feature_extraction import text 
from nltk.stem import WordNetLemmatizer 
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle
import collections
from collections import Counter

# showing the whole tweet column
pd.set_option('max_colwidth', 280)

# importing raw tweets before they were cleaned
pickle_in = open("pickle/raw_tweets.pickle","rb")
raw_df = pickle.load(pickle_in)

print(raw_df.head(2))

#filtering out hashtags from raw tweets
raw_df['hashtags'] = raw_df['tweet'].str.extract('([^&]#[\w]+)', expand=False).str.strip()
print(raw_df.head(2))
print(raw_df.shape)
print(raw_df.hashtags.isna().sum())

# dropping tweet rows with no hashtags
raw_df.dropna(inplace=True)
print(raw_df.shape)
raw_df.reset_index(inplace=True)

#new df with essential columns
hashtags_df = raw_df[['label', 'hashtags']].copy()
print(hashtags_df.head())

#removing any character before#
hashtags_df['hashtags_2'] = hashtags_df['hashtags'].str.extract('(#[\w]+)', expand=False).str.strip()
print(hashtags_df.head())

# # iteratiively censoring words
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('faggots','f**gots')
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('faggot','f**got')
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('shittmybosssays','s**tmybosssays')
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('hesgay','hesg*y')
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('pussy','p**sy')
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('bitch','b**ch')
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('redskins','r**skins')
# hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace('hoe','h*e')

replacements = { 'bitch':'b**ch', 'bitches':'b**ches', 'nigga':'n***a', 'nigger':'ni**er', 'ass':'a**', 'hoe':'h**', 'hoes':'h**s', 'faggot':'fa***t', 'faggots':'fa***ts', 'fuck':'f**k','fucking':'f**king', 'pussy':'p**sy', 'fag':'f**', 'shit':'sh*t', 'hesgay':'hesg*y','redskins':'r**skins',}

for k, v in replacements.items():
    hashtags_df['hashtags_2'] = hashtags_df['hashtags_2'].str.replace(k, v)

# creating new dfs for each classification
# hate speech
df_freq_hate = hashtags_df[hashtags_df['label']==1]
# not hate speech
df_freq_not_hate = hashtags_df[hashtags_df['label']==0]

# pulling out the hashtags column for raw tweets
hashtag_hate = df_freq_hate['hashtags_2']
hashtag_not_hate = df_freq_not_hate['hashtags_2']

# exact amount of hashtags in hate speech
total_vocab_hate = set()
for comment in hashtag_hate:
    total_vocab_hate.update(comment)
print(len(total_vocab_hate))

# exact amount of hashtags in not hate speech
total_vocab_NOT_hate = set()
for comment in hashtag_not_hate:
    total_vocab_NOT_hate.update(comment)
print(len(total_vocab_NOT_hate))



# list of all words across hate speech tweets
df_hate_count = list(df_freq_hate['hashtags_2'])
# create counter
hate_hashtag = collections.Counter(df_hate_count)
# top 10 hate speech tweet hashtags
print(hate_hashtag.most_common(25))

# list of all words across NON hate speech tweets
df_not_hate_count = list(df_freq_not_hate['hashtags_2'])
# create counter
not_hate_hashtag = collections.Counter(df_not_hate_count)
# top 10 hate speech tweet hashtags
print(not_hate_hashtag.most_common(25))

#frequency distribution graph
# create counts of hate and not hate with values and words
hate_bar_counts = [x[1] for x in hate_hashtag.most_common(25)]
hate_bar_words = [x[0] for x in hate_hashtag.most_common(25)]

not_hate_bar_counts = [x[1] for x in not_hate_hashtag.most_common(25)]
not_hate_bar_words = [x[0] for x in not_hate_hashtag.most_common(25)]

# set the color of the bar graphs
color = cm.viridis_r(np.linspace(.4,.8, 30))

# top 25 hashtags for each label
new_figure = plt.figure(figsize=(16,4))

ax = new_figure.add_subplot(121)
ax2 = new_figure.add_subplot(122)
# generating a bar chart on each axes
ax.bar(hate_bar_words, hate_bar_counts, color=color)
ax2.bar(not_hate_bar_words, not_hate_bar_counts, color=color )

ax.title.set_text('Hate Speech')
ax2.title.set_text('Not Hate Speech')

for ax in new_figure.axes:
    plt.sca(ax)
    plt.xticks(rotation=60)
plt.tight_layout(pad=0)

plt.savefig('Visualizations/word count bar graphs.png')
plt.show()

#wordcloud
hate_dict = dict(zip(hate_bar_words, hate_bar_counts))
not_hate_dict = dict(zip(not_hate_bar_words, not_hate_bar_counts))

# create the word cloud for hate speech
hate_wordcloud = WordCloud(colormap='Dark2', background_color='white', random_state=16).generate_from_frequencies(hate_dict)

# Display the generated image w/ matplotlib:
plt.figure(figsize=(6,6), facecolor='k')
plt.imshow(hate_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)

plt.savefig('Visualizations/satire_wordcloud.png')

plt.show()

# create the word cloud for NOT hate speech
not_hate_wordcloud = WordCloud(colormap='Dark2', background_color='white', random_state=16).generate_from_frequencies(not_hate_dict)

plt.figure(figsize=(6,6), facecolor='k')
plt.imshow(not_hate_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('Visualizations/not_satire_wordcloud.png')

plt.show()

#joining word clouds
# new figure
f = plt.figure(figsize=(10,8))

# hate speech word cloud
f.add_subplot(1,2, 1)
plt.imshow(hate_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Hate Speech', fontsize=18)

# not hate speech word cloud
f.add_subplot(1,2, 2)
plt.imshow(not_hate_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Not Hate Speech', fontsize=18)

# setting spacing between graphs
plt.tight_layout(pad=3)

plt.savefig('Visualizations/censored_top_hashtags.png', bbox_inches = "tight", pad_inches=.5)
plt.show()

