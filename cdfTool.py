
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys




# generates a random uniform number from a given seed
def uniformRng(seed):

    m = 2**32
    a = 1103515245
    c = 12345

    seed = (a*seed + c) % m
    return seed/m

# creates a sequence of random numbers according to exponential distribution
def exponential(exponent, n, seed):

    i = 0
    myList = []

    while i <= n:

        random = uniformRng(seed + i)

        myList.append((-math.log(1.00-random) / exponent))
        i += 1

    return myList

    """will need to sort decreasing"""

# creates a sequence of random numbers according to geometric distribution
def geometric(probability, n, seed):

    i = 0
    myList = []

    while i <= n:

        random = uniformRng(seed + i)

       # myList.append ((math.log(1-random)) / (math.log(1-p)))

        if random < probability:
            value = 0
        else:
            value = math.ceil(math.log(1-random) / math.log(1 - probability))

        myList.append(value)

        i += 1

    return myList

# creates a sequence of random numbers according to gumbel distribution
def gumbel(mu,beta, n, seed):

    i = 0
    myList = []

    while i <= n:
        random = uniformRng(seed + i)

        value = mu - (beta * math.log(-math.log(random)))

        myList.append(value)

        i += 1

    return myList



# plots a cdf and saves it as a pdf, also creates a dictionary with the plot ranges and counts for those ranges
def plotCdf(disType, numSequence):

    #calculate bins dynamically
    numberOfBins = 50

    while numberOfBins < len(numSequence) / 4:
        numberOfBins += 25


    numSequence.sort()
    minValue = numSequence[0]
    maxValue = numSequence[-1]
    totalLength = minValue + maxValue
    subrangeLength = totalLength / numberOfBins
    currentStart = numSequence[0]

    edges = []

    edges.append(currentStart)

    for i in range(int(numberOfBins)):
        currentStart += subrangeLength
        edges.append(currentStart)

    #print(edges)

    edgesDictionary = {}

    for i in range (len(edges)-1):
        lower = edges[i]
        upper = edges [i+1]
        binRange = (lower,upper)
        edgesDictionary[binRange] = 0
    #print(edgesDictionary)

    for number in numSequence:
        for bin in edgesDictionary:
            if number >= bin[0] and number < bin[1]:
                edgesDictionary[bin] += 1
    #print(edgesDictionary)

    # get the list of count values from the dictionary
    counts= list(edgesDictionary.values())

    # plotting
    cdf = np.cumsum(counts)
    plotFigure = plt.figure()

    plotFigure.suptitle(disType + ' cdf plot', fontsize=20)
    plt.style.use('seaborn')
    plt.plot(edges[1:], cdf / cdf[-1])
    if disType == "geo" or "exp":
        plt.ylim([0.00, 1.01])
    plt.xlim([edges[0], edges[-1]])
    #plt.show()

    fileName = disType +"_plot.pdf"
    plotFigure.savefig(fileName)

    # return dictionary of bins and counts to use for cdf data output
    return edgesDictionary

# creates a file of the number sequence
def writeNumberSequence(disType, sequence):

    fileName = disType + '_rng_sequence.txt'

    pwd = os.path.dirname(os.path.realpath(__file__))

    path = os.path.join(pwd, fileName)

    i = 0

    try:
        file = open(path, 'w')

        for number in sequence:
            file.write("%f, " % number)
            i += 1
            if i == 10:
                file.write("\n")
                i = 0


        file.close()

    except IOError:
        print("Unable to write file, file not saved")

# creates a file containing the cdf data
def writeCdfData(disType, bins_dictionary):

    fileName = disType + '_cdf_data.txt'

    pwd = os.path.dirname(os.path.realpath(__file__))


    path = os.path.join(pwd, fileName)

    try:
        file = open(path, 'w')

        for (binRangeStart,binRangeEnd), counts in bins_dictionary.items():
            file.write("range: %s - %s count: %i \n" % (binRangeStart, binRangeEnd,counts))

        file.close()

    except IOError:
        print("Unable to write file, file not saved")



# gets inputs form the command line, calls the other functions that produce the outputs
def takeInputs(n, seed, disType, param1, *optional):

    try:
        param2 = optional[0]
    except:
        param2 = 1

    if  not float(seed):
        print("please enter an integer/float for seed")

    else:
        if not int(n):
            print("please enter an integer for n")

        else:

            disType = disType.lower()
            n = int(n)
            seed = float(seed)
            param1 = float(param1)

            if disType == "exp":
                if float(param1) or int(param1):

                    sequence = exponential(param1, n, seed)
                    writeNumberSequence(disType, sequence)
                    cdf_Data = plotCdf(disType,sequence)
                    writeCdfData(disType, cdf_Data)

                else:
                    print("invalid parameter type")

            elif disType == "geo":
                if float(param1) or int(param1):
                    if param1 <= 0.99 and param1 >= 0.01:
                        sequence = geometric(param1, n, seed)
                        writeNumberSequence(disType, sequence)
                        cdf_Data = plotCdf(disType, sequence)
                        writeCdfData(disType, cdf_Data)

                    else:
                        print("parameter should be between 0.01 and 0.99")
                else:
                    print("invalid parameter type")

            elif disType == "gum":
                    if float(param1) or int(param1):
                        param2 = float(param2)
                        sequence = gumbel(param1, param2, n, seed)
                        writeNumberSequence(disType, sequence)
                        cdf_Data = plotCdf(disType, sequence)
                        writeCdfData(disType, cdf_Data)

                    else:
                        print("invalid parameter type")

            else:
                print("invalid distribution selected try exp, geo or gum")





# running the program

args_list = sys.argv

if len(args_list) == 5:
    takeInputs(args_list[1],args_list[2],args_list[3],args_list[4])

elif len(args_list) == 6:
    takeInputs(args_list[1], args_list[2], args_list[3], args_list[4], args_list[5])
else:
    print("incorrect format, try python3 cdfTool.py 1500 56767 geo 0.3")






