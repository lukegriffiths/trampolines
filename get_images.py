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

def get_image(coords,topath, zoom=18, verbose=False):
    """Get satellite image using google maps staticmap API

    Args:
        coords (tuple of floats): Tuple of long, lat coords
        topath (string or path): folder destination of images
    """
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/staticmap'

    coords = str(coords[0]) + "," + str(coords[1])
    
    params = {
            'key': API_KEY,
            'size': '640x640',
            'maptype': 'satellite',
            'zoom': str(zoom),
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

    # spacing required for 19 zoom
    spacing_long = 0.00171661376953125
    spacing_lat = 0.0008583068847869413
    OFFSET = 0 # start of numbering of images

    long_range = (10.5, 10.8)
    lat_range = (59.88, 59.97)
    coords_start = (lat_range[0], long_range[0])

    num_lat = int((lat_range[1] - lat_range[0]) / spacing_lat)
    num_long = int((long_range[1] - long_range[0]) / spacing_long)
    
    #num_lat = 3 # number of images to take in lat direction
    #num_long = 3 # number of images to take in long direction

    total_num_images = num_lat * num_long

    input(f"Will fetch {total_num_images} images - press Enter to continue...")

    zoom = 19
    # make zero-array of coordinate pairs
    coords_grid = np.zeros((num_lat,num_long), dtype='f,f')

    print(f"Starting at {coords_start}...")

    # cycle through each coordinate pair
    for i in range(num_lat):
        for j in range(num_long):
            coords_grid[i,j] = (coords_start[0] + i * spacing_lat, coords_start[1] + j * spacing_long)
    
    # make into 1D array of coordinate pairs
    coords_vec = coords_grid.flatten()

    # write text file with image names and coordinates
    with open('./images/images.txt', 'w') as f:
        print('Getting image data...')
        for i, coords in enumerate(tqdm(coords_vec)):
            f.write(f"{i+OFFSET}, {coords[0]}, {coords[1]}, {zoom}\n")
            get_image(coords, topath=f'images/{i+OFFSET}', zoom=zoom, verbose=False)
