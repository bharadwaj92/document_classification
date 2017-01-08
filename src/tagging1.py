from multiprocessing import Pool
import pickle
physics_corpus = pickle.load(open("phycorp_maxdf25" , "rb"))
#print(physics_corpus)
result = {}
num_processes = 10
import math
import io
import csv
import os
from functools import partial
from collections import Counter
import time
import collections
def set_tag( line):
    result_line = {}
    linetokens = line.split(" ")
    for item in linetokens:
        for key in physics_corpus.keys():
            content_tokens = physics_corpus[key].split(" ")
            if item in content_tokens:
                if(key in result_line.keys()):
                    #print(item,key , os.getpid())
                    result_line[key] = result_line[key]+1
                else:
                    result_line[key] = 1
    return result_line            
start_time = time.time()    
with io.open('words.csv', 'r' ,encoding = 'ascii' , errors = 'ignore' ) as csv_file:
    reader = csv.reader(csv_file)
    for line in reader:
        if(line[1] == "set()"):
            result[line[0]] = "physics"
        else:
            content = "".join(line[1].replace("'","").replace("{","").replace("}","").split(','))
            temp = set_tag(content)
            #print(temp)
            if( bool(temp)):
                result[line[0]] = Counter(temp).most_common(2) 
            else:
                result[line[0]] = "physics"

print("--- %s seconds ---" % (time.time() - start_time))
ordered_results = collections.OrderedDict(sorted(result.items()))
print(ordered_results)
with io.open('result_sp.csv', 'w' ,encoding = 'ascii' , errors = 'ignore' ) as file1:
    writer = csv.writer(file1)
    for key , value in ordered_results.items():
        writer.writerow([key, value])

