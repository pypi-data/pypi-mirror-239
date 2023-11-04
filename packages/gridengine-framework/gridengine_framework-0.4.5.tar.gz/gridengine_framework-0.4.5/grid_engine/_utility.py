# This file contains utility functions for the grid engine.
import os
# Path: grid-engine/utility.py

CWD = os.getcwd()
if not os.path.exists(f'{CWD}/saves/'):
    os.mkdir(f'{CWD}/saves/')

SAVES_DIR = f'{CWD}/saves/'

def get_grid_dir(grid_id):
    """
    Creates a directory for saving generated grids.
    """
    if not os.path.exists(f'{SAVES_DIR}{grid_id}/'):
        os.mkdir(f'{SAVES_DIR}{grid_id}/')
    return f'{SAVES_DIR}{grid_id}/'
# Define the directory for saving generated grids.

# Define the function for generating grid images
def generate_images(dimensions, cdata, cell_size, grid_id, animate=False):
    print('Generating grid image ...')
    print('Importing pillow ...')

    from PIL import Image, ImageDraw, ImageShow
    import random
    print('Preparing raw image ...')
    image = Image.new('RGB', dimensions, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    w, h, s = dimensions[0], dimensions[1], cell_size
    total_cell_count = (w//s)*(h//s)
    print('Counting cells ...')
    print(f'Total cells: {total_cell_count}')
    cell_info = cdata
    print('Shuffling cells ...')
    x_data = cell_info['X']
    y_data = cell_info['Y']
    categories = cell_info['CATEGORY']
    colors = cell_info['COLOR']
    coordinates = list(zip(x_data, y_data))
    cells = list(zip(coordinates, colors, categories))

    if animate:
        frames = []
        # First let's draw the whole grid as a base layer with the background color (16, 78, 139, 255).
        # 500 cells at a time.
        coords = coordinates
        random.shuffle(coords)
        for count in range(0, total_cell_count, 500):
            for coord in zip(range(500), coords[count:count+500]):
                print(f'Drawing base cells {count+1}-{min(count+500, total_cell_count)} ... {round(((count+500)/total_cell_count)*500)}%', end='\r')
                i, coord = coord
                x, y = coord
                color = (16, 78, 139, 255)
                draw.rectangle((x, y, x+(cell_size), y+(cell_size)), fill=color)
            frames.append(image.copy())
        print('Base cells drawn.')
        # Now let's add a brief period of time before we start drawing more
        frames.extend(image.copy() for _ in range(30))
        # Now let's draw the cells in the order of their categories
        for category in ["GRASS", "SAND", "RIVER"]:
            print(f'Drawing cells of category {category} ...')
            cat_count = categories.count(category)
            for count in range(0, cat_count, 100):
                for cell in zip(range(100), cells[count:count+100]):
                    i, cell = cell
                    x, y = cell[0]
                    color = cell[1]
                    ctgry = cell[2]
                    if ctgry == category:
                        draw.rectangle((x, y, x+(cell_size), y+(cell_size)), fill=color)
                frames.append(image.copy())
        print('Saving grid animation ...')
        grid_id = grid_id[-5:]
        grid_dir = get_grid_dir(grid_id)
        frames[0].save(f'{grid_dir}grid.gif', format='GIF', append_images=frames[1:], save_all=True, duration=0.25, loop=0)
        print(f'grid.gif saved to {grid_dir}.')
    else:
        for i, cell in enumerate(cells):
            print(f'Drawing cells         {round((i/total_cell_count)*100)}%', end='\r')
            x = cell[0]
            y = cell[1]
            color = cell[2]
            draw.rectangle((x, y, x+(cell_size), y+(cell_size)), fill=color)
        print('Cells drawn.                                   ')
    print('Saving grid image ...')
    image.save(f'{grid_dir}grid.png')
    print(f'grid.png saved to {grid_dir}.')
    
    
# Define the QuietDict class

from typing import Union

class QuietDict:
    def __init__(self):
        self.items = {}

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key: Union[str, int]):
        if isinstance(key, str):
            return self.items[key]
        elif isinstance(key, int):
            return list(self.items.values())[key]
        else:
            raise TypeError("Key must be of type str or int")

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, key):
        return key in self.items

    def __repr__(self):
        return f"{self.__class__.__name__}({len(self.items)} items)"

    def __sub__(self, other):
        if isinstance(other, QuietDict):
            for key, value in self.items.copy().items():
                if key in other:
                    del self[key]

    def update(self, other=None, **kwargs):
        if other:
            if hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def values(self):
        return list(self.items.values())