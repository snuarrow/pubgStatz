import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy import misc
from PIL import Image
import cv2

class Animator:
    def __init__(self, fps: int):
        self.width = 1920
        self.height = 1920
        self.fps = fps
        self.x_offset = 700
        self.y_offset = 700
        self.scalar = 0.947 * 0.01

    def _scale_location(self, event: dict):
        location = event['character']['location']
        x = (location['x'] - self.x_offset) * self.scalar
        y = (location['y'] - self.y_offset) * self.scalar
        z = float(location['z'])
        return int(x), int(y), int(z)


    def _make_gradients(self, event_frames: list, kernel_size: int):
        gradients = [np.zeros((self.width, self.height)) for _ in range(len(event_frames))]
        for i, event_frame in enumerate(event_frames):
            print(f'generating gradient: {i+1}/{len(event_frames)}')
            for event in event_frame:
                x, y, _ = self._scale_location(event)
                try:
                    gradients[i][y][x] += 1
                except IndexError:
                    pass

        def gkern(kernlen, std):
            """Returns a 2D Gaussian kernel array."""
            gkern1d = signal.gaussian(kernlen, std=std).reshape(kernlen, 1)
            gkern2d = np.outer(gkern1d, gkern1d)
            return gkern2d

        kernel = gkern(51, 7)


        for i, gradient in enumerate(gradients):
            print(f'convolving: {i+1}/{len(gradients)}')
            gradients[i] = signal.convolve2d(gradient, kernel, boundary='symm', mode='same')
            #plt.imshow(gradients[i], interpolation='none')
        return gradients

    def _relative_gradient(self, normal, target):
        #highest = 0
        relative_gradient = np.zeros((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                t = target[x][y]
                n = normal[x][y]
                

                #if n == 0:
                #    relative_win = 0
                #else:
                #    relative_win = max(min(t/n, 1), 0)
                

                #if relative_win != 0:
                #    print(f't: {t}, n: {n}, rel: {relative_win}')
                #print(relative_win)
                #if relative_win > highest:
                #    highest = relative_win
                #print(relative_win * 50)
                relative_gradient[x][y] = t/(n+1)
        #print(f'highest {highest}')
        #for x in range(self.width):
        #    for y in range(self.height):
        #        relative_gradient[x][y] *= 255/highest
        return relative_gradient

    def _convert_to_rgb(self, gradient):
        out = np.zeros((self.width, self.height, 3), np.uint8)
        for x in range(self.width):
            for y in range(self.height):
                #out[x][y][0] += min(gradient[x][y] * 1, 255)
                out[x][y][1] += min(gradient[x][y] * 300, 255)
                #out[x][y][2] += min(gradient[x][y] * 100, 255)
        return Image.fromarray(out)

    def animate_winners(self):
        all_positions = []
        winner_positions = []

        frames = len(all_positions)
        
        with open('winner_positions_animation.json') as f:
            winner_positions = json.load(f)

        with open('all_positions_animation.json') as f:
            all_positions = json.load(f)

        #start = 23
        #stop = 30

        #all_positions = all_positions[start:stop]
        #winner_positions = winner_positions[start:stop]

        gradients_all = self._make_gradients(all_positions, 101)
        
        gradients_winner = self._make_gradients(winner_positions, 101)
        

        karakin_img = Image.open('karakin.jpg').convert('RGB')

        results = []

        relative_gradients = []

        #def to_json(numpy_array):
            
        #    json.dump(numpy_array.tolist())

        for i, (all_gradient, winner_gradient) in enumerate(zip(gradients_all, gradients_winner)):
            #plt.imshow(all_gradient)
            #plt.show()
            #plt.imshow(winner_gradient)
            #plt.show()
            print(f'calculating relative gradient: {i+1}/{len(gradients_all)}')
            relative_gradient = self._relative_gradient(all_gradient, winner_gradient)
            relative_gradients.append(relative_gradient)

        #with open('relative_gradients.json', 'w') as f:
        #    json.dump(relative_gradients, f)

        for i, relative_gradient in enumerate(relative_gradients):
            #plt.imshow(relative_gradient)
            #plt.show()
            #exit(1)
            print(f'coloring gradient: {i+1}/{len(relative_gradients)}')
            rgb_gradient = self._convert_to_rgb(relative_gradient)
            snapshot = Image.blend(karakin_img, rgb_gradient, alpha=0.7)
            #snapshot.show()
            #exit()
            results.append(snapshot)

        videodims = (self.width,self.height)
        fourcc = cv2.VideoWriter_fourcc(*'avc1')    
        video = cv2.VideoWriter("yoloyolo.mp4",fourcc, self.fps,videodims)
        #img = Image.new('RGB', videodims, color = 'darkred')
        #draw stuff that goes on every frame here
        for i, snapshot in enumerate(results):
            print(f'rendering mp4: {i+1} /  {len(results)}')
            imtemp = snapshot.copy()
            # draw frame specific stuff here.
            video.write(cv2.cvtColor(np.array(imtemp), cv2.COLOR_RGB2BGR))
        video.release()

        
        #print(karakin_img.size)
        #result = self._convert_to_rgb(relative_gradient)
        #print(result.size)
        #snapshot = Image.blend(karakin_img, result, alpha=0.7)

        #snapshot.show()



        

