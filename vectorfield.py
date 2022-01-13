
import sys
import random
import argparse
from math import *
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


DEFAULT_HEIGHT = 1600
DEFAULT_WIDTH = 900
DEFAULT_DENSITY = 4
DEFAULT_COLORSCHEME = 'dark_background'

XLIM_MIN, XLIM_MAX = [-20, 20]
YLIM_MIN, YLIM_MAX = [-20, 20]

# parser arguments
parser = argparse.ArgumentParser('Save vector fields as a PNG file. Comes with several default vector fields.')
parser.add_argument('-c', '--color', type=str,
                    help='Color scheme', choices=plt.style.available,  default=DEFAULT_COLORSCHEME)
parser.add_argument('-v', '--vectorfield', type=int,
                    default=0, help='Create a random vector field or use some predefined ones.')
parser.add_argument('-ht', '--height', type=int, default=DEFAULT_HEIGHT, help=f'Height. Default:{DEFAULT_HEIGHT}')
parser.add_argument('-w', '--width', type=int, default=900, help=f'Width. Default: {DEFAULT_WIDTH}')
parser.add_argument('-d', '--density', type=int, default=DEFAULT_DENSITY,
                    help='Density of the vector field.')
parser.add_argument('-p', '--path', type=str, help='Path in which the file will be saved. ',
                    default=pathlib.Path(__file__).parent.resolve())
parser.add_argument('-f', '--function', type=str, nargs=2, default=None, help='Function to be represented. Two functions must be provided, each for one axis.')
parser.add_argument('-s', '--show', action='store_true',
                    help='Show the image or not.')

# create grid
x, y = np.meshgrid(np.linspace(XLIM_MIN, XLIM_MAX, 50),
                   np.linspace(YLIM_MIN, YLIM_MAX, 50))

# parse the inputs
args = parser.parse_args()
height = args.height
density = args.density
path = pathlib.Path(args.path)
function_x = lambda x: eval(args.function[0])
function_y = lambda y: eval(args.function[1])

# list with functions
func_list = [x, y, -10/20*np.sin(x) - 2*y, np.sin(x)*np.cos(y), np.cosh(x)]

# We set some interesting vector fields
predefined_vf = [[1, 2], [0, 1]]

if args.function is None:
    if args.vectorfield == 1:
        # retrieve 2 random func
        u, v = random.sample(func_list, 2)
    elif args.vectorfield == 2:
        # use our selected vector fields
        u = func_list[predefined_vf[args.vectorfield - 1][0]]
        v = func_list[predefined_vf[args.vectorfield - 1][1]]
    else:
        print('Wrong option, please try again.')
        sys.exit()
else:
    u = np.vectorize(function_x)(x)
    v = np.vectorize(function_y)(y)


plt.style.use(args.color)
fig = plt.figure()
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

# plot it
ax.streamplot(x, y, u, v, density=density)

full_path = f'{path}/vectorfield.png'
# save it with desired size
plt.savefig(f'{path}/vectorfield.png', bbox_inches='tight', pad_inches=0, format='png',
            dpi=height/fig.get_size_inches()[1])

# we open our image
img = Image.open(full_path)

# we get our actual img size
img_width, img_height = img.size

left = 300
top = 100
right = img_width - 300
bottom = img_height - 100
cropped_img = img.crop((left, top, right, bottom))
cropped_img.save(full_path)

if args.show is True:
    cropped_img.show()