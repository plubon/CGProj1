import Tkinter as Tk
import tkFileDialog
from ImageManager import ImageManager
from PIL import ImageTk


class MainWindow(Tk.Tk):

    def __init__(self):
        Tk.Tk.__init__(self)
        self.filechooseoptions=self.getfilechooseoptions()
        self.currentFileName = None
        self.imageLabel = None
        self.photo = None
        self.toppanel = None
        self.botpanel = None
        self.combobox = None
        self.filter = None
        self.size = None
        self.scale = None
        self.entries = []
        self.checkboxes = []
        self.checked = None
        self.palette = None
        self.bits = None
        self.combopal = None
        self.pal = None
        self.manager = ImageManager()
        self.initialize()

    def initialize(self):
        self.title = "CGP2"
        self.toppanel = Tk.Frame(self)
        self.toppanel.pack(side=Tk.TOP)
        self.botpanel = Tk.Frame(self)
        self.botpanel.pack()
        self.rightpanel = Tk.Frame(self)
        self.rightpanel.pack(side=Tk.RIGHT)
        Tk.Button(self.toppanel, text="Choose an image", command=self.fileselecthandler).pack(side=Tk.LEFT)
        Tk.Button(self.toppanel, text="Transform", command=self.transform).pack(side=Tk.LEFT)
        self.imageLabel = Tk.Label(self.botpanel)
        self.imageLabel.pack()
        combooptions = ["Random dithering", "Median cut color quantization"]
        palettes = ["3 bit", "16 colors", "6 bit", "256 colors", "9 bit", "12 bit", "15 bit", "18 bit"]
        self.filter = Tk.StringVar(self)
        self.pal = Tk.StringVar(self)
        self.filter.set(combooptions[0])
        self.pal.set(palettes[0])
        self.combobox = apply(Tk.OptionMenu, (self.toppanel, self.filter)+tuple(combooptions))
        self.combobox.pack(side=Tk.LEFT)
        self.combopal = apply(Tk.OptionMenu, (self.toppanel, self.pal) + tuple(palettes))
        self.combopal.pack()
        self.size = Tk.IntVar(self)
        self.scale = Tk.Scale(self.rightpanel, from_=2, to_=16, tickinterval=1, variable=self.size)
        self.scale.set(3)
        self.scale.pack()
        self.size.set(2)
        self.mainloop()

    def getfilechooseoptions(self):
        options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('jpg files', '.jpg'), ('all files', '.*')]
        options['initialdir'] = 'C:\\'
        options['title'] = 'Choose an image'
        return options

    def fileselecthandler(self):
        self.currentFileName = tkFileDialog.askopenfilename(**self.filechooseoptions)
        if self.currentFileName:
            self.loadimage()

    def loadimage(self):
        self.manager.loadimage(self.currentFileName)
        self.drawimage()

    def drawimage(self):
        if self.photo is None and self.imageLabel is None:
            self.photo = ImageTk.PhotoImage(self.manager.image)
            self.imageLabel = Tk.Label(self, image=self.photo).pack()
        else:
            self.photo = ImageTk.PhotoImage(self.manager.image)
            self.imageLabel.configure(image = self.photo)
            self.imageLabel.image = self.photo

    def transform(self):
        if self.manager.image is None:
            return
        self.manager.transform(self.filter.get(), self.scale.get(), self.pal.get())
        self.drawimage()

if __name__ == "__main__":
    mw = MainWindow()

