import argparse
from lib import *

parser = argparse.ArgumentParser(description='Acquire rain data from the SSMI.')
parser.add_argument('-s', '--start-day', help='YYYY-MM-DD', required=True)
parser.add_argument('-e', '--end-day', help='YYYY-MM-DD', required=True, type=int)
parser.add_argument('-d', '--directory-path', help='Path to directory for storing the data.', required=True)
parser.add_argument('-t', '--tiles', help='tiles you would like to download', required=True)
args = parser.pars_args()
