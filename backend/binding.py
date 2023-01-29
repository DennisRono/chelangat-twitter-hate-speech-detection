import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def hateanalyze(tweet):
    # # removing punctuation
    tweet = re.sub(r'[%s]' % re.escape(string.punctuation), '', str(tweet))
    #     # tokenizing
    tokens =word_tokenize(tweet)
    # #remove stopwords
    stop_words = set(stopwords.words('english','swahili'))
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in stop_words]
    #     # taking root word
    lemmatizer = WordNetLemmatizer() 
    lemmatized_output = []
    for word in stopwords_removed:
        lemmatized_output.append(lemmatizer.lemmatize(word))
    
    #instantiating  vectorizer
    vectorizer = pickle.load(open('models/vect.pkl', 'rb'))
    X_test = lemmatized_output
    X_test_tfidf = vectorizer.transform(X_test)

    # vect = TfidfVectorizer(stop_words= stop_words, lowercase= False, dtype= str)
    # X_train_tfidf = pickle.load(open('models/X_train_tfidf.pkl', 'rb'))
    # vect.fit(X_train_tfidf)
    # X_test = lemmatized_output
    # X_test_tfidf = vect.transform(X_test)
   
   # loading in model
    final_model = pickle.load(open('models/knn.pkl', 'rb'))
# apply model to make predictions
    prediction = final_model.predict(X_test_tfidf[0])

    if prediction == 0:
        return {'result': 'not hate speech', 'hate':'false'}
    else:
        return {'result': 'hate speech', 'hate':'true'}

def sentiment_analysis(tweet):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_dict = analyzer.polarity_scores(tweet)
    if sentiment_dict['compound'] >= 0.05:
        category = "Positive ✅"
    elif sentiment_dict['compound'] <= -0.05:
        category = "Negative 😢"
    else:
        category = "Neutral ✔️"
    return {'status':category, 'dictionary':sentiment_dict}
