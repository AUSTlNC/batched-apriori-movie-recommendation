
import numpy as np
import pandas as pd
import heapq
import time
import heapq

from collections import Counter


'''
Julian Zhao
jzzhao@emory.edu


THIS  CODE  WAS MY OWN WORK.
IT WAS  WRITTEN  WITHOUT  CONSULTING  CODE WRITTEN BY OTHER STUDENTS 
Name: Julian Zhao

Collaboration Statement -- I discussed with the following classmate:
Austin Cai
Helen Zeng
'''

# For list of itemset (list of strings) of size k, generate itemset of size (k+1)
def find(curID, watched, freq_item, rating):
    

    r2, c2 = rating.shape

    for i in range(r2):

        curRow = str(rating.iloc[i][0]).split()
        freq = rating.iloc[i][1]

        if len(curRow)==1:
            continue
        if curID not in curRow:
            continue


        for word in curRow:
            if word not in watched:
                freq_item[word] += freq


    return freq_item


def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    
    start_time = time.time()

    rating = pd.read_csv("batch_freq.csv")

    user = pd.read_csv("data_5star.csv")

    mapping = pd.read_csv("movie_titles.csv", encoding = "ISO-8859-1", header = None, names = ['Movie_Id', 'Year', 'Name'])

    title_to_id = {}
    id_to_title = {}


    # rows and columns
    r, c = mapping.shape




    for i in range(r):
        curIdx = int(mapping.iloc[i][0])
        curName = mapping.iloc[i][2]
        title_to_id[curName] = curIdx
        id_to_title[curIdx] = curName
        
    print("Name to ID Conversion")
    print("--- %s seconds ---" % (time.time() - start_time))


    # Customer ID
    # 337541 works
    # 372233 works

    query = "785314"

    ur, uc = user.shape
    freq_item = Counter()

    

    for i in range(ur):
        if str(user.iloc[i][0]) == query:
            print("----------")
            print("|Found ID: "+ query + " |")
            print("----------")
            movies = str(user.iloc[i][1]).split(",")
            watched = set(movies)
            for s in movies:
         
                freq_item = find(s,watched,freq_item,rating)

            break

    print("Find all related items in frequent item set")
    print("--- %s seconds ---" % (time.time() - start_time))


    pq = []

    for key,value in freq_item.items():

        heapq.heappush(pq,(value,id_to_title[int(key)]))

        if len(pq)>10:

            heapq.heappop(pq)

    idx = 1

    namelist = []
    numlist = []

    while len(pq)>0:

        freq, key = heapq.heappop(pq)
        namelist.insert(0,key)
        numlist.insert(0,freq)

    for i in range(len(namelist)):

        name = namelist[i]
        freq = numlist[i]

        s = str(i+1)+ ":  " + name + " ---> " +str(freq)

        print(s)

    

    





if __name__ == "__main__":
    main()