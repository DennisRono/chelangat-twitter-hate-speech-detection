import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')
import seaborn as sns
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

#importing clean df
pickle_in = open("pickle/clean_df.pickle","rb")
clean_df = pickle.load(pickle_in)

#sentiment of tweets
# function to calculate polarity scores
pol = lambda x: analyser.polarity_scores(x)
# creating new column 'polarity' in clean_df
clean_df['polarity'] = clean_df['clean_tweets'].apply(pol)
# checking that worked
print(clean_df.head(2))

#parsing out polarity score
# dropping unessential columns
# and seperating out 'polarity' dictionary
df = pd.concat([clean_df.drop(['total_votes', 'hate_speech_votes', 'other_votes', 'tweet', 'polarity'], axis=1), clean_df['polarity'].apply(pd.Series)], axis=1)
print(df.head())

# new dataframe with average polarity score for each label
scores_df = df.groupby('label')['pos'].mean().reset_index(name='avg_positive')
scores_df['avg_neutral'] = df.groupby('label')['neu'].mean()
scores_df['avg_negative'] = df.groupby('label')['neg'].mean()
scores_df['avg_compound'] = df.groupby('label')['compound'].mean()

print(scores_df.head())

#visualizing distribution score
# creating dnsity plot for each label's polarity scores
plt.figure(figsize=(12, 8))
ax = sns.histplot(df['neg'][clean_df['label'] == 0], label='Not Hate Speech', color='green')
ax = sns.histplot(df['neg'][clean_df['label'] == 1], label='Hate Speech', color='red')
# setting label, title and legend
ax.set_title('Negativity of All Tweets', fontsize=20)
ax.set_ylabel('Density', fontsize=16)
ax.set_xlabel('Negativity Score', fontsize=16)
ax.legend(prop=dict(size=14))

plt.savefig('Visualizations/negativity_scores.png', bbox_inches = "tight", pad_inches=.5)
plt.show()

# creating dnsity plot for each label's polarity scores
plt.figure(figsize=(12, 8))
ax = sns.histplot(df['neu'][clean_df['label'] == 0], label='Not Hate Speech', color='orange')
ax = sns.histplot(df['neu'][clean_df['label'] == 1], label='Hate Speech', color='blue')
# setting label, title and legend
ax.set_title('Neutrality of All Tweets', fontsize=20)
ax.set_ylabel('Density', fontsize=16)
ax.set_xlabel('Neutrality Score', fontsize=16)
ax.legend(prop=dict(size=14))

plt.savefig('Visualizations/neutrality_scores.png', bbox_inches = "tight", pad_inches=.5)
plt.show()

# creating dnsity plot for each label's polarity scores
plt.figure(figsize=(12, 8))
ax = sns.histplot(df['pos'][clean_df['label'] == 0], label='Not Hate Speech', color='green')
ax = sns.histplot(df['pos'][clean_df['label'] == 1], label='Hate Speech', color='red')
# setting label, title and legend
ax.set_title('Positivity of All Tweets', fontsize=20)
ax.set_ylabel('Density', fontsize=16)
ax.set_xlabel('Positivity Score', fontsize=16)
ax.legend(prop=dict(size=14))

plt.savefig('Visualizations/positivity_scores.png', bbox_inches = "tight", pad_inches=.5)
plt.show()

# creating dnsity plot for each label's polarity scores
plt.figure(figsize=(12, 8))
ax = sns.histplot(df['compound'][clean_df['label'] == 0], label='Not Hate Speech', color='purple')
ax = sns.histplot(df['compound'][clean_df['label'] == 1], label='Hate Speech', color='blue')
# setting label, title and legend
ax.set_title('Compound Polarity Score of All Tweets', fontsize=20)
ax.set_ylabel('Density', fontsize=16)
ax.set_xlabel('Compound Score', fontsize=16)
ax.legend(prop=dict(size=14))

plt.savefig('Visualizations/compound_polarity_score.png', bbox_inches = "tight", pad_inches=.5)
plt.show()

#bar chart of sentiment scored by tweet type
# function to add percentage above each polarity score
def autolabel(rects):
    """Add a text label above bars to display its perentage of data."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:.3}'.format(height * 100) + '%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# setting labls and average scores
labels = ['Hate Speech', 'Not Hate Speech']
all_positivity = df['pos'].groupby(df['label']).mean()
all_neutrality = df['neu'].groupby(df['label']).mean()
all_negativity = df['neg'].groupby(df['label']).mean()

# set width of bars
width = 0.2  # the width of the bars
# set position of bar on x-axis
x = np.arange(len(labels))
r1 = x
r2 = [x + width for x in r1]
r3 = [x + width for x in r2]

# graph figure
fig, ax = plt.subplots(figsize=(8, 6))
# 3 types of grouped bar graphs
ax1 = ax.bar(r1, all_positivity, width, label='Positivity', color='green')
ax2 = ax.bar(r2, all_neutrality, width, label='Neutrality', color='purple')
ax3 = ax.bar(r3, all_negativity, width, label='Negativity', color='firebrick')

# applying percentage display function
autolabel(ax1)
autolabel(ax2)
autolabel(ax3)

# setting axis labels, title and legend location
ax.set_ylabel('Scores')
ax.set_title('Average Polarity Scores by Tweet Type')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.savefig('Visualizations/avg_polarity_by_tweet_type.png', bbox_inches = "tight", pad_inches=.5)
plt.show()

