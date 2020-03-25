#%matplotlib notebook

from PIL import Image, ImageFilter, ImageEnhance
import random
import numpy as np
from numpy import asarray
import json
import matplotlib
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import matplotlib.animation as animation
import cv2


big_data = []
with open('positions_animation.json') as f:
    big_data = json.load(f)

for i, a in enumerate(big_data):
    if i > 0:
        for b in a:
            big_data[i-1].append(b)
    

for a in big_data:
    print(len(a))

print(len(big_data))

#exit(1)

fps = 20
width = 1920
height = 1920

#snapshots = [ np.zeros((width,height)) for _ in range( len(big_data) ) ]
snapshots = [ np.zeros((width,height,4), np.uint8) for _ in range( len(big_data) ) ]
highest = 0
for i, frame in enumerate(big_data):
    #print(len(frame))
    print(f'{i+1} / {len(big_data)}')
    #if i < 25:
    #    continue
    for event in frame:
        location = event['character']['location']
        x = (location['x'] - 700) * 0.947
        y = (location['y'] - 700) * 0.947
        try:
            snapshots[i][int(y / 100)][int(x / 100)][0] = 255
            snapshots[i][int(y / 100)][int(x / 100)][1] = 128
            #snapshots[i][int(y / 100)][int(x / 100)][2] = 255
            snapshots[i][int(y / 100)][int(x / 100)][3] = 255
            #snapshots[i][int(y / 100)][int(x / 100)] += 10
            #if snapshots[i][int(y / 100)][int(x / 100)] > highest:
            #    highest = snapshots[i][int(y / 100)][int(x / 100)]
        except IndexError:
            pass

        #print(json.dumps(snapshots, indent=4, default=str))
        #exit(1)
    #snapshots[i] = gaussian_filter(snapshots[i], sigma=3)
    #break

#print(highest)
#factor = 255 / highest
img = Image.open("karakin.jpg")
img = img.convert('RGBA')


def convert_to_rgb(snapshots):
    out = np.zeros((width,height,3), np.uint8)
    #out = img
    for i in range(width):
        for j in range(height):
            t = snapshots[i][j]
            #print(t)
            #t *= factor
            m = img[i][j]
            #out[i][j] = img[i][j]
            #out[i][j][0] = t + m[0]
            #out[i][j][1] = t + m[1]
            #out[i][j][2] = t + m[2]
            out[i][j] = img[i][j] * 0.2
            if t != 0:
                f = 100
                out[i][j][0] = min(out[i][j][0] + f*t, 255)
                out[i][j][1] = min(out[i][j][1] + f*t, 255)
                out[i][j][2] = min(out[i][j][2] + f*t, 255)
            #else:
            #    out[i][j] = img[i][j] * 0.2

            #out[i][j][3] = 0.5
            #exit(1)
 
    return out

#snapshots[25] = convert_to_rgb(snapshots[25])
for q, snapshot in enumerate(snapshots):
    print(f'{q+1} / {len(snapshots)}')
    imr = Image.fromarray(snapshot)
    imr = imr.filter(ImageFilter.GaussianBlur(radius = 7))
    enhancer = ImageEnhance.Brightness(imr)
    imr = enhancer.enhance(3)
    enhancer = ImageEnhance.Contrast(imr)
    imr = enhancer.enhance(5.0)

    snapshot = Image.blend(img, imr, alpha=0.7)

    #snapshot.show()
    snapshots[q] = snapshot

    #snapshots[q].show()
    #exit(1)

videodims = (width,height)
fourcc = cv2.VideoWriter_fourcc(*'avc1')    
video = cv2.VideoWriter("test.mp4",fourcc, fps,videodims)
#img = Image.new('RGB', videodims, color = 'darkred')
#draw stuff that goes on every frame here
for i, snapshot in enumerate(snapshots):
    print(f'{i+1} /  {len(snapshots)}')
    imtemp = snapshot.copy()
    # draw frame specific stuff here.
    video.write(cv2.cvtColor(np.array(imtemp), cv2.COLOR_RGB2BGR))
video.release()

#snapshots[0].save('pillow_imagedraw.gif',
#               save_all=True, append_images=snapshots[1:], optimize=False, duration=5, loop=0)
exit(1)

#snapshots[25].show()
#exit(1)

#    snapshot = convert_to_rgb(snapshot)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure( figsize=(8,8) )
#img = plt.imread("airlines.jpg")
plt.gca().set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
a = snapshots[0]
im = plt.imshow(a)
plt.show()
exit(1)
def animate_func(i):
    if i % fps == 0:
        print( '.', end ='' )

    im.set_array(snapshots[i])
    return [im]

anim = animation.FuncAnimation(
                               fig, 
                               animate_func, 
                               frames = len(big_data),
                               interval = 1000 / fps, # in ms
                               )

anim.save('test_anim.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])

print('Done!')