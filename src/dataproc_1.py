import csv
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import io 
import csv
import re

word_tokens = []
corpuspath = r'/mnt/c/Users/bharadwaj/Desktop/kaggle/physics_corpus.csv'
path = r'/mnt/c/Users/bharadwaj/Desktop/kaggle/test.csv'
content = {}
with open('test.csv', newline = '', encoding = 'utf-8') as f:
    reader= csv.reader(f)
    for row in reader:
        print(row[0])
        content[row[0]]= row[1]+ row[2]

with io.open('content.csv', 'w' ,encoding = 'utf-8' ) as csv_file:
    writer = csv.writer(csv_file)
    for key, value in content.items():
        writer.writerow([key, content[key]]) 