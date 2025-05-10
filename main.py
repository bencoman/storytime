import tkinter as tk
from app import StoryTimeApp
from logutil import Log

if __name__ == "__main__":
    log = Log()
    root = tk.Tk()
    app = StoryTimeApp(root,log)
    root.mainloop()
