
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


def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    
    start_time = time.time()

    rating = pd.read_csv("batch_freq.csv")

    mapping = pd.read_csv("movie_titles.csv", encoding = "ISO-8859-1", header = None, names = ['Movie_Id', 'Year', 'Name'])

    title_to_id = {}
    id_to_title = {}


    # rows and columns
    r, c = mapping.shape

    query = "Titanic"


    # mapping
    for i in range(r):
        curIdx = int(mapping.iloc[i][0])
        curName = mapping.iloc[i][2]
        title_to_id[curName] = curIdx
        id_to_title[curIdx] = curName


    queryNum = str(title_to_id[query])

    print(queryNum)

    print("Name to ID Conversion")
    print("--- %s seconds ---" % (time.time() - start_time))


    r2, c2 = rating.shape

    freq_item = Counter()

    for i in range(r2):

        curRow = str(rating.iloc[i][0]).split()
        freq = rating.iloc[i][1]

        if len(curRow)==1:
            continue
        if queryNum not in curRow:
            continue




        for word in curRow:
            if word != queryNum:
                freq_item[word] += freq

    print("Find all related items in frequent item set")
    print("--- %s seconds ---" % (time.time() - start_time))


    pq = []

    for key,value in freq_item.items():

        heapq.heappush(pq,(value,id_to_title[int(key)]))

        if len(pq)>10:

            heapq.heappop(pq)

    idx = 1

    while len(pq)>0:

        freq, key = heapq.heappop(pq)

        s = str(idx)+ ":  " + key + " ---> " +str(freq)
        idx+=1

        print(s)

    

    





if __name__ == "__main__":
    main()