from pylab import plot, show
from geopy.geocoders import Nominatim
import math
from math import sqrt

location_cache = {}  # this will cache the coordinates of the locations, to prevent fetching the location again


class matchrow:
    def __init__(self, row, allnum=False):
    	'''
        row - a line from the file
        the lines has comma separated values, and all the values except the
        last value will be used in the classification
        the last value indicates whether or not someone is considered a good match
        allnum - shows if all the columns of the row are numbers
        '''
        self.data = [float(row[i]) for i in range(len(row) - 1)] if allnum\
            else row[0:len(row) - 1]
        self.match = int(row[len(row) - 1])


def loadmatch(f, allnum=False):
    '''
    f - the name of the file whose data is to be loaded
    rows will have all the data of the file from each file
    '''
    rows = []
    for line in file(f):
        rows.append(matchrow(line.split(','), allnum))
    return rows


def plotagematches(rows):
    '''
    generates a scatter plot for man's age versus woman's age
    a match will be shown be a green 'o' while no match will be shown by
    a red 'x'
    The matching will only be based on age, which is quite simple
    '''
    xdm, ydm = [r.data[0] for r in rows if r.match == 1], \
        [r.data[1] for r in rows if r.match == 1]

    xdn, ydn = [r.data[0] for r in rows if r.match == 0], \
        [r.data[1] for r in rows if r.match == 0]

    plot(xdm, ydm, 'go')
    plot(xdn, ydn, 'rx')

    show()


def lineartrain(rows):
    '''
    classifies linearly.
    rows - the row of data to be used to find classes
    finds the averages of the data points belonging to a class
    new data will be classified based on its closeness to the averagaes of the
    classes. The closest class average will be the class of the data
    '''
    averages = {}  # will hold the sums of the data points of classes
    counts = {}  # will hold the counts of the occurrences of the classes

    for row in rows:
        # the class, in this case we can have either a match or not i.either
        # only 2 classes for the ages only data
        clazz = row.match

        averages.setdefault(clazz, [0.0] * len(row.data))
        counts.setdefault(clazz, 0)

        for i in range(len(row.data)):
            averages[clazz][i] = float(row.data[i])  # adding the data point to the class data point sum
            counts[clazz] += 1  # incrementing the counts

    for clazz, avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[clazz]  # the average of the sums

    return averages


def dotproduct(v1, v2):
    '''
    finds the dot product of 2 vectors
    '''
    return sum([v1[i] * v2[i] for i in range(len(v1))])


def dpclassify(point, avgs):
    '''
    classifies data using dot products
    point - the ata point to be classified
    avgs - the averages of the classes
    the class of the data point is determined by finding the sign between
    the vector connecting the point and the center of the vector connecting the
    average points
    '''
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) / 2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
    if y > 0:
        return 0
    return 1


def yesno(v):
    '''
    converts yesno values into numerical
    if the value is not specified or is ambiguous a value of 0 will
    be assigned
    '''
    if v == 'yes':
        return 1
    elif v == 'no':
        return -1
    return 0


def matchcount(interest1, interest2):
    '''
    returns the numbers of common interests between 2 people
    '''
    interest1 = interest1.split(':')  # the interests are split by ':'
    interest2 = interest2.split(':')
    common_interests = 0
    for interest in interest1:
        if interest in interest2:
            common_interests += 1
    return common_interests


def getlocation(address):
    '''
    gets the latitude and longitude from the address
    uses the geopy api to get the coodinates
    '''
    if address in location_cache:
        return location_cache[address]
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    lat = location.latitude  # the latitude
    longi = location.longitude  # the longitude
    location_cache[address] = float(lat), float(longi)  # adding the locations to the cache

    return location_cache[address]


def milesdistance(a1, a2):
    '''
    calculates the approximate distance in miles between addresses a1 and a2
    '''
    lat1, longi1 = getlocation(a1)
    lat2, longi2 = getlocation(a2)
    latdif = 69.1 * (lat2 - lat1)  # distance between latitudes in miles
    longidif = 53.0 * (longi2 - longi1)  # distance between longitudes in miles
    return sqrt(pow(latdif, 2) + pow(longidif, 2))  # distance between the coordinates


def loadnumerical():
    '''
    creates a new dataset from the dataset in matchmaker.csv
    the non-numerical data points are converted to numerical ones
    '''
    oldrows = loadmatch('matchmaker.csv')  # consists of numerical and non-numerical data
    newrows = []  # will hold the new data having only numerical data
    count = 0
    for row in oldrows:
        count += 1
        d = row.data
        data = [float(d[0]), yesno(d[1]), yesno(d[2]), float(d[5]), yesno(d[6]), yesno(d[7]),
            matchcount(d[3], d[8]), milesdistance(d[4], d[9]), row.match]
        newrows.append(matchrow(data))

    return newrows


def scaledata(rows):
    '''
    scales data to be in the same range
    if a specific date point is in a bigger scale than the rest, its contribution to learning will be greater than
    other data points. The data ranges after scaling will be between 0 and 1
    '''
    low = [999999999.0] * len(rows[0].data)  # will hold the minimum of every data column
    high = [-999999999.0] * len(rows[0].data)  # will hold the maximum of every data column

    # finding the minimum and the maximum values of each columns
    for row in rows:
        d = row.data
        for i in range(len(d)):
            if d[i] < low[i]:
                low[i] = d[i]
            if d[i] > high[i]:
                high[i] = d[i]

    # function that scales data
    def scaleinput(d):
        return [(d[i] - low[i]) / (high[i] - low[i]) for i in range(len(low))]  # scales the value between 0 and 1

    newrows = [matchrow(scaleinput(row.data) + [row.match]) for row in rows]

    return newrows, scaleinput


def rbf(v1, v2, gamma=20):
    '''
    radial-bias function
    the output is non-linear which makes it possible to map to more complex
    spaces
    gamma is used to determine the linear separation between the dataset
    '''
    dv = [v1[i] - v2[i] for i in range(len(v1))]
    l = sum([dv[i] ** 2 for i in range(len(dv))]) ** 0.5  # size of the vector
    return math.e ** (-gamma * l)


def nlclassify(point, rows, offset, gamma):
    sum0 = 0.0
    sum1 = 0.0
    count0 = 0.0
    count1 = 0.0

    for row in rows:
        if row.match == 0:
            sum0 += rbf(point, row.data, gamma)
            count0 += 1
        else:
            sum1 += rbf(point, row.data, gamma)
            count1 += 1

    y = (1.0/count0)*sum0-(1.0/count1)*sum1+offset

    if y < 0:
        return 0
    return 1


def getoffset(rows, gamma=10):
    l0 = []
    l1 = []

    for row in rows:
        if row.match == 0:
            l0.append(row.data)
        else:
            l1.append(row.data)

    sum0 = sum(sum([rbf(v1, v2, gamma) for v1 in l0]) for v2 in l0)
    sum1 = sum(sum([rbf(v1, v2, gamma) for v1 in l1]) for v2 in l1)

    return (1.0/(len(l1)**2))*sum1-(1.0/(len(l0)**2))*sum0
