# import libraries
# packages for data cleaning function
import pickle
import string
import re
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
pd.options.display.max_columns = 50
sns.set()
plt.style.use('bmh')

# load in data
df = pd.read_csv('HateSpeechKEN.csv', index_col=0)
print(df.head())

#Return unique values based on a hash table.
classes = ['Hate Speech','Offensive Language','Neither']
print("unique class", df['class'].unique())

# checking class imbalance of the original data labels
sns.set_theme(style="whitegrid")
sns.countplot(x=df['class']).set_title('Distribution of Class')

plt.savefig('Visualizations/class_imbalance.png',bbox_inches="tight", pad_inches=.5)
plt.show()

# creating new column labels for hatespeech
df['label'] = df['class'].replace(1, 0)
print(df.label.unique())

# changing hate speech to 1 and not hate speech to 0
df['label'] = df['label'].replace(0, 1)
df['label'] = df['label'].replace(2, 0)

print(df.label.unique())


# visualization
plt.figure(figsize=(10, 5))
ax = sns.countplot(x=df['label'])

ax.set_title('Amount of Tweets Per Label', fontsize=20)
ax.set_xlabel('Type of Tweet', fontsize=15)
ax.set_ylabel('Count', fontsize=15)
ax.set_xticklabels(['Not Hate Speech', 'Hate Speech'], fontsize=13,)

total = float(len(df))  # one person per row
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 3,
            '{:1.2f}'.format(height/total * 100) + '%',
            ha="center")

plt.savefig('Visualizations/cleaned_class_imbalance.png',bbox_inches="tight", pad_inches=.5)
plt.show()

# creating new clean dataset with renamed column
# changes to the dataset
# dropping the class column
# renaming count to total votes
# renaming hate speech to hate speech votes
# adding together offensive languages and neither to become other votes
# creating new dataframe `clean_df`

raw_df = df[['hate_speech', 'offensive_language','neither', 'tweet', 'label']].copy()

# renaming those columns
raw_df.rename(columns={'count':'total_votes','hate_speech':'hate_speech_votes' }, inplace=True)

# creating column for vote count for not hate speech tweets
raw_df['other_votes'] = raw_df['offensive_language'] + raw_df['neither']

# reordering the columns and dropping the old 'offensive_language' and 'neither' columns
raw_df = raw_df.reindex(columns=['total_votes', 'hate_speech_votes', 'other_votes', 'label', 'tweet'])

# checking that it all worked
print("rawdf", raw_df.head())

# pickling the raw tweets for later censored$uncensored
pickle_out = open("pickle/raw_tweets.pkl", "wb")
pickle.dump(raw_df, pickle_out)
pickle_out.close()

#pickle_in = open("pickle/raw_tweets.pickle", "rb")
#raw_df = pickle.load(pickle_in)



# cleaning tweets
# copying new `clean_df` and cleaning up the tweets
clean_df = raw_df.copy()
print("clean tweets", clean_df.head())

# function to clean all data


def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    # make text lowercase
    text = text.lower()
    # removing text within brackets
    text = re.sub(r'\[.*?\]', '', text)
    # removing text within parentheses
    text = re.sub(r'\(.*?\)', '', text)
    # removing numbers
    text = re.sub(r'\w*\d\w*', '', text)
    # if there's more than 1 whitespace, then make it just 1
    text = re.sub(r'\s+', ' ', text)
    # if there's a new line, then make it a whitespace
    text = re.sub(r'\n', ' ', text)
    # removing any quotes
    text = re.sub(r'\"+', '', text)
    # removing &amp;
    text = re.sub(r'(\&amp\;)', '', text)
    # removing any usernames
    text = re.sub(r'(@[^\s]+)', '', text)
    # removing any hashtags
    text = re.sub(r'(#[^\s]+)', '', text)
    # remove `rt` for retweet
    text = re.sub(r'(rt)', '', text)
    # string.punctuation is a string of all punctuation marks
    # so this gets rid of all punctuation
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    # getting rid of `httptco`
    text = re.sub(r'(httptco)', '', text)

    return text


def round1(x): return clean_text_round1(x)


# appling data cleaning function to `tweet` column
clean_df['clean_tweets'] = clean_df['tweet'].apply(round1)
# checking that it worked
print("cleantweets", clean_df.head())

# checking for missing values
print(clean_df.isnull().sum())
# pickling clean df for later use
pickle_out = open("pickle/clean_df.pkl", "wb")
pickle.dump(clean_df, pickle_out)
pickle_out.close()
