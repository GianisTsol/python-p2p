import tkinter as tk
from tkinter.filedialog import askopenfilename
import threading

class gui(threading.Thread):
    def __init__(self):
        super(gui, self).__init__()



    def openfile(self):
       filename = askopenfilename(parent=self.window)
       #Todo file selction stuff



    def updateInfo(self, peers, knownpeers):
        for i in peers:
            listbox.insert(peers.index(i), i.host)

        my_label.config(text = "Connected Peers: " + str(len(peers)))
        my_label1.config(text = "Known Peers: " + str(len(knownpeers)))

    def run(self):
        self.window = tk.Tk()
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)


        self.window.geometry("500x200")
        frame1 = tk.Frame(master=self.window, width=200, height=100)
        frame2 = tk.Frame(master=self.window, width=200, height=100)

        listbox = tk.Listbox(frame1)

        my_label = tk.Label(frame2,
                         text = "Connected Peers: NaN")
        my_label1 = tk.Label(frame2,
                         text = "Total Known Peers: NaN")

        my_label.pack()
        my_label1.pack()

        listbox.pack()

        frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.window.mainloop()


a = gui()
a.start()

def updateInfo(peers, knownpeers):
    a.updateInfo(peers, knownpeers)
