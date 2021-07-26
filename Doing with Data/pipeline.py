import csv
import json
import unidecode
from fuzzywuzzy import fuzz

route = 'routes/'

with open(route+'route.csv', mode='r', encoding='utf-8') as csv_file: #file with paths of the network
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    routes = list(csv_reader)

with open(route+'nodes_geocoded.csv', mode='r', encoding='utf-8') as csv_file: #file with node coordinates
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    nodes = list(csv_reader)

length_r = 0
macrosegment_list = []
nodeA = routes[0][3]
macrosegment = routes[0][0]
i = 0
while i < len(routes):
    if macrosegment == routes[i][0]:
        length_r += float(routes[i][5])
        i += 1
        continue
    else:
        macrosegment_list.append([macrosegment,routes[i-1][2],nodeA, routes[i-1][4], length_r, routes[i-1][6], routes[i-1][9],routes[i-1][8]])
        nodeA = routes[i][3]
        macrosegment = routes[i][0]
        length_r = 0
macrosegment_list.append([macrosegment,routes[i-1][2],nodeA, routes[i-1][4], length_r, routes[i-1][6], routes[i-1][9],routes[i-1][8]])

dataset = []
geometryType = "LineString" #for the type of line needed
not_found = 0


for index, row in enumerate(macrosegment_list):
    if row[1] == '':
        break
    introw = []
    introw.append(index + 1)
    introw.append(row[7]) # phase
    introw.append(row[1])# route name
    introw.append(row[4]) #route length
    introw.append(row[6]) #available pairs
    pointA = row[2] #defined as Punta A in the source file, start of the connection
    pointB = row[3] #defined as Punta B in the source file, end of the connection
    introw.append(pointA)
    introw.append(pointB)
    pointA_coordinates = [0,0]
    pointB_coordinates = [0,0]
    for node in nodes:
        if fuzz.ratio(unidecode.unidecode(node[0]),unidecode.unidecode(pointA))>93:
            pointA_coordinates = [float(node[6]), float(node[7])] #extract pointA coordinates
            #print(node[0]," <-> ", pointA)
        elif fuzz.ratio(unidecode.unidecode(node[0]) , unidecode.unidecode(pointB))>93:
            pointB_coordinates = [float(node[6]), float(node[7])] #extract pointB coordinates
            #print(node[0]," <-> ", pointB)

    if (pointA_coordinates == [0,0]): #logic for pointA and B not being found
        not_found += 1
        print("POINT A: " ,pointA, " NOT FOUND!")

    if (pointB_coordinates == [0,0]): #logic for pointA and B not being found
        not_found += 1
        print("POINT B: " ,pointB, " NOT FOUND!")
    if (pointA_coordinates == [0,0] or pointB_coordinates == [0,0]): #logic for pointA and B not being found
        not_found += 1
        print("One of the ", row[1], " route nodes was not found! Check if the name is correctly written!")

    #creating dictionary with format neccesary for pipeline map
    route_dictionary = {'type': 'Feature', 'properties': {}, 'geometry': {'type': geometryType, 'coordinates': [pointA_coordinates, pointB_coordinates]}}
    route_dictionary_str = json.dumps(route_dictionary) #function to convert dictionary into json file text
    introw.append(route_dictionary_str)
    dataset.append(introw)

if not_found == 0:
    print("All data found!")
else:
    print(not_found, " coordinate(s) not found, their longitude and latitude has been labeled with 0")

with open(route+"traced_routes_json_v3.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['key_id','Year', 'RouteName', 'RouteLength', 'Pairs', 'PuntaA', 'PuntaB', 'JSONroute'])
    writer.writerows(dataset)
