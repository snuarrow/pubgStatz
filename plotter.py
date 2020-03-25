import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import json
from tools import DateTools
from scipy.ndimage.filters import gaussian_filter

#big_data = []
#with open('positions_animation.json') as f:
#    big_data = json.load(f)
#
#frames = []
#
#for i, interval in enumerate(big_data):
#    for event in interval:
#        print(json.dumps(event, indent=4, default=str))
#        exit(1)
#
#        location = event['character']['location']
#
#        try
#
#print(len(big_data))
#exit(0)
#uniform_data = np.random.rand(100,120)


#uniform_data = gaussian_filter(uniform_data, sigma=3)
#print(uniform_data)
#
#ax = sns.heatmap(uniform_data)
#plt.show()
#
#
#class Plotter:
#    def __init__(self):
#        print('yolo')

def plotPlayerChronology(playerChronology: list, matchStart: dict, matchEnd: dict):
    datetools = DateTools()
    matchStartTime = datetools.toDateTime_ms_accuracy(matchStart["_D"])
    matchEndTime = datetools.toDateTime_ms_accuracy(matchEnd["_D"])
    print(len(playerChronology))
    timestamps = []
    for event in playerChronology:
        ts = datetools.toDateTime_ms_accuracy(event["_D"])
        if datetools.inRange(matchStartTime, ts, matchEndTime):
            timestamps.append(ts)

    distances = []

    for i, ts in enumerate(timestamps[1:]):
        dist = abs((ts - timestamps[i-1]).total_seconds())
        if dist < 20:
            distances.append(dist)

    plt.hist(distances, density=True, bins=30)
    plt.show()
