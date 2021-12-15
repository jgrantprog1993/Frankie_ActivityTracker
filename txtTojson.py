import json

logfile = open('ResultsFolder/GPS_TrackerData_1_12_14_2021_23_42_35.txt')

#initialising a list to append all the log lines formatted as json
log_list = []

for line in logfile:
    # splitting on '|'
    pipe_split = [ele.strip() for ele in line.split(", ")]

    # initialising dictionary to fill the line splitted data in key-value pairs
    line_dict = dict()

    for ele in pipe_split:
        # splitting on first occurrence of ':' 
        key,val = ele.split(":",1)
        line_dict[key] = val

    # appending the key-value data of each line to a list
    log_list.append(line_dict)

with open('dump.json', 'w') as json_file:
    json.dump(log_list,json_file,indent=4)


