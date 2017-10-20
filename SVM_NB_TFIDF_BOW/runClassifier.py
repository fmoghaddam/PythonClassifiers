import util
import sklearn.datasets
import sklearn.metrics
import sklearn.cross_validation
import sklearn.svm
import sklearn.naive_bayes
import sklearn.neighbors
from colorama import init
from termcolor import colored
import sys
import os
import glob
import cPickle
import numpy as np
from nltk.corpus import words
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score

def main(dataPath=None,classifier='SVM_LINEAR',encoding='TFIDF',cvFlag=False,testPercentage=0.2,fold=5):
    init()    
    pathForDataset = dataPath
    # remove any newlines or spaces at the end of the input
    path = pathForDataset.strip('\n')
    if path.endswith(' '):
        path = path.rstrip(' ')

    main_test(path,classifier,encoding,cvFlag,testPercentage,fold)

def main_test(path=None,classifier='SVM_LINEAR',encoding='TFIDF',cvFlag=False,testPercentage=0.2,fold=5):

    dir_path = path or 'dataset'  
    # load data
    print colored('Loading files into memory', 'green', attrs=['bold'])
    files = sklearn.datasets.load_files(dir_path)
   
    # refine all emails
    print colored('Refining all files', 'green', attrs=['bold'])
    util.refine_all_emails(files.data)

    # calculate the BOW representation
    print colored('Calculating BOW', 'green', attrs=['bold'])
    word_counts = util.bagOfWords(files.data)    
    
    if encoding in ["BOW"]:
        X = word_counts
    elif encoding=='TFIDF':
        # TFIDF
        print colored('Calculating TFIDF', 'green', attrs=['bold'])        
        word_list = words.words()
        word_list = list(set(word_list))        
        stop_words = stopwords.words('english')
        vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(vocabulary=word_list,stop_words = stop_words)
        X = vectorizer.fit_transform(files.data)          

    if classifier=='SVM_LINEAR':    
        clf = sklearn.svm.LinearSVC()        
    elif classifier=='NB':
        clf = sklearn.naive_bayes.MultinomialNB()
    elif classifier=='SVM_KERNEL':
        clf = sklearn.svm.SVC(kernel='poly',decision_function_shape='ovr')
    elif classifier=='KNN':
        n_neighbors = 10
        weights = 'uniform'
        weights = 'distance'
        clf = sklearn.neighbors.KNeighborsClassifier(n_neighbors, weights=weights)

    print colored('Configuration = '+classifier +' '+encoding +' CV='+cvFlag, 'magenta', attrs=['bold'])        
    print colored('Testing classifier with train-test split', 'magenta', attrs=['bold'])    
    if cvFlag == 'True':
        kfold_cross_validation(X, files.target, clf, test_size=float(testPercentage), y_names=files.target_names, confusion=False,kfold=int(fold))        
    else:   
        cross_validation(X, files.target, clf, test_size=float(testPercentage), y_names=files.target_names, confusion=False)                

def kfold_cross_validation(X, y, clf, test_size=0.2, y_names=None, confusion=False,kfold=5):
    scores = sklearn.model_selection.cross_val_score(clf, X, y, cv=kfold,n_jobs=-1)
    print "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)    

def cross_validation(X, y, clf, test_size=0.4, y_names=None, confusion=False):    
    print 'test size is: %2.0f%%' % (test_size * 100)    
    X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X, y, test_size=test_size)
    clf.fit(X_train, y_train)

    y_predicted = clf.predict(X_test)
    
    print "accuracy= " + str(accuracy_score(y_test, y_predicted))

def saveModel(name,clf):
    with open(name, 'wb') as fid:
        cPickle.dump(clf, fid)

def loadModel(name,clf):
    with open(name, 'rb') as fid:
        clf = cPickle.load(fid)

def saveTFIDF(name,vectorizer):
    with open(name, 'wb') as fid:
        cPickle.dump(vectorizer, fid)

def loadTFIDF(name):
    with open(name, 'rb') as fid:
        vectorizer = cPickle.load(fid)
        return vectorizer

if __name__ == '__main__':
    dataPath = sys.argv[1]
    classifier = sys.argv[2]
    encoding = sys.argv[3]
    cvFlag = sys.argv[4]
    testPercentage = sys.argv[5]
    if cvFlag=='True':    
        fold = sys.argv[6]
        main(dataPath,classifier,encoding,cvFlag,testPercentage,fold)
    else:
        main(dataPath,classifier,encoding,cvFlag,testPercentage,5)
