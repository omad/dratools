import threading
import time
from pathlib import Path
from tkinter import *
from tkinter import scrolledtext



class LogViewer(threading.Thread):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        print('thread started')
        window = Tk()
        window.title("Log Viewer")

        window.geometry('750x300')

        # Make the ScrolledText fill and resize with the window
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)

        txt = scrolledtext.ScrolledText(window, width=40, height=10)

        txt.grid(column=0, row=0, sticky='nsew')

        log_contents = Path(self.filename).read_text('utf8')

        txt.insert(INSERT, log_contents)
        window.mainloop()
        print('thread finished')


if __name__ == '__main__':
    viewer = LogViewer(r"C:\Users\u68320\oldpythonpath.txt")
    viewer.start()
    viewer.join()
