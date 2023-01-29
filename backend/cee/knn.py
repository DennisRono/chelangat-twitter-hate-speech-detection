import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.feature_extraction import text 
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
from imblearn.over_sampling import SMOTE
from collections import Counter
from imblearn.under_sampling import TomekLinks # doctest: +NORMALIZE_WHITESPACE

#import X and Y from process.py
# importing x and y from nlp preprocessing
pickle_in = open("pickle/X_lem.pkl", "rb")
X_lem = pickle.load(pickle_in)

pickle_in = open("pickle/y_lem.pkl", "rb")
y_lem = pickle.load(pickle_in)


# setting up stop words
stop_words = set(stopwords.words('english', 'swahili'))

# Train_split test
X_train, X_test, y_train, y_test = train_test_split(
    X_lem, y_lem, test_size=0.20, random_state=15)

# using tf_idf vectorizor with bigrams
tfidf = TfidfVectorizer(stop_words= stop_words, ngram_range=(1,2))
# sparse matrix format with 265K stored elements
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


# taking a quick look at the non zero elements
non_zero_cols = X_train_tfidf.nnz / float(X_train_tfidf.shape[0])
print("Average Number of Non-Zero Elements in Vectorized Articles: {}".format(non_zero_cols))
percent_sparse = 1 - (non_zero_cols / float(X_train_tfidf.shape[1]))
print('Percentage of columns containing ZERO: {}'.format(percent_sparse))

## pickling X_train for future use
pickle_out = open("pickle/X_train.pkl","wb")
pickle.dump(X_train, pickle_out)
pickle_out.close()

## pickling tfidf_data_train for future use
pickle_out = open("pickle/tfidf.pkl","wb")
pickle.dump(tfidf, pickle_out)
pickle_out.close()

# joining them
#training = pd.concat([X_train_df, y_train_df], axis=1)
#print("training:", training.head(2))


#Knn parameters
knn = KNeighborsClassifier(n_neighbors=1, weights='distance', algorithm='brute', p=2, metric='cosine', metric_params=None, n_jobs=None)
knn.fit(X_train_tfidf, y_train)
knn_test_preds = knn.predict(X_test_tfidf)

knn_precision = precision_score(y_test, knn_test_preds)
knn_recall = recall_score(y_test, knn_test_preds)
knn_f1_score = f1_score(y_test, knn_test_preds)
knn_weighted_f1_score = f1_score(y_test, knn_test_preds, average='weighted')
knn_accuracy_score = accuracy_score(y_test, knn_test_preds)

# printing evaluation metrics up to 4th decimal place
print('Testing Metrics for Knearest Neighbor with Lemmatization & TF-IDF Vectorization')
print('Precision: {:.4}'.format(knn_precision))
print('Recall: {:.4}'.format(knn_recall))
print('F1 Score: {:.4}'.format(knn_f1_score))
print('weighted_f1_score:{:.4}'.format(knn_weighted_f1_score))
print('Accuracy_score:{:.4}'.format(knn_accuracy_score))

# creating dictionary with all metrics
metric_dict = {}
metric_dict['Knearest Neighbor'] = {'precision': knn_precision, 'recall': knn_recall,
                                    'f1_score': knn_f1_score, 'weighted_f1': knn_weighted_f1_score}


mat = confusion_matrix(y_test, knn_test_preds)
print("confusion matrix", mat)

sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=['Hate Speech', 'Not Hate Speech'], yticklabels=['Hate Speech', 'Not Hate Speech'], cmap="Blues")
plt.xlabel('true label')
plt.ylabel('predicted label')
plt.title('Knearest Neighbor')

# fixing matplotlib heatmap cutoff issue
b, t = plt.ylim()  # discover the values for bottom and top
b += 0.5  # Add 0.5 to the bottom
t -= 0.5  # Subtract 0.5 from the top
plt.ylim(b, t)  # update the ylim(bottom, top) value
plt.show()
plt.savefig('visualization/knn_confusionmatrix.png', bbox_inches = "tight", pad_inches=.5)

#error_rate = []
 
#for i in range(1,40):
    
    #knn = KNeighborsClassifier(n_neighbors=i)
    #knn.fit(X_train_tfidf, y_train)
    #predict_i = knn.predict(X_test_tfidf)
    #print(error_rate)
    #error_rate.append(np.mean( predict_i != y_test))

#plt.figure(figsize=(10,6))
#plt.plot(range(1,40),error_rate,color='blue', linestyle='dashed', marker='o',
         #markerfacecolor='red', markersize=10)
#plt.title('Error Rate vs. K Value')
#plt.xlabel('K')
#plt.ylabel('Error Rate')
#plt.show()
#plt.savefig('visualization/Error Rate vs. K Value.png')



text = ["nini mbaya na hawa waluhya"]
inp = tfidf.transform(text)
print("output is", knn.predict(inp))
sm = SMOTE()
smote_X_train, smote_y_train = sm.fit_resample(X_train_tfidf, y_train)

smote_knn = KNeighborsClassifier( n_neighbors=1, weights='distance', algorithm='brute', p=2, metric='cosine', metric_params=None, n_jobs=None)
smote_knn.fit(smote_X_train, smote_y_train)
smote_knn_test_preds = smote_knn.predict(X_test_tfidf)


smote_precision = precision_score(y_test, smote_knn_test_preds)
smote_recall = recall_score(y_test, smote_knn_test_preds)
smote_f1_score = f1_score(y_test, smote_knn_test_preds)
smote_weighted_f1_score = f1_score(y_test, smote_knn_test_preds, average='weighted')
smote_accuracy_score = accuracy_score(y_test, smote_knn_test_preds)

# printing evaluation metrics up to 4th decimal place
print('Testing Metrics for Oversampled KNeighborsClassifier with Lemmatization Features')
print('Precision: {:.4}'.format(smote_precision))
print('Recall: {:.4}'.format(smote_recall))
print('F1 Score: {:.4}'.format(smote_f1_score))
print('Accuracy_score:{:.4}'.format(smote_accuracy_score))

metric_dict['KNeighborsClassifier Oversampled with SMOTE'] = {'precision': smote_precision, 'recall': smote_recall, 'f1_score': smote_f1_score,  'weighted_f1': smote_weighted_f1_score}

smote_mat = confusion_matrix(y_test, smote_knn_test_preds)
print("confusion matrix", smote_mat)

#KNN with Tomek Links
#to undersample the majority class
tl = TomekLinks()
tomek_X_train, tomek_y_train = tl.fit_resample(X_train_tfidf, y_train)
print('Resampled dataset shape %s' % Counter(tomek_y_train))

tomek_knn = KNeighborsClassifier(n_neighbors=1, weights='distance', algorithm='brute', p=2, metric='cosine', metric_params=None, n_jobs=None)

tomek_knn.fit(tomek_X_train, tomek_y_train)
tomek_knn_test_preds = tomek_knn.predict(X_test_tfidf)

tomek_precision = precision_score(y_test, tomek_knn_test_preds)
tomek_recall = recall_score(y_test, tomek_knn_test_preds)
tomek_f1_score = f1_score(y_test, tomek_knn_test_preds)
tomek_weighted_f1_score = f1_score(y_test, tomek_knn_test_preds, average='weighted')
tomek_accuracy_score = accuracy_score(y_test, tomek_knn_test_preds)

# printing evaluation metrics up to 4th decimal place
print('Testing Metrics for Undersampled KNeighborsClassifier with Lemmatization Features')
print('Precision: {:.4}'.format(tomek_precision))
print('Recall: {:.4}'.format(tomek_recall))
print('F1 Score: {:.4}'.format(tomek_f1_score))
print('Accuracy_score:{:.4}'.format(tomek_accuracy_score))

metric_dict['KNeighborsClassifier Undersampled with Tomek Links'] = {'precision': tomek_precision, 'recall': tomek_recall, 'f1_score': tomek_f1_score,  'weighted_f1': tomek_weighted_f1_score}

tomek_mat = confusion_matrix(y_test, tomek_knn_test_preds)
print("confusion matrix", tomek_mat)
#metric for all baselines
print(pd.DataFrame.from_dict(metric_dict, orient='index'))


# pickle_out = open("pickle/knn.pkl",'wb')
# pickle.dump(knn, pickle_out)
# pickle_out.close()
