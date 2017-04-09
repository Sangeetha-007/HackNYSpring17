"""
work in progress

"""
import requests
import json
import pickle
import math
import itertools
import statistics 
from collections import defaultdict

def normalize_function(val, maximum, minimum):
    return (val - minimum)/(maximum-minimum)

def normalize(data):
    normalize_dict = {}
    for tname,tvalues in pickle_data.items():
        normalize_dict[tname] = {}
        for mode_type in model:
            non_normalized_array = [item[mode_type] for item in tvalues.values()]
            #fix nm and None values
            for a,b in enumerate(non_normalized_array):
                if b == "nm" or b == None:
                    try:
                        non_normalized_array[a] = (non_normalized_array[a-1]+non_normalized_array[a+1])/2.0
                    except TypeError:
                        #fix this
                        non_normalized_array[a] = (non_normalized_array[a-1]+non_normalized_array[a-2])/2.0
            minimum = min(non_normalized_array)
            maximum = max(non_normalized_array)
            normalize_dict[tname][mode_type] = [normalize_function(i,maximum, minimum) for i in non_normalized_array]
    return normalize_dict


def get_num_combinations(array):
    length = len(array)
    return pow(2, length) - 1 - length

def get_array_subsets(array):
    all_combos = []
    for i in range(get_num_combinations(array)):
        all_combos.extend(list(itertools.combinations(array,i)))
    return all_combos

def sortNormalized(array):
    for tname,tvalues in array.items():
        for mode_type in model:
            tvalues[mode_type] = sorted(tvalues[mode_type], reverse= True)

def performance(combo_array, array):
    stock_status = {}
    for tname,tvalues in array.items():
        stock_status[tname] = []
        for i in combo_array:
            if i:
                #get combined mean
                arraysum = []
                for m in i:
                    arraysum.extend(tvalues[m])
                combined_score = getMean(arraysum)
                max_val = max(tvalues[i[-1]])
                print(combined_score,max_val)
                if(combined_score > max_val):
                    result_score = 1
                if(combined_score < max_val):
                    result_score = -1
                if(combined_score == max_val):
                    result_score = 0
                stock_status[tname].append(result_score)
            else:
                stock_status[tname].append(None)
    return stock_status

def getMean(array):
    return statistics.mean(array)   


blacklist = [float(0), float(1)]
def removeStuff(array):
    for tname,tvalues in array.items():
        for a in tvalues.keys():
            array[tname][a] = [e for e in array[tname][a] if float(e) not in blacklist]


pickle_data = pickle.load(open("procs.p", "rb"))
tickers = pickle_data.keys()
model = ["PE", "EPS", "PBV", "NM", "NINR"]

#normalize array
normalized_array = dict(normalize(pickle_data))

#make list of all_combos
all_combos = get_array_subsets(model)

#sort normalize array
sortNormalized(normalized_array)

#remove 0 and 1
removeStuff(normalized_array)

matrix = performance(all_combos, normalized_array)
print(matrix)

