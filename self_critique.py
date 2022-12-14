import tkinter as tk
import random

filename = "critiques_list.txt"
window = tk.Tk()

greeting = tk.Label(text="Hello, Viewer!")
greeting.pack()

with open(filename, 'r') as f:
    line_list = f.read().split('\n')
    critique = tk.label(text=random.choice(line_list))
    critique.pack()
