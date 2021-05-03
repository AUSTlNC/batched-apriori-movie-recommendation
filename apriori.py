import argparse
import numpy as np
import pandas as pd
import time
import heapq
from itertools import combinations
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
def generate(last_list):

    super_list = []

    # for each pair (i,j) determine if they are differ by one element

    for i in range(0,len(last_list)):

        for j in range(i+1,len(last_list)):

            list1 = last_list[i]
            list2 = last_list[j]

            target = len(list1)+1

            curlist = []

            for word in list1:
                if word not in curlist:
                    curlist.append(word)

            for word in list2:
                if word not in curlist:
                    curlist.append(word)



            curlist.sort()

            # If two list are differ by one element and it had not been included before, add it to the super_list

            if len(curlist) == target and curlist not in super_list:
                super_list.append(curlist)

    return super_list

# Prune the list through checking if all its (k-1)-size subsets are included in the previous frequent itemset. If not, then eliminate the list of string.
def prune(last_list, cur_list):
    
    prune_list = []


    for eachlist in cur_list:

        freq = True

        # Use the combination method in python package
        # This method can generate all the sublist of length(k-1) of for a list (k)

        for sublist in combinations(eachlist,len(eachlist)-1):

            sublist2 = list(sublist)

            # If this list is not in the last frequent list, then this list is not frequent 
            if sublist2 not in last_list:
                freq = False
                break

        if freq:
            prune_list.append(eachlist)

    return prune_list

# Count all the frequency of the prune list item. Return the Counter
def count(prune_list,transactions):

    cnt = Counter()


    for item in prune_list:

        # I use the string concatenation as the key with space between each word.
        name = ' '.join(item)
        cur = 0

        for transaction in transactions:

            # For each transaction, all the words in the itemset must be presented in the transaction
            # If so, then the frequency increases

            find = True
            for word in item:
                if word not in transaction:
                    find = False
                    break

            if find:
                cur+=1

        # Save the key and its frequency
        cnt[name] = cur

    return cnt



def apriori(df, threshold, start_time):

    

    c = Counter()

    # Iterate each "transaction" and count each individual text as an item
    # Save the transaction to a list (for later count() method)
    transactions = []


    for item in df["5-Star Movies"]:

    

        curList = item.split(",")
        a = set()

        for word in curList:

            # For each word, increase frequency by 1
            c[word]+=1
            a.add(word)

        transactions.append(a)


    # The first frequent item list
    last_list = []

    # Answer heap. It sorts each pair by the negative value of its frequency. Therefore, it is a maxHeap structure  
    ans_heap = []

    for key in c:

        # If value bigger than threshold, make each word into a list, and add that list to the frequent item list
        # Also, add it to the answer maxheap
        if c[key]>=threshold:

            curList = []
            curList.append(key)
            last_list.append(curList)
            heapq.heappush(ans_heap,(-1*c[key],key))

    print("item-size: 1")
    print("--- %s seconds ---" % (time.time() - start_time))

    loop = 2

    # When there are still frequent item in the list
    while(len(last_list)>0):

        # Generate the k+1 frequent list
        cur_list = generate(last_list)

        print("Generation: "+str(loop))
        print("--- %s seconds ---" % (time.time() - start_time))

        if len(cur_list)==0:
            break

        # Prune the current list
        prune_list = prune(last_list,cur_list)

        print("Prune: "+str(loop))
        print("--- %s seconds ---" % (time.time() - start_time))

        # Get the counter of the current prune list
        cnt = count(prune_list,transactions)

        print("Count: "+str(loop))
        print("--- %s seconds ---" % (time.time() - start_time))

        last_list = []

        # If the frequency is bigger than the threshold, then add the current itemset to the k-size frequent itemset and answer heap
        for key in cnt:

            if cnt[key]>=threshold:

                last_list.append(key.split())
                heapq.heappush(ans_heap,(-1*cnt[key],key))

        print("item-size: " + str(loop))
        print("--- %s seconds ---" % (time.time() - start_time))
        loop+=1

    # Write the answer
    # file = open("output_20000.txt","w") 

    dic = {}

    while(len(ans_heap)>0):

        # Write each answer in the proper format
        freq, key = heapq.heappop(ans_heap)
        dic[key] = freq

    return dic



def main():
    """
    Main file to run from the command line.
    """
    # set up the program to take in arguments from the command line
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--rating",
                        default="data_5star.csv",
                        help="filename for features of the training data")
    parser.add_argument("--numBatch",
                        default=10,
                        help="filename for features of the training data")
    parser.add_argument("--dropRate",
                        default=0.4,
                        help="filename for features of the training data")
    parser.add_argument("--threshold",
                        default=0.05,
                        help="filename for features of the training data")
    
    

    args = parser.parse_args()
    rating = pd.read_csv(args.rating)
    numBatch = args.numBatch


    # testing


    dropRate = args.dropRate
    threshold = args.threshold
    start_time = time.time()

    freq_item = Counter()

    freq_batch = {}



    for i in range(1,numBatch+1):

        print("batch_num" + str(i))

        drop_percent = int(len(rating.index)*dropRate)
        drop_idx = np.random.choice(rating.index, drop_percent, replace=False)
        newRating = rating.drop(drop_idx)

        minSupport = int(threshold*int(len(rating.index)*(1-dropRate)))

        #numOfRows to drop: 185446
        print("Number of rows to drop: "+str(drop_percent))

        #Minsup 13908
        print("minSupport: " + str(minSupport))

        freq_dict = apriori(newRating,minSupport,start_time)

        curMap = {}

        for key,value in freq_dict.items():

            freq_item[key]+=1
            curMap[key] = value


        freq_batch[i] = curMap





    datadict = {"Frequent Itemset":[],"Number of batches":[]}
    for key,value in freq_item.items():

        datadict["Frequent Itemset"].append(key)
        datadict["Number of batches"].append(value)

    df_batch = pd.DataFrame(datadict)

    df_batch.to_csv("batch_freq.csv",index = False)

    allfreqdict = {"Batch Number":[],"Frequent Itemset":[],"Frequency":[]}

    for i in range(1,numBatch+1):

        curMap = freq_batch[i]

        for key,value in curMap.items():

            allfreqdict["Batch Number"].append(i)
            allfreqdict["Frequent Itemset"].append(key)
            allfreqdict["Frequency"].append(value)

    df_all = pd.DataFrame(allfreqdict)


    df_all.to_csv("all_batches.csv",index = False)







if __name__ == "__main__":
    main()