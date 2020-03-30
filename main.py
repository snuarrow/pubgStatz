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
from tools import DateTools
from datetime import datetime, timedelta
from animator import Animator
import random
from gradient_factory import GradientFactory
import gc

def dev():

    def binarySearch(datetools: DateTools, events: list, toBeFound: datetime, left: int, right: int, previous_distance: timedelta):
        #print(f'left: {left}, right: {right}')
        mid = round((left + right) /  2)
        #print(f'mid: {mid}')
        subtraction = datetools.toDateTime_ms_accuracy(events[mid]['_D']) - toBeFound
        current_distance = abs(subtraction)
        #print(f'mid: {events[mid]}')
        #print(f'toBeFound: {toBeFound}')
        #print(f'subtraction: {current_distance}')

        if left == mid or right == mid:
        #    print('break')
            #print(events[mid])
            return events[mid]  

        if subtraction >= timedelta(0):
        #    print(f'positive')
            return binarySearch(datetools, events, toBeFound, left, mid, abs(subtraction))
        else:
        #    print(f'negative')
            return binarySearch(datetools, events, toBeFound, mid, right, abs(subtraction))


    #print('development mode')
    matches_by_matchId = None
    #with open('karakin_player_positions.json') as f:
    with open('karaking_player_positions_organized_by_matchid.json') as f:
        matches_by_matchId = json.load(f)

    datetools = DateTools()
#
    #re_organized = {}
#
    #for position in positions:
    #    matchId = position['matchId']
    #    if matchId in re_organized:
    #        re_organized[matchId].append(position['event'])
    #    else:
    #        re_organized[matchId] = [position['event']]
    #    #print(json.dumps(re_organized, indent=4, default=str))
    #    #print(datetools.toDateTime_ms_accuracy(position['event']['_D']))
    #
    #with open('karaking_player_positions_organized_by_matchid.json', 'w') as f:
    #    json.dump(re_organized, f)

    #for matchId in matches:
    #    first_event = matches[matchId][:1][0]
    #    last_event = matches[matchId][-1:][0]
    #    first_datetime = datetools.toDateTime_ms_accuracy(first_event['_D'])
    #    last_datetime = datetools.toDateTime_ms_accuracy(last_event['_D'])
    #    match_duration = last_datetime - first_datetime
    #    #for event in matches[matchId]:
    #    print(json.dumps(first_event, indent=4, default=str))
    #    print(json.dumps(last_event, indent=4, default=str))
    #    print(match_duration)
    #    intervals = datetools.getIntervals(first_datetime, last_datetime, 60)
    #    print(json.dumps(intervals, indent=4, default=str))
    #    binarySearch(datetools, matches[matchId], intervals[1], 0, len(matches[matchId]) -1, timedelta(days=1))
    #    exit(1)

    #big_data = None
    #with open('karakin_all_events.json') as f:
    #    big_data = json.load(f)
#
#
    #matches = {}
#
    #for event in big_data:
    #    #print(json.dumps(event, indent=4, default=str))
    #    #exit(1)
    #    matchId = event['matchId']
    #    try:
    #        accountId = event['event']['character']['accountId']
    #        if matchId not in matches:
    #            matches[matchId] = {accountId: [event['event']]}
    #        else:
    #            if accountId not in matches[matchId]:
    #                matches[matchId][accountId] = [event['event']]
    #            else:
    #                matches[matchId][accountId].append(event['event'])
    #    except KeyError:
    #        pass
#
    #with open('karakin_all_events_by_match_and_player.json', 'w') as f:
    #    json.dump(matches, f)

    matches = None
    with open('karakin_all_events_by_match_and_player.json') as f:
        matches = json.load(f)

    big_data_frame = []

    for k, matchId in enumerate(matches):
        print(f'{k+1} / {len(matches)}')
        all_events_for_match = matches_by_matchId[matchId]
        first_event = all_events_for_match[0]
        last_event = all_events_for_match[len(all_events_for_match)-1]
        first_datetime = datetools.toDateTime_ms_accuracy(first_event['_D'])
        last_datetime = datetools.toDateTime_ms_accuracy(last_event['_D'])
        intervals = datetools.getIntervals(first_datetime, last_datetime, 3)
        for j, accountId in enumerate(matches[matchId]):
            #print(j)
            playerEvents = matches[matchId][accountId]
            previousEventAtInterval = None
            for i, interval in enumerate(intervals):
                #print(f'{j} {i}')
                #print(interval)
                eventAtInterval = binarySearch(datetools=datetools, events=playerEvents, toBeFound=interval, left=0, right=len(playerEvents)-1, previous_distance=timedelta(days=1))
                if previousEventAtInterval:
                    if eventAtInterval == previousEventAtInterval:
                        continue
                previousEventAtInterval = eventAtInterval
                #print(json.dumps(eventAtInterval['_D']))
                #exit(1)
                try:
                    big_data_frame[i]
                except IndexError:
                    big_data_frame.append([])

                try:
                    big_data_frame[i].append(eventAtInterval)
                except IndexError:
                    print('skip')
                    pass
                
            #print(json.dumps(big_data_frame, indent=4, default=str))
        #exit(1)
            #binarySearch(datetools=datetools, events=playerEvents, )
            #print(len(playerEvents))
            #exit(1)

    with open('positions_animation.json', 'w') as f:
        json.dump(big_data_frame, f)
    exit(1)

def make_frames(grouped_events: dict, interval_seconds: int):
    def binarySearch(datetools: DateTools, events: list, toBeFound: datetime, left: int, right: int, previous_distance: timedelta):
        mid = round((left + right) /  2)
        #print(type(events))
        #print(f'left: {left}, right: {right}, mid: {mid}, len events: {len(events)}')
        subtraction = datetools.toDateTime_ms_accuracy(events[mid]['_D']) - toBeFound
        current_distance = abs(subtraction)
        if left == mid or right == mid:
            return events[mid]  
        if subtraction >= timedelta(0):
            return binarySearch(datetools, events, toBeFound, left, mid, abs(subtraction))
        else:
            return binarySearch(datetools, events, toBeFound, mid, right, abs(subtraction))

    num_frames = 0
    datetools = DateTools()
    frames = []
    for k, matchId in enumerate(grouped_events):
        print(f'generate frames: {k+1}/{len(grouped_events)}, num frames: {num_frames}')
        #print(json.dumps(grouped_events[matchId]['account.ccc4fc71e5274a32ac4bb89c2439e4ad'], indent=4))
        #exit()
        first_datetime = datetools.toDateTime_ms_accuracy(grouped_events[matchId]['first']['_D'])
        last_datetime = datetools.toDateTime_ms_accuracy(grouped_events[matchId]['last']['_D'])
        intervals = datetools.getIntervals(first_datetime, last_datetime, interval_seconds)
        for accountId in grouped_events[matchId]:
            if accountId not in ['first', 'last']:
                playerEvents = grouped_events[matchId][accountId]
                #print(json.dumps(playerEvents, indent=4))
                #exit()
                for i, interval in enumerate(intervals):
                    eventAtInterval = binarySearch(datetools=datetools, events=playerEvents, toBeFound=interval, left=0, right=len(playerEvents)-1, previous_distance=timedelta(days=1))
                    try:
                        frames[i].append(eventAtInterval)
                    except IndexError:
                        frames.append([])
                        frames[i].append(eventAtInterval)
                    if i > num_frames:
                        num_frames = i
    return frames


def group_by_match_and_player(all_eventss: list, winners: dict):


    def append_event(events: dict, event: dict):
        matchId = event['matchId']
        accountId = event['event']['character']['accountId']
        if matchId not in events:
            events[matchId] = {
                'first': event['event'],
                accountId: [event['event']]
            }
        else:
            if accountId not in events[matchId]:
                events[matchId][accountId] = [event['event']]
            else:
                events[matchId][accountId].append(event['event'])
        events[matchId]['last'] = event['event']
        return events

    all_events = {}
    winner_events = {}
    for event in all_eventss:
        matchId = event['matchId']
        try:
            accountId = event['event']['character']['accountId']
            if matchId in winners and accountId in winners[matchId]:
                winner_events = append_event(winner_events, event)
            all_events = append_event(all_events, event)
        except KeyError:
            pass

        #if matchId not in events_by_match_and_account_id:
        #    events_by_match_and_account_id[matchId] = {
        #        'first': event['event'],
        #        accountId: [event['event']]
        #    }
        #else:
        #    if accountId not in events_by_match_and_account_id[matchId]:
        #        events_by_match_and_account_id[matchId][accountId] = [event['event']]
        #    else:
        #        events_by_match_and_account_id[matchId][accountId].append(event['event'])
        #events_by_match_and_account_id[matchId]['last'] = event['event']
    return all_events, winner_events

def dev_winners():
    dataloader = DataLoader()
    load_stuff = True
    #load_all_positions = False
    #make_winner_frames = False
    #make_all_players_frames = False
    animate = True
    if load_stuff:
        winners = dataloader.loadWinners('Summerland_Main', 'Squad_fpp')
        #winners_positions_by_match_and_account_id = group_by_match_and_player(winners_positions)
        #with open('karakin_all_winners.json', 'w') as f:
        #    json.dump(winners, f)

        all_positions = dataloader.loadAllEvents('Summerland_Main')
        print(len(all_positions))
        all_positions_organized, all_winner_positions_organized = group_by_match_and_player(all_positions, winners)
        #with open('karakin_all_positions_organized.json', 'w') as f:
        #    json.dump(all_positions_organized, f)
        print(len(all_positions_organized))
        print(len(all_winner_positions_organized))

        #all_positions = {}
        #with open('karakin_all_positions_organized.json') as f:
        #    all_positions = json.load(f)
        all_positions_frames = make_frames(grouped_events=all_positions_organized, interval_seconds=3)
        with open('all_positions_animation.json', 'w') as f:
            json.dump(all_positions_frames, f)

        winner_positions_frames = make_frames(grouped_events=all_winner_positions_organized, interval_seconds=3)
        with open('winner_positions_animation.json', 'w') as f:
            json.dump(winner_positions_frames, f)

    if animate:
        animator = Animator(fps=20)
        animator.animate_winners()

        
        


def parse_arguments():
    parser = argparse.ArgumentParser(description='Boohyeaz, PUBGSTATZZ backendz! version: very beta')
    parser.add_argument('--db-status', action='store_true', help='print count of telemetry types in database')
    parser.add_argument('--populate', action='store_true', help='populate database')
    parser.add_argument('--players', type=int, help='downloadload matches and telemetries from this many players')
    parser.add_argument('--root-player', type=str, help='root player name, to where start recursive data search')
    parser.add_argument('--token', type=str, help='pubg api token')
    parser.add_argument('--plot', action='store_true', help='enable plotting')
    parser.add_argument('--plot-target', type=str, help='some of these: squad_landings, ...')
    parser.add_argument('--cache', action='store_true', help='enable caching')
    parser.add_argument('--dev', action='store_true', help='use this for development')
    parser.add_argument('--cache-locations', action='store_true', help='cache player locations by interval of 3sec into database table locations')
    parser.add_argument('--threads', type=int, default=1)
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    dataloader = DataLoader()
    #playerpositions = dataloader.loadAllPlayerPositions(mapName='Summerland_Main')
    #allEvents = dataloader.loadAllEvents(mapName='Summerland_Main')
    #with open('karakin_all_events.json', 'w') as f:
    #    json.dump(allEvents, f)

    #exit(1)
    


    if args.dev:
        #dev()
        print('yolo')
        #matchIds = dataloader.loadMatchIds(gameMode='squad-fpp', mapName='Summerland_Main')
        #telemetry = dataloader.loadTelemetry(matchIds[0])
        #gradient_factory = GradientFactory(height=1920, width=1920, gameMode='squad-fpp', mapName='Summerland_Main')
        #gradient_factory.launch(threads=2)
        #print(json.dumps(telemetry, indent=4))
        #dev_winners()
        return

    if args.cache_locations:
        gradient_factory = GradientFactory(height=1920, width=1920, gameMode='squad-fpp', mapName='Summerland_Main')
        gradient_factory.launch(threads=args.threads)
        return

    if args.db_status:
        dbStatus = dataloader.loadDatabaseStatus()
        print(json.dumps(dbStatus, indent=4))
        return

    if args.populate:
        webDataBasePopulator = WebDataBasePopulator()
        webDataBasePopulator.saveAllMatchesOfPlayer(playerName=args.root_player)
        dataLoader = DataLoader()
        uniquePlayers = dataloader.loadUniquePlayers(count=args.players)
        #uniquePlayers = random.sample(dataLoader.loadUniquePlayers(), args.players)
        for uniquePlayer in uniquePlayers:
            webDataBasePopulator.saveAllMatchesOfPlayer(playerName=uniquePlayer)
        webDataBasePopulator.getTelemetriesForExistingMatches()
        print('database population complete')
        return
    if args.cache:
        if args.plot_target == 'karakin_landings':
            dataLoader = DataLoader()
            all_karakin_landings = dataLoader.loadAllParachuteLandings(mapName='Summerland_Main')
            with open('all_karakin_landings.json', 'w') as f:
                json.dump(all_karakin_landings, f)
        elif args.plot_target == 'player_positions':
            dataLoader = DataLoader()
            #all_karakin_player_positions = dataLoader.loadAllPlayerPositions(mapName='Summerland_Main')
            #all_karakin_player_positions = []

        print('caching complete')
        return
    
    if args.plot:
        if args.plot_target == 'karakin_landings':
            landings = None
            with open('all_karakin_landings.json') as f:
                landings = json.load(f)
            dataframe = np.zeros([2200,2200])
            for landing in landings:
                landing = landing['event']['character']['location']
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
        gc.collect()
        sys.exit(1)
