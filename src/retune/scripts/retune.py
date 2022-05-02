import sys
import os

sys.path.append(os.path.dirname(sys.argv[0]) + "/../packages")
from public import *

__parser = argparse.ArgumentParser()
__parser.add_argument('config', type=str, help='Configuration file, either subscription url or file path is ok.')
__parser.add_argument('template', type=str, help='Template file, same requirement as configuration.')
__parser.add_argument('-o', '--output', type=str, help='Output file path.', default='config.yml')
args = __parser.parse_args()

def main():
    


if __name__ == '__main__':
    main()
