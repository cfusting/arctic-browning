import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os.path
import argparse
import sys

parser = argparse.ArgumentParser(description='Plot a series of tiffs with a single scale.')
parser.add_argument('-i', '--in-file', help='Name of file containing a list of files for plotting.', required=True)
parser.add_argument('-o', '--out-file', help='Name of resulting plot.', required=True)
parser.add_argument('-d', '--dpi', help='Dots per inch.', default=400, type=int)
parser.add_argument('-r', '--rows', help='Number of rows.', required=True, type=int)
parser.add_argument('-c', '--cols', help='Number of columns.', required=True, type=int)
parser.add_argument('-w', '--width', help='Width of the plot in inches.', default=7, type=int)
parser.add_argument('-t', '--height', help='Height of the plot in inches.', default=5, type=int)
args = parser.parse_args()


def plot_one(file_path, axs):
    img = mpimg.imread(file_path) * .0001
    axs.set_title(os.path.basename(file_path))
    image = axs.imshow(img, vmin=0, vmax=1)
    axs.axis("off")
    return image

file_list = [line.rstrip('\n') for line in open(args.in_file)]
if args.cols * args.rows != len(file_list):
    sys.exit("The product of the specified number of rows and columns does not equal the number of files.")
fig, axes = plt.subplots(nrows=args.rows, ncols=args.cols, figsize=(args.width, args.height))
i = 0
im = None
for ax in axes.flat:
    im = plot_one(file_list[i], ax)
    i += 1
fig.colorbar(im, ax=axes.ravel().tolist(), orientation="horizontal")
plt.savefig(args.out_file, dpi=args.dpi)
