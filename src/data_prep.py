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
with open(path, newline = '', encoding = 'utf-8') as f:
    reader= csv.reader(f)
    for i in range(3):
        for row in reader:
            content[row[0]]= row[1]+ row[2]

stop = stopwords.words('english')
stop.sort()
with io.open('words.csv', 'w' ,encoding = 'ascii' , errors = 'ignore' ) as csv_file:
    writer = csv.writer(csv_file)
    for key in content:
        print(key)
        words = []
        text = content[key]
        tokens = word_tokenize(text.lower())
        tokens.sort()
        for i in tokens:
            ## removing paragraph tokens and other small words 
            if(i != 'p' and i !='/p' ):
                if i not in stop:
                    if i not in string.punctuation:
                        word = re.sub('[^A-Za-z]+', '', i)
                        if(len(word) >3 and len(word)< 15 and word != 'href' and word!= 'http' and word!= 'https'  ):
                            words.append(word)
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                continue
        content[key] = set(words)
        print(content[key])
        writer.writerow([key, content[key]])