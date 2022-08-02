#
#
#

import os
import sys
import geopandas as gpd
import pandas as pd
import re


KEYS = ['std_ymd',	'arrival_hour',	'local_user',
        'sex',	'age',	'org',	'dest',	'catecode_a',
        'catecode_b',	'catecode_c',	'catecode_d']


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

        df = pd.read_csv(file, sep=sep)[:10]
        cols = df.columns

        if sep == '|':
            col = [x.lower() for x in df.columns]
            df.columns = col
        try:
            temp.append(df[KEYS])
        except KeyError:
            print(file)
            continue

        if not os.path.exists('temp.csv'):
            temp[-1].to_csv('temp.csv', mode='w', encoding='euc-kr')
        else:
            temp[-1].to_csv('temp.csv', mode='a', encoding='euc-kr')

    df = pd.concat(temp)


if __name__ == '__main__':
    main(data_dir=sys.argv[1],
         result_dir=sys.argv[2])
