## building a wiki corups for physics
from bs4 import BeautifulSoup
import urllib.request
import wikipedia as wk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import io
import csv
import pickle
corpus_dict = {}
vectorarray = []
## Arrays of table contents in wikipedia page
field = []
subfields = []
theories = []
concepts = [] 
page_content = {}
## getting the table data from the wikipedia for the topics
def get_tabledata():
    global field, subfields,theories,concepts
    wiki = "http://en.wikipedia.org/wiki/Physics"
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib.request.urlopen(wiki)
    soup = BeautifulSoup(req)
    table = soup.find("table", { "class" : "wikitable" })
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        #For each "tr", assign each "td" to a variable.
        if len(cells) == 4:
            field.append(cells[0].find(text=True))
            subfields.append(cells[1].findAll(text=True))
            theories.append(cells[2].findAll(text=True))
            concepts.append(cells[3].findAll(text=True))
        if len(cells) ==2:
            field.append(cells[0].find(text = True))
            subfields.append(cells[1].findAll(text = True))
    return field, subfields, theories, concepts

def get_wiki_page(i):
    for item in i:
        if(item.strip() in string.punctuation):
            continue
        elif(item == 'weak' or item == 'strong' or item == 'Spin' or item == 'String' or item == 'Phases' or item == 'Cosmos' or item == '), ' or item == ' (' ):
            continue
        else:
            try:
                page_item = wk.page(item)
            except wk.exceptions.DisambiguationError as e:
                earray = e.options
                get_wiki_page(earray)
            pc = page_item.content
            print(item)
            if(item in page_content.keys()):
                continue
            else:
                page_content[item] = pc
            
##getting contents from the different pages found above in the table
def get_pagecontent():
    for item1 in field:
        print(item1)
        page_item1 = wk.page(item1)
        pc1 = page_item1.content
        page_content[item1] = pc1
    for item2 in subfields:
        get_wiki_page(item2)
    for item3 in theories:
        get_wiki_page(item3)
    for item4 in concepts:
        get_wiki_page(item4)

def process_content():
    stop = stopwords.words('english')
    stop.sort()
    for key in page_content:
        print(key)
        words = []
        text = page_content[key]
        tokens = word_tokenize(text.lower())
        tokens.sort()
        for i in tokens:
            if i not in stop:
                if i not in string.punctuation and i.isalpha():
                    if(len(i) >3 and len(i)< 15 ):
                        words.append(i)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        page_content[key] = set(words)

def write_to_csv():
    with io.open('physics_corpus.csv', 'w' ,encoding = 'ascii' , errors = 'ignore' ) as csv_file:
        writer = csv.writer(csv_file)
        for key, value in page_content.items():
            writer.writerow([key, value])

def prepare_pickle():
    with io.open('physics_corpus.csv', 'r' ,encoding = 'ascii' , errors = 'ignore' ) as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            if(line == []):
                continue
            else:
                content = "".join(line[1].replace("'","").split(','))
                corpus_dict[line[0]]= content
                vectorarray.append(content)
                
    print(vectorarray)
    vectorizer = TfidfVectorizer(max_df = 6)
    X = vectorizer.fit_transform(vectorarray)
    gt2words = vectorizer.get_feature_names()
    print(gt2words)
    for key in corpus_dict.keys():
        new_content= ""
        content = corpus_dict[key].split(" ")
        for item in content:
            if(item in gt2words):
                new_content += " " + item
            else:
                continue
        corpus_dict[key]= new_content
    pickle.dump(corpus_dict,open("phy_corp","wb"))
get_tabledata()
#print( concepts)
get_pagecontent()
process_content()
write_to_csv()
prepare_pickle()