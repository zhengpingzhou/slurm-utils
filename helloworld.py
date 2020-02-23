import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-id', '--run_id', type=str)
opt = parser.parse_args()

print('Hello world!', opt.run_id)
