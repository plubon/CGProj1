from PIL import Image
from random import randint
from Cuboid import  Cuboid

class ImageManager:

    names = ["Random dithering", "Median cut color quantization"]
    palettes = ["3 bit", "16 colors", "6 bit", "256 colors", "9 bit", "12 bit", "15 bit", "18 bit"]
    nums = [8, 16, 64, 256, 512, 4096, 32768, 262144]

    def __init__(self):
        self.image = None
        self.copy = None
        self.raster = None
        self.matrix = None
        self.anchor = None
        self.k = None
        self.palette = None

    def getgrayscale(self, x, y):
        sum = 0
        for t in range(3):
            sum = sum + self.raster[x, y][t]
        return sum // 3

    def setgrayscale(self, x, y, val):
        newpix = (val, val, val)
        self.raster[x, y] = newpix

    def loadimage(self, path):
        self.image = Image.open(path)
        self.raster = self.image.load()

    def mediancut(self):
        v = ImageManager.nums[ImageManager.palettes.index(self.palette)]
        pixellists = []
        pixels = []
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                pixels.append(self.raster[x, y])
        pixellists.append(pixels)
        while len(pixellists) < v:
            newlist = []
            for item in pixellists:
                maxval = [1, -1, -1]
                minval = [300, 300, 300]
                for t in range(3):
                    maxval[t] = max(item, key=lambda f: f[t])[t]
                    minval[t] = min(item, key=lambda f: f[t])[t]
                diffs = [maxval[0]-minval[0], maxval[1]-minval[1], maxval[2] - minval[2]]
                splitcolor = diffs.index(max(diffs))
                item.sort(key=lambda tup: tup[splitcolor])
                newlist.append(item[:len(item)/2])
                newlist.append(item[len(item)/2:])
            pixellists = newlist
        cuboids = []
        for item in pixellists:
            tuples = []
            for t in range(3):
                    tuples.append((min(item, key=lambda f: f[t])[t], max(item, key=lambda f: f[t])[t]))
            cuboids.append(Cuboid(tuples[0], tuples[1], tuples[2]))
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                for cuboid in cuboids:
                    if cuboid.containspixel(self.raster[x, y]):
                        self.raster[x, y] = cuboid.color
                        break



    def randomdither(self):
        print self.k
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                thresholds = []
                for z in range(self.k-1):
                    added = False
                    while not added:
                        val = randint(1, 254)
                        if val not in thresholds:
                            thresholds.append(val)
                            added = True
                thresholds.sort()
                val = self.getgrayscale(x, y)
                changed = False
                for t in range(len(thresholds)):
                    if val < thresholds[t]:
                        self.setgrayscale(x, y, (255//(self.k-1))*t)
                        changed = True
                        break
                if not changed:
                    self.setgrayscale(x, y, 255)



    def transform(self, name, k, palette):
        self.k = k
        self.palette = palette
        if name == ImageManager.names[0]:
            self.randomdither()
        if name == ImageManager.names[1]:
            self.mediancut()

