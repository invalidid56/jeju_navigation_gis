#
#
#

import os
import sys

import pandas as pd
import re


def main(data_dir, result_dir):
    #
    #
    #
    file_list = sum([[os.path.join(data_dir, x, y) for y in os.listdir(os.path.join(data_dir, x))] for x in os.listdir(data_dir) if x.endswith('월')], [])

    prev = re.compile('data/[0-9]월/tmap')
    temp = []

    for file in file_list:
        if prev.match(file):
            sep = '|'
        else:
            sep = ','

        df = pd.read_csv(file, sep=sep).head()

        if sep == '|':
            col = [x.lower() for x in df.columns]
            df.columns = col

        temp.append(df)

    df = pd.concat(temp)


if __name__ == '__main__':
    main(data_dir=sys.argv[1],
         result_dir=sys.argv[2])
