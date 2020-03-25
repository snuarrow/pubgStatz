import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import json
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

def plotPlayerChronology(playerChronology: list):
    print(len(playerChronology))
    for event in playerChronology[:10]:
        print(json.dumps(event, indent=4))
        print('-------------------------')
