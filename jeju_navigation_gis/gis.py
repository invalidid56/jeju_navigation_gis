#
#
#

import os
import sys
import geopandas as gpd
import pandas as pd
import re


def main(data_dir, result_dir):
    #
    #
    #
    gdf = gpd.read_file(data_dir)
    print(gdf.head())

if __name__ == '__main__':
    main(data_dir=sys.argv[1],
         result_dir=sys.argv[2])
