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
from scipy.sparse import vstack
from nltk.corpus import words
from nltk.corpus import stopwords
from sklearn.metrics import average_precision_score

def main(sentence=None,modelName=None,tfidfModelName=None):
    init()        
    main_test(sentence,modelName,tfidfModelName)

def main_test(sentence='',modelName=None,tfidfModelName=None):

    vectorizer = loadFeatures(tfidfModelName) 
    mapDic = dict({"negative":0,"positive":1}) 
    inverted_dict = dict([[v,k] for k,v in mapDic.items()])
    TEST = vectorizer.transform([sentence])    
    clf = loadModel(modelName)
    cross_validation(inverted_dict,TEST,clf)

def cross_validation(inverted_dict,X, clf):    
    y_predicted = clf.predict(X)        
    print inverted_dict[y_predicted[0]]    

def saveModel(name,clf):
    with open(name, 'wb') as fid:
        cPickle.dump(clf, fid)

def loadFeatures(name,vectorizer):
    with open(name, 'wb') as fid:
        cPickle.dump(vectorizer, fid)

def loadModel(name):
    with open(name, 'rb') as fid:
        clf = cPickle.load(fid)
        return clf
def loadFeatures(name):
    with open(name, 'rb') as fid:
        vectorizer = cPickle.load(fid)
        return vectorizer

if __name__ == '__main__':    
    sentence = sys.argv[1]
    modelName = sys.argv[2]
    tfidfModelName = sys.argv[3]
    main(sentence,modelName,tfidfModelName)