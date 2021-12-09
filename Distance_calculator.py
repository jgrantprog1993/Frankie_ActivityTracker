from math import radians, cos, sin, asin, sqrt
import glob
import os 
from datetime import datetime

now = datetime.now() # current date and time
date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

def haversine(lon1, lat1, lon2, lat2):
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance = 2 * asin(sqrt(a)) * 6371 #6371 is the radius of the Earth
    return distance

##https://stackoverflow.com/questions/903853/how-do-you-extract-a-column-from-a-multi-dimensional-array
def column(matrix, i):
    return [row[i] for row in matrix]

def calctime(time):
    timeRes = time[-1] - time[0]
    ##print(timeRes)
    return timeRes


def calcDistanceDelta_Sum(data):
    latCol = column(data,0)
    lonCol = column(data,1)
    x=0
    distCalcList = []
    while x<(len(latCol)-1):
        distanceCalc = haversine(lonCol[x], latCol[x], lonCol[x+1], latCol[x+1])
        ###print(distanceCalc)
        distCalcList.append(distanceCalc)
        x+=1

    distanceTotal = sum(distCalcList)
    ##print(distCalcList)
    ##print(distanceTotal)
    return distanceTotal, distCalcList

def avgSpeed(data, timeCalcRes):
    totalDist, intervDist = calcDistanceDelta_Sum(data)
    avgSpeed = totalDist / timeCalcRes
    return avgSpeed

##https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder##
list_of_files = glob.glob('/home/pi/Assignment_2/ResultsFolder/*.txt') # * means all if need specific format then *.csv 
latest_file = max(list_of_files, key=os.path.getctime)

ins = open(latest_file, 'r')
data = []
timedata = []
for line in ins:
    number_strings = line.split() # Split the line on runs of whitespace
    numbers = [float(n) for n in number_strings] # Convert to floats
    data.append(numbers) # Add the "row" to your list.
    ##print(data) # [[1, 3, 4], [5, 5, 6]]
    
for x in data:
    timedata.append(x[:][2])
    ##print(timedata)


##print(timedata)
timeCalcRes = calctime(timedata)
print( f'{timeCalcRes:.5f}')
totalDist, distDelta = calcDistanceDelta_Sum(data)
print(f'{totalDist:.5f}')

avgSpeedRes = avgSpeed(data, timeCalcRes)
print(f'{avgSpeedRes:.5f}')

file2 = open(f'ResultsFolder/GPS_Stats_{date_time}.txt', 'w')
file2.write(f"{timeCalcRes:.5f} {totalDist:.5f} {avgSpeedRes:.5f} \n")

