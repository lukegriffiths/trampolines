import requests
import time
import os
from dotenv import load_dotenv

load_dotenv('api_key.env')
API_KEY = os.environ.get('API_KEY')
print(API_KEY)

def second_opinion(coords,topath):
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/staticmap'

    coords = str(coords[0]) + "," + str(coords[1])
    
    params = {
            'key': API_KEY,
            'size': '1024x1024',
            'maptype': 'satellite',
            'zoom': '18',
            'format': 'jpg',
            'center': coords
        }
        #print(params['center'])
    response = requests.get(GOOGLE_MAPS_API_URL, params=params)
    print(response.status_code)
    time.sleep(1)
        
    filepath = topath + '_gmaps.jpg'
    print(filepath)
            
    with open(filepath, 'wb') as f:
        f.write(response.content)
            
coords = ('59.92549', '10.78712')
#coords = ('40.714728','-73.998672')
i = 0
second_opinion(coords, topath=f'images/{i}')