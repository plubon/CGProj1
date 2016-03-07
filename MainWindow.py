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
        self.checkboxesvals = []
        self.checkboxes=[]
        self.gridpanel = None
        self.checked = None
        self.manager = ImageManager()
        self.initialize()

    def initialize(self):
        self.title = "CGP1"
        self.toppanel = Tk.Frame(self)
        self.toppanel.pack(side=Tk.TOP)
        self.botpanel = Tk.Frame(self)
        self.botpanel.pack()
        self.rightpanel = Tk.Frame(self)
        self.rightpanel.pack(side=Tk.RIGHT)
        self.gridpanel = Tk.Frame(self.rightpanel)
        self.gridpanel.pack()
        Tk.Button(self.toppanel, text="Choose an image", command=self.fileselecthandler).pack(side=Tk.LEFT)
        Tk.Button(self.toppanel, text="Transform", command=self.transform).pack(side=Tk.LEFT)
        self.imageLabel = Tk.Label(self.botpanel)
        self.imageLabel.pack()
        combooptions = ["Inversion", "Brightness correction","Contrast Enhancement", "Gamma Correction", "Blur", "Gaussian", "Sharpen","Edge detection", "Emboss", "Custom"]
        self.filter = Tk.StringVar(self)
        self.filter.set(combooptions[0])
        self.combobox = apply(Tk.OptionMenu, (self.toppanel,self.filter)+tuple(combooptions))
        self.combobox.pack(side=Tk.LEFT)
        self.scale = Tk.Scale(self.rightpanel, from_=3, to_=15, tickinterval=2, variable=self.size)
        self.scale.bind("<ButtonRelease-1>", self.sliderhandler)
        self.scale.set(3)
        self.scale.pack()
        self.size = Tk.IntVar(self)
        self.size.set(3)
        self.drawgrid()
        self.mainloop()

    def drawgrid(self):
        for widget in self.gridpanel.winfo_children():
            widget.destroy()
        temp = self.size.get()
        self.checked=None

        for i in range(temp):
            for j in range(temp):
                panel = Tk.Frame(self.gridpanel)
                panel.grid(row=i, column=j)
                tempvar = Tk.IntVar()
                tempstr = Tk.IntVar()
                cb = Tk.Checkbutton(panel, variable=tempvar, command=self.handlecheckbox)
                cb.pack()
                if i == temp//2 and i == j:
                    cb.select()
                    tempvar.set(1)
                    self.checked = tempvar
                self.checkboxesvals.append(tempvar)
                self.checkboxes.append(cb)
                vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                Tk.Entry(panel, textvariable=tempstr, validate = 'key', validatecommand = vcmd).pack()
                self.entries.append(tempstr)

    def handlecheckbox(self):
        temp=None
        i=0
        for val in self.checkboxesvals:
            if self.checked is None:
                if val.get() == 1:
                    temp=val
                else:
                    self.checkboxes[i].deselect()
            else:
                if self.checked != val and val.get() == 1:
                    temp = val
                else:
                    self.checkboxes[i].deselect()
            i = i + 1
        self.checked=temp


    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

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

    def sliderhandler(self, event):
        x = self.scale.get()
        if int(x) % 2 == 0:
            self.size.set(int(x)+1)
        else:
            self.size.set(int(x))
        self.checkboxesvals=[]
        self.entries=[]
        self.checkboxes=[]
        self.drawgrid()

    def transform(self):
        if self.manager.image is None:
            return
        self.manager.transform(self.filter.get(), self.getfiltermatrix(), self.getanchor())
        self.drawimage()

    def getfiltermatrix(self):
        ret = [[]]
        i = 0
        for item in self.entries:
            if i != 0 and i % self.size.get() == 0:
                ret.append([])
            ret[i//self.size.get()].append(item.get())
            i += 1
        return ret

    def getanchor(self):
        idx = 0
        i = 0
        for item in self.checkboxesvals:
            if item.get() == 1:
                idx = i
            i += 1
        return (idx // self.size.get(), idx % self.size.get())


if __name__ == "__main__":
    mw = MainWindow()

