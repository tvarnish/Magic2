import tkinter as Tk
import tkinter.ttk as ttk
import magic2gui.callbacks as m2callbacks
import magic2gui.matplotlib_frame as m2mframe
import magic2gui.status_bar as m2status_bar
from matplotlib.pyplot import imread
import numpy as np


class Options:
    def __init__(self):
        self.objects = {
            "background": {
                "canvas": None,
                "fringes": None
            },
            "plasma": {
                "canvas": None,
                "fringes": None
            }
        }
        self.fig = None
        self.ax = None
        self.labeller = None
        self.status = None
        self.current = None
        self.fringes_or_map = 'fringes'
        self.show = None


def main():
    root = Tk.Tk()
    root.wm_title("Magic2")
    options = Options()

    menu = Tk.Menu(root)
    root.config(menu=menu)

    filemenu = Tk.Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Open background image",
                         command=lambda:
                         m2callbacks.open_image(options, 'background'))
    filemenu.add_command(label="Open plasma image",
                         command=lambda:
                         m2callbacks.open_image(options, 'plasma'))

    options.mframe = m2mframe.GraphFrame(root, bind_keys=True, show_toolbar=True)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    options.mframe.grid(row=0, column=0, sticky=("N", "S", "E", "W"))
    options.fig = options.mframe.fig
    options.ax = options.mframe.ax
    options.ax.imshow(imread('logo.png'))

    side_frame = Tk.Frame(root)
    side_frame.grid(row=0, column=1, padx=5, pady=5, sticky="N")

    display_group = Tk.LabelFrame(side_frame, text="Display", padx=5, pady=5)
    display_group.pack(fill=Tk.BOTH)

    display_modes = [
        ("Background fringes", "background_fringes"),
        ("Background map", "background_map"),
        ("Plasma fringes", "plasma_fringes"),
        ("Plasma map", "plasma_map")
    ]
    options.show = Tk.StringVar()
    for name, key in display_modes:
        b = ttk.Radiobutton(display_group, text=name, variable=options.show,
                            value=key, command=lambda: m2callbacks.show_image(options))
        b.pack(anchor=Tk.W)

    operations_group = Tk.LabelFrame(side_frame, text="Operations", padx=5, pady=5)
    operations_group.pack(fill=Tk.BOTH)

    b = ttk.Button(operations_group, text="Interpolate",
                   command=lambda: m2callbacks.interpolate(options))
    b.pack()

    options.status = m2status_bar.StatusBar(root)
    options.status.grid(row=1, columnspan=2, sticky=("W", "E"))
    # status.set("waiting",-1)

    root.mainloop()


if __name__ == "__main__":
    main()
