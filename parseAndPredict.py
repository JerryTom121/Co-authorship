# Christopher Thamrun
# cthamrun@bu.edu
# CS565, Project 1 - Co-authorship prediction

import csv
import string
import math

features = open('features.txt')
terms = {}

blacklist = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it',\
 	     'for', 'not', 'on', 'with', 'as', 'you', 'do', 'at', 'this', 'but', 'by',\
	     'from', 'they', 'we', 'say', 'or', 'an', 'will', 'my', 'one', 'all', \
	     'would', 'there', 'their', 'what', 'up', 'out', 'if', 'about', 'who', 'get',\
             'which', 'go', 'can', 'no', 'just', 'know', 'take', 'into', 'some', 'could', \
	     'them', 'see', 'other', 'than', 'then', 'see', 'other', 'than', 'then', 'now', \
	     'look', 'only', 'come', 'its', 'over', 'think', 'also', 'use', 'how', 'our', \
	     'work', 'am', 'way', 'new', 'want', 'any', 'these', 'most'] 

def parseFeatures(inputText):
	authors = {}
	for line in inputText:
		list = [x.strip() for x in line.split(", ")]
		author = list[0]
		if author not in authors: 
			authors[author] = {}
		features = list[1:]
		for f in features:
			x = f.split(":")
			term = x[0].strip("\"").strip(".").strip(",")
			term = term.strip(")").strip("(").strip("?")
			term = term.strip(";").strip("_").strip("-").lower()
			punc = set(string.punctuation)
			term = ''.join(ch for ch in term if ch not in punc)
			freq = int(x[-1])
			if term not in blacklist and len(term) >= 9:
				if term not in authors[author]:
					authors[author][term] = freq
				else:
					authors[author][term] += freq
	return authors

authorFeatureList = parseFeatures(features)

edgesCSV = open('edges_names.csv')
trainCSV = open('train.csv')

edgesToPredict = []

def parseEdges(edges, train):
	edgesMatrix = {}
	reader0 = csv.reader(edges)
	reader1 = csv.reader(train)
	reader0.next()
	reader1.next()
	for i in range(5000):
		x = reader0.next()
		x = [a.strip() for a in x]
		y = reader1.next()
		edgesMatrix[tuple(x[1:])] = int(y[1])
	for i in range(14999):
		x = reader0.next()
		x = [a.strip() for a in x]
		edgesToPredict.append(tuple(x[1:]))
	return edgesMatrix
		
edgesMatrix = parseEdges(edgesCSV, trainCSV)

def calcDist(a1, a2):
	author1 = authorFeatureList[a1]
	author2 = authorFeatureList[a2]
	if len(author1) == 0 or len(author2) == 0:
		return 0.0
	return JSim(author1.keys(), author2.keys())

def JSim(x, y):
	common = list(set(x).intersection(y))
	all = list(set(x).union(y))
	jsim = float(len(common)) / float(len(all))
	return jsim

def calculateThreshold():
	numPairedAuthors = 0
	totalDistance = 0
	for (author1, author2) in edgesMatrix:
		if edgesMatrix[(author1, author2)] == 0:
			totalDistance += calcDist(author1, author2)
			numPairedAuthors += 1
	threshold = totalDistance / numPairedAuthors
	return threshold

threshold = calculateThreshold() 
print threshold

def predict():
	prediction = []
	for (a1, a2) in edgesToPredict:
		if calcDist(a1, a2) >= threshold - 0.0005:
			prediction.append(1)
		else:
			prediction.append(0)
	return prediction

pred = predict()

testCSV = open('test1.csv', "w")
writer = csv.writer(testCSV)
id = []
for i in range(14999):
	id.append(5001 + i)
rows = zip(id, pred)
writer.writerow(('id', 'coauthors'))
for row in rows:
	writer.writerow(row)
