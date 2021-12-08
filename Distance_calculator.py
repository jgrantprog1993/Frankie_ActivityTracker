from math import radians, cos, sin, asin, sqrt
import glob
import os 

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


def calctime(time):
    timeRes = time[-1] - time[0]
    ##print(timeRes)
    return timeRes

list_of_files = glob.glob('/home/pi/Assignment_2/*.txt') # * means all if need specific format then *.csv
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
        ##print(x[:][2])

##print(timedata)
timeCalcRes = calctime(timedata)
print( timeCalcRes)


##print(str(data[:,-1]))

