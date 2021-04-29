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
        self.listbox.delete(0, tk.END)
        self.peers = peers
        for i in peers:
            self.listbox.insert(peers.index(i), i.host)

        self.my_label.config(text = "Connected Peers: " + str(len(peers)) + " | Total Known Peers: " + str(len(knownpeers)))

    def GetPeerInfo(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            for i in self.peers:
                if i.host == data:
                    self.info.delete(1.0, tk.END)
                    self.info.insert(1.0, "ID: " + i.id)
                    self.info.insert(2.0, "IP: " + i.host)

    def stop(self):
        self.window.quit

    def run(self):
        self.window = tk.Tk()
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)


        self.window.geometry("600x400")
        top1 = tk.Frame(master=self.window)
        top2 = tk.Frame(master=self.window, bg="grey45")
        top3 = tk.Frame(master=self.window)
        frame2 = tk.Frame(master=top1)
        frame3 = tk.Frame(master=top3)

        self.my_label = tk.Label(top1, text = "LOADING")
        self.my_label.pack()

        self.listbox = tk.Listbox(top2)
        #self.listbox.bindtags((str(self.listbox), str(self.window), "all"))
        self.listbox.bind("<<ListboxSelect>>", self.GetPeerInfo)
        self.listbox.pack(fill=tk.X)
        self.listbox.configure(bg="grey75", highlightthickness=0, relief="flat")

        self.info = tk.Text(top3, height=3, borderwidth=0)
        self.info.pack()
        self.info.configure(state="disabled")
        self.info.configure(bg=self.window.cget('bg'), relief="flat")

        self.messagebox = tk.Text(frame3, height=15, width=65, borderwidth=1)
        self.messagebox.pack()
        self.messagebox.configure(state="disabled")

        top1.pack(fill=tk.X)
        tk.Frame(master=self.window, height=1, bg="black").pack(fill=tk.X)
        top2.pack(fill=tk.X)
        tk.Frame(master=self.window, height=1, bg="black").pack(fill=tk.X)
        top3.pack(fill=tk.X)
        frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        frame3.pack(fill=tk.BOTH, expand=True)
        self.window.mainloop()


guic = gui()
guic.start()

def updateInfo(peers, knownpeers):
    guic.updateInfo(peers, knownpeers)
