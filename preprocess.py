import time
import pandas as pd 

def readFile(customer_to_movie, name):

    file = open(name,'r')

    movieID = "null"

    count = 1

    for line in file:

        line = line.rstrip()


        if ':' in line:

            movieID = line[:len(line)-1]

            if int(movieID)%100==0:

                print(movieID)

        else:

            rate = line.split(",")

            if int(rate[1])==5:

                customer = rate[0]

                s = ""

                if customer in customer_to_movie:

                    s = customer_to_movie[customer]+","

                s += movieID

                customer_to_movie[customer] = s

    file.close()




def main():
    """
    Main file to run from the command line.
    """

    customer_to_movie = {}

    name_list = ["combined_data_1.txt","combined_data_2.txt","combined_data_3.txt","combined_data_4.txt"]

    start_time = time.time()

    for name in name_list:

        readFile(customer_to_movie,name)

        print(len(customer_to_movie))
        print("--- %s seconds ---" % (time.time() - start_time))

    print(len(customer_to_movie))

    datadict = {"CustomerID":[],"5-Star Movies":[]}

    for key,value in customer_to_movie.items():

        datadict["CustomerID"].append(key)
        datadict["5-Star Movies"].append(value)

    df = pd.DataFrame(datadict)

    df.to_csv("data_5star.csv",index = False)


if __name__ == "__main__":
    main()