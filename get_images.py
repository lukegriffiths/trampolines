import requests
import time
import os
from dotenv import load_dotenv
import numpy as np
from tqdm import tqdm

# load environment variables with API key
load_dotenv('api_key.env')
API_KEY = os.environ.get('API_KEY')
print(API_KEY)

def get_image(coords,topath, verbose=False):
    """Get satellite image using google maps staticmap API

    Args:
        coords (tuple of floats): Tuple of long, lat coords
        topath (string or path): folder destination of images
    """
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
    if verbose:
        print(response.status_code)
    time.sleep(1)
        
    filepath = topath + '_gmaps.jpg'
    if verbose:
        print(filepath)
            
    with open(filepath, 'wb') as f:
        f.write(response.content)
            

if __name__ =='__main__':

    # initial parameters
    coords_start = (59.93717029103388, 10.807871254728301) # lat long coordinates of start point
    num_lat = 10 # number of images to take in lat direction
    num_long = 10 # number of images to take in long direction
    spacing = 0.003 # interval in degrees between images
    OFFSET = 25 # start of numbering of images

    # make zero-array of coordinate pairs
    coords_grid = np.zeros((num_lat,num_long), dtype='f,f')

    # cycle through each coordinate pair
    for i in range(num_lat):
        for j in range(num_long):
            coords_grid[i,j] = (coords_start[0] + i * spacing, coords_start[1] + j * spacing)
    
    # make into 1D array of coordinate pairs
    coords_vec = coords_grid.flatten()

    # write text file with image names and coordinates
    with open('./images/images.txt', 'w') as f:
        print('Getting image data...')
        for i, coords in enumerate(tqdm(coords_vec)):
            f.write(f"{i+OFFSET}, {coords[0]}, {coords[1]}\n")
            get_image(coords, topath=f'images/{i+OFFSET}', verbose=False)
