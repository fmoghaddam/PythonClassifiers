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
from sklearn.metrics import accuracy_score

def main(testDataPath = None, modelName=None, tfidfModelName=None):
    init()    
    pathForDataset = testDataPath
    # remove any newlines or spaces at the end of the input
    path = pathForDataset.strip('\n')
    if path.endswith(' '):
        path = path.rstrip(' ')

    main_test(path,modelName,tfidfModelName)

def main_test(path=None,modelName=None,tfidfModelName=None):

    dir_path = path
    
    # load data
    print colored('Loading test data into memory', 'green', attrs=['bold'])       
    testFiles = sklearn.datasets.load_files(dir_path)        

    print colored('Loading features into memory', 'green', attrs=['bold'])        
    vectorizer = loadTFIDF(tfidfModelName)

    print colored('Loading model into memory', 'green', attrs=['bold'])        

    clf = loadModel(modelName)
    
    TEST = vectorizer.transform(testFiles.data)    
    
    mapDic = dict({"negative":"0", "positive":"1"}) 
    inverted_dict = dict([[v,k] for k,v in mapDic.items()])    

    cross_validation(inverted_dict,TEST, testFiles.target, clf, test_size=1, y_names=testFiles.target_names, confusion=False)

def cross_validation(inverted_dict,X, y, clf, test_size=0.4, y_names=None, confusion=False):        
    y_predicted = clf.predict(X)    
    print "accuracy= " + str(accuracy_score(y, y_predicted))
    
def saveModel(name,clf):
    with open(name, 'wb') as fid:
        cPickle.dump(clf, fid)

def loadModel(name):
    with open(name, 'rb') as fid:
        clf = cPickle.load(fid)
        return clf

def loadTFIDF(name):
    with open(name, 'rb') as fid:
        vectorizer = cPickle.load(fid)
        return vectorizer

if __name__ == '__main__':
    testDataPath = sys.argv[1]
    modelName = sys.argv[2]
    tfidfModelName = sys.argv[3]

    main(testDataPath,modelName,tfidfModelName)