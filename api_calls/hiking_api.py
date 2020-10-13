### Quinn Siebers
import requests
import os

# url = 'hikingproject.com/data/get-trails?lat=40.0274&lon=-105.2519&maxDistance=10&key=200938679-800b65469cb54ac98df735f3abe211cd'
# FOR NOW THIS IS HARD CODED
key = '200938679-800b65469cb54ac98df735f3abe211cd'

# def getTrails(lat, long):

url = 'https://www.hikingproject.com/data/get-trails'
    
query = {'lat' : '40.0274', 'lon' : '-105.2519', 'key' : key }

data = requests.get(url, params=query).json()

for x in range(-1,5):
    trail_name = data['trails'][x]['name']
    trail_summary = data['trails'][x]['summary']
    trail_length = data['trails'][x]['length']
    trail_difficulty = data['trails'][x]['difficulty']
    trail_img = data['trails'][x]['imgMedium']

    print(f'Name: {trail_name} | Trail summary: {trail_summary} | Trail length: {trail_length} | Trail difficulty: {trail_difficulty} | Trail img: {trail_img}')


# data = requests.get(url).json()
# print(data)

### example function

def get_trails(lat, lon):

    url = 'https://www.hikingproject.com/data/get-trails'
    
    query = {'lat' : lat, 'lon' : lon, 'key' : key }

    data = requests.get(url, params=query).json()
##example  print for 5 results
    for x in range(-1,5):
        trail_name = data['trails'][x]['name']
        trail_summary = data['trails'][x]['summary']
        trail_length = data['trails'][x]['length']
        trail_difficulty = data['trails'][x]['difficulty']
        trail_img = data['trails'][x]['imgMedium']

        print(f'Name: {trail_name} | Trail summary: {trail_summary} | Trail length: {trail_length} | Trail difficulty: {trail_difficulty} | Trail img: {trail_img}')