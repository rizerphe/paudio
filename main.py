from tkinter import filedialog
from tkinter import *
from pydub import AudioSegment
from pydub.playback import play as pydub_play
from threading import Thread
from threading import Event
import pickle
root = Tk()
root.title('paudio')
c = Canvas(root, width=500, height=500)
c.pack()
audios = []
threads = []


class Play(Thread):
    def __init__(self, segment):
        Thread.__init__(self)
        self.segment = segment
        self.setName('SoundThread')
    def run(self):
        pydub_play(self.segment)


def add():
    global audios
    s = filedialog.Open(root).show()
    c.create_rectangle(0, 240, 500, 260, fill='white')
    c.create_text(250, 250, text='wait please,\nloading audio file...')
    c.update()
    if s.endswith('mp3'):
        u = AudioSegment.from_mp3(s)
    elif s.endswith('wav'):
        u = AudioSegment.from_wav(s)
    else:
        return
    audios.append([True, s, u])
def play():
    for a, s, f in audios:
        if a:
            pydub_play(f)
def launch():
    global threads
    threads = []
    for a, s, f in audios:
        if a:
            threads.append(Play(f))
    for t in threads:
        t.start()
def save():
    path = filedialog.SaveAs(root).show()
    pickle.dump(audios, open(path, 'wb'))
def openF():
    global audios
    path = filedialog.Open(root).show()
    audios = pickle.load(open(path, 'rb'))


menubar = Menu(root)
menubar.add_command(label="Add file", command=add)
menubar.add_command(label="Play", command=launch)
menubar.add_command(label="Play one-by-one", command=play)
menubar.add_command(label="Open", command=openF)
menubar.add_command(label="Save as", command=save)
menubar.add_command(label="Quit", command=quit)
root.config(menu=menubar)


def select(evt):
    n = evt.y//20-1
    if len(audios) > n:
        if evt.x > 30:
            audios[n][0] = not audios[n][0]
        else:
            del audios[n]
c.bind('<Button-1>', select)


while True:
    c.delete('all')
    c.create_rectangle(0, 0, 500, 500, fill='white')
    n = 0
    for active, path, data in audios:
        c.create_rectangle(100, 0+n*20, 500, 20+n*20, fill='green')
        c.create_text(300, 10+n*20, text=path)
        c.create_text(15, 10+n*20, text='X', fill='red')
        if active:
            c.create_rectangle(45, 5+n*20, 55, 15+n*20, fill='green')
        else:
            c.create_rectangle(45, 5+n*20, 55, 15+n*20)
        n += 1
    root.update()
