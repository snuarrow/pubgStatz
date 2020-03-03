import sys
import argparse
import os
import json
from flows import WebDataBasePopulator
from flows import DataLoader
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

def parse_arguments():
    parser = argparse.ArgumentParser(description='Boohyeaz, PUBGSTATZZ backendz! version: very beta')
    parser.add_argument('--populate', action='store_true', help='populate database')
    parser.add_argument('--players', type=int, help='downloadload matches and telemetries from this many players')
    parser.add_argument('--root-player', type=str, help='root player name, to where start recursive data search')
    parser.add_argument('--token', type=str, help='pubg api token')
    parser.add_argument('--plot', action='store_true', help='enable plotting')
    parser.add_argument('--plot-target', type=str, help='some of these: squad_landings, ...')
    parser.add_argument('--cache', action='store_true', help='enable caching')
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    if args.populate:
        webDataBasePopulator = WebDataBasePopulator()
        webDataBasePopulator.saveAllMatchesOfPlayer(playerName=args.root_player)
        dataLoader = DataLoader()
        uniquePlayers = dataLoader.loadUniquePlayers()[:args.players]
        for uniquePlayer in uniquePlayers:
            webDataBasePopulator.saveAllMatchesOfPlayer(playerName=uniquePlayer[1])
        webDataBasePopulator.getTelemetriesForExistingMatches()
        print('database population complete')
        return
    if args.cache:
        if args.plot_target == 'karakin_landings':
            dataLoader = DataLoader()
            all_karakin_landings = dataLoader.loadAllParachuteLandings(mapName='Summerland_Main')
            with open('all_karakin_landings.json', 'w') as f:
                json.dump(all_karakin_landings, f)

        print('caching complete')
        return
    
    if args.plot:
        if args.plot_target == 'karakin_landings':
            landings = None
            with open('all_karakin_landings.json') as f:
                landings = json.load(f)
            dataframe = np.zeros([2200,2200])
            for landing in landings:
                dataframe[int(landing['y'] / 100)][int(landing['x'] / 100)] += 1
            # disable margins:
            #plt.gca().set_axis_off()
            #plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
            #plt.margins(0,0)
            #plt.gca().xaxis.set_major_locator(plt.NullLocator())
            #plt.gca().yaxis.set_major_locator(plt.NullLocator())
            dataframe = gaussian_filter(dataframe, sigma=51)
            ax = sns.heatmap(dataframe)
            #ax.get_figure().savefig('out.pdf')
            plt.show()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)