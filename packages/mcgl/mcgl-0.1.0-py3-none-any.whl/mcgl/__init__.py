__version__ = "0.1.0"

import tkinter.ttk
import tkinter

class App:
  def __init__(self, title):
    self.title = title
    self.app = tkinter.Tk(screenName=title)