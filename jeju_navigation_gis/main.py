#
#
#

import os
import sys
from sklearn.cluster import KMeans
import shutil
import matplotlib.pyplot as plt
import pandas as pd
import re


KEYS = ['dest_hh', 'dest_mm', 'dest']


def main(data_dir, result_dir):
    #
    #
    #
    if os.path.exists('temp.csv'):
        os.remove('temp.csv')
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
            temp[-1].to_csv('temp.csv', mode='a', encoding='euc-kr', header=False)

    df = pd.concat(temp)

    df['LAT'] = df['dest'].str.split('_').str[0].map(lambda x: int(x[5:]))
    df['LON'] = df['dest'].str.split('_').str[1]
    df['TIME'] = 24*df['dest_hh'] + df['dest_mm']

    df = df.drop(['dest', 'dest_hh', 'dest_mm'], axis=1)

    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d import proj3d

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    X = df

    # 3d scatterplot 그리기
    ax.scatter(X['LAT']
               , X['LON']
               , X['TIME']
               , s=10  # 사이즈
               , cmap="orange"  # 컬러맵
               , alpha=1  # 투명도
               , label='class1'  # 범례
               )

    plt.legend()  # 범례표시
    plt.show()

    ks = range(1, 10)
    inertias = []

    for k in ks:
        model = KMeans(n_clusters=k)
        model.fit(df)
        inertias.append(model.inertia_)

    plt.figure(figsize=(4, 4))

    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()


if __name__ == '__main__':
    main(data_dir=sys.argv[1],
         result_dir=sys.argv[2])
