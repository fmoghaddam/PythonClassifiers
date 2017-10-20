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

def main(datapath=None, classifier='SVM_LINEAR',encoding='TFIDF'):
    init()    
    pathForDataset = datapath
    # remove any newlines or spaces at the end of the input
    path = pathForDataset.strip('\n')
    if path.endswith(' '):
        path = path.rstrip(' ')

    main_test(path,classifier,encoding)

def main_test(path=None,classifier='SVM_LINEAR',encoding='TFIDF'):

    dir_path = path or 'dataset'  
    # load data
    print colored('Loading dataset into memory', 'green', attrs=['bold'])
    files = sklearn.datasets.load_files(dir_path)
   
    # refine all emails
    print colored('Refining all files', 'green', attrs=['bold'])
    util.refine_all_emails(files.data)
    
    if encoding in ["BOW"]:
        # calculate the BOW representation
        print colored('Calculating BOW', 'green', attrs=['bold'])
        word_counts = util.bagOfWords(files.data)    
        X = word_counts
        saveFeatures(classifier+'_'+encoding+'_'+str(len(files.target_names))+'class'+'_'+'BOW.tfidf',word_counts)
    elif encoding=='TFIDF':
        # TFIDF
        print colored('Calculating TFIDF', 'green', attrs=['bold'])        
        word_list = words.words()
        word_list = list(set(word_list))        
        stop_words = stopwords.words('english')
        vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(vocabulary=word_list,stop_words = stop_words)
        X = vectorizer.fit_transform(files.data)   
        saveFeatures(classifier+'_'+encoding+'_'+str(len(files.target_names))+'class'+'_'+'TFIDF.tfidf',vectorizer)
        #vectorizer = loadFeatures('/home/farshad/Python_Classifier/tfidf') 


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

    print colored('Configuration = '+classifier +' '+encoding, 'magenta', attrs=['bold'])        

    X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X, files.target, test_size=0)

    clf.fit(X_train, y_train)

    saveModel(classifier+'_'+encoding+'_'+str(len(files.target_names))+'class'+'.pkl',clf)    

def saveModel(name,clf):
    with open(name, 'wb') as fid:
        cPickle.dump(clf, fid)

def loadModel(name,clf):
    with open(name, 'rb') as fid:
        clf = cPickle.load(fid)

def saveFeatures(name,vectorizer):
    with open(name, 'wb') as fid:
        cPickle.dump(vectorizer, fid)

def loadFeatures(name):
    with open(name, 'rb') as fid:
        vectorizer = cPickle.load(fid)
        return vectorizer

if __name__ == '__main__':
    datapath = sys.argv[1]
    classifier = sys.argv[2]
    encoding = sys.argv[3]    
    main(datapath,classifier,encoding)
