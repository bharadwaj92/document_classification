import time
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
import collections

def dict_divide(raw_dict, num):
    list_result = []
    len_raw_dict = len(raw_dict)
    if len_raw_dict > num:
        base_num = int(len_raw_dict / num)
        addr_num = len_raw_dict % num
        for i in range(num):
            this_dict = dict()
            keys = list()
            if addr_num > 0:
                keys = list(raw_dict.keys())[:base_num + 1]
                addr_num -= 1
            else:
                keys = list(raw_dict.keys())[:base_num]
            for key in keys:
                this_dict[key] = raw_dict[key]
                del raw_dict[key]
            list_result.append(this_dict)

    else:
        for d in raw_dict:
            this_dict = dict()
            this_dict[d] = raw_dict[d]
            list_result.append(this_dict)
    return list_result

dict_list = dict_divide(physics_corpus, 10)

def set_tag( line, dict_item):
    result_part = {}
    linetokens = line.split(" ")
    for item in linetokens:
        for key in dict_item.keys():
            content_tokens = dict_item[key].split(" ")
            if item in content_tokens:
                if(key in result_part.keys()):
                #print(item,key , os.getpid())
                    result_part[key] = result_part[key]+1
                else:
                    result_part[key] = 1
                
    return result_part

start_time = time.time()                
if __name__ == '__main__':
    p = Pool(processes = num_processes)    
    with io.open('words.csv', 'r' ,encoding = 'ascii' , errors = 'ignore' ) as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            if(line[1] == "set()"):
                result[line[0]] = "physics"
            else:
                content = "".join(line[1].replace("'","").replace("{","").replace("}","").split(','))
                temp = p.map(partial(set_tag ,content), dict_list)
                res = Counter({})
                for items in temp:
                    res = res + Counter(items)
                if(bool(res)):
                    result[line[0]] = res.most_common(2) 
                    
                else:
                    result[line[0]] = "physics"
                
                result_part = {}
                
                 
print("--- %s seconds ---" % (time.time() - start_time))
orderd_results = collections.OrderedDict(sorted(result.items()))
print(orderd_results)
with io.open('result_mp.csv', 'w' ,encoding = 'ascii' , errors = 'ignore' ) as file1:
    writer = csv.writer(file1)
    for key , value in orderd_results.items():
        writer.writerow([key, value])
