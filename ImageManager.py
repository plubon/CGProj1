from PIL import Image


class ImageManager:

    names = ["Inversion", "Brightness correction","Contrast Enhancement", "Gamma Correction", "Blur", "Gaussian", "Sharpen","Edge detection", "Emboss", "Custom"]

    def __init__(self):
        self.image = None
        self.copy = None
        self.raster = None
        self.matrix = None
        self.anchor = None
        self.rastercopy = None
        self.matrixsum = None

    def loadimage(self, path):
        self.image = Image.open(path)
        self.raster = self.image.load()

    def functionfilter(self, func):
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                newpix = (func(self.raster[i, j][0]), func(self.raster[i, j][1]), func(self.raster[i, j][2]))
                self.raster[i, j] = newpix

    def convolutionfilter(self):
        self.copy = self.image.copy()
        self.rastercopy = self.copy.load()
        self.matrixsum = 0
        for l in self.matrix:
            self.matrixsum += sum(l)
        if self.matrixsum == 0:
            self.matrixsum = 1
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                self.convolutepixel(i, j)
        self.image = self.copy

    def convolutepixel(self, i, j):
        newpx = [0, 0, 0]
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                px = self.raster[(i+x-self.anchor[0]) % self.image.size[0], (j+y-self.anchor[1]) % self.image.size[1]]
                for t in range(3):
                    newpx[t] += px[t] * self.matrix[x][y]
        for t in range(3):
            newpx[t] = newpx[t] // self.matrixsum
        self.rastercopy[i, j] = tuple(newpx)

    def transform(self, name, matrix, anchor):
        self.matrix = matrix
        self.anchor = anchor
        if name == ImageManager.names[0]:
            self.functionfilter(lambda x: 255-x)
        elif name == ImageManager.names[1]:
            self.functionfilter(lambda x: min(255, x+25))
        elif name == ImageManager.names[2]:
            self.functionfilter(lambda x: max(0,min(255, int(1.2*x-25))))
        elif name == ImageManager.names[3]:
            self.functionfilter(lambda x: int(255*(x/float(255)**0.9)))
        elif name == ImageManager.names[4]:
            self.matrix = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
            self.anchor = (1, 1)
            self.convolutionfilter()
        elif name == ImageManager.names[5]:
            self.matrix = [[0, 1, 0], [1, 4, 1], [0, 1, 0]]
            self.anchor = (1, 1)
            self.convolutionfilter()
        elif name == ImageManager.names[6]:
            self.matrix = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
            self.anchor = (1, 1)
            self.convolutionfilter()
        elif name == ImageManager.names[7]:
            self.matrix = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
            self.anchor = (1, 1)
            self.convolutionfilter()
        elif name == ImageManager.names[8]:
            self.matrix = [[-1, 0, 1], [-1, 1, 1], [-1, 0, 1]]
            self.anchor = (1, 1)
            self.convolutionfilter()
        elif name == ImageManager.names[9]:
            self.matrix = matrix
            self.anchor = anchor
            self.convolutionfilter()

