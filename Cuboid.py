class Cuboid:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.color = ((self.r[1]+self.r[0])/2, (self.g[1]+self.g[0])/2, (self.b[1]+self.b[0])/2)

    def containspixel(self, pix):
        return pix[0] >= self.r[0] and pix[0] <= self.r[1] and pix[1] >= self.g[0] and pix[1] <= self.g[1] and pix[2] >= self.b[0] and pix[2] <= self.b[1]
