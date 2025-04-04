import os
import sys

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import ttkbootstrap as tb
import tkinter as tk
from src.gui.pages.home import HomePage
from src.gui.pages.recon_result import ReconstructionResultPage
from src.gui.pages.reconstruction import ReconstructionPage
from src.gui.pages.simu_result import SimulationResultPage
from src.gui.pages.simulation import SimulationPage


class CTApp(tb.Window):
    def __init__(self):
        super().__init__(
            themename="flatly"
        )  # try: cosmo, flatly, litera, darkly
        self.title("CT Image Reconstruction")
        self.geometry("800x600")
        self.minsize(600, 400)
        self.resizable(True, True)

        container = tb.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for PageClass in [HomePage, ReconstructionPage,
                          ReconstructionResultPage, SimulationPage,
                          SimulationResultPage]:
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(column=0, row=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = CTApp()
    app.mainloop()
