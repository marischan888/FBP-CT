import os

from matplotlib import pyplot as plt
from ttkbootstrap.dialogs.dialogs import Messagebox

from tkinter.filedialog import *
import ttkbootstrap as tb


class SimulationResultPage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ## grid config
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        # Title
        self.result_label = tb.Label(self, text="Simulation Result", font=("Helvetica", 28, "bold"),
                                     bootstyle="dark")
        self.result_label.grid(row=0, column=0, columnspan=6, pady=(30, 10), sticky="n")

        # === Sinogram Label ===
        self.original_label = tb.Label(self, text="Original Image", font=("Helvetica", 15), bootstyle="dark")
        self.original_label.grid(row=1, column=0, columnspan=3, pady=(5, 0))

        # === Reconstructed Image Label ===
        self.recon_label = tb.Label(self, text="Simulated Sinogram", font=("Helvetica", 15), bootstyle="dark")
        self.recon_label.grid(row=1, column=3, columnspan=3, pady=(5, 0))

        # === Original Image ===
        self.original_canvas = tb.Label(self)
        self.original_canvas.grid(row=2, column=0, columnspan=3, padx=(50, 0), pady=10)

        # === Simulated Sinogram ===
        self.simu_canvas = tb.Label(self)
        self.simu_canvas.grid(row=2, column=3, columnspan=3, pady=10)

        # === Save Image Section ===
        inner = tb.Frame(self)
        inner.grid(row=3, column=0, columnspan=6)
        self.path_var = tb.StringVar()
        self.filename_var = tb.StringVar()

        inner.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)
        inner.columnconfigure(2, weight=1)
        inner.columnconfigure(3, weight=1)
        inner.columnconfigure(4, weight=1)
        inner.columnconfigure(5, weight=1)

        # Save Path
        path_lbl = tb.Label(inner, text="Path:", font=("Helvetica", 12), bootstyle="default", width=10)
        path_lbl.grid(row=3, column=0, sticky="w", padx=(50, 10), pady=(20, 10))

        path_entry = tb.Entry(inner, textvariable=self.path_var, width=20, bootstyle="warning")
        path_entry.grid(row=3, column=1, padx=(5, 5), pady=(20, 10))

        browse_btn = tb.Button(inner, text="Browse", command=self.browse_file, bootstyle="warning", width=10)
        browse_btn.grid(row=3, column=2, padx=(10, 20), pady=(20, 10))

        # File Name
        filename_lbl = tb.Label(inner, text="File Name:", font=("Helvetica", 12), bootstyle="default", width=15)
        filename_lbl.grid(row=3, column=3, sticky="e", padx=(20, 5), pady=(20, 10))

        filename_entry = tb.Entry(inner, textvariable=self.filename_var, width=20, bootstyle="warning")
        filename_entry.grid(row=3, column=4, sticky="w", padx=(0, 10), pady=(20, 10))

        # Save Button
        save_btn = tb.Button(inner,
                             text="Save",
                             bootstyle="warning",
                             command=self.save_recon,
                             width=10)
        save_btn.grid(row=3, column=5, sticky="w", padx=(10, 20), pady=(20, 10))

        # === Navigation Buttons ===
        self.back_home_btn = tb.Button(self,
                                       text="Back to Home",
                                       width=20,
                                       command=lambda: controller.show_frame("HomePage"),
                                       bootstyle="warning")
        self.back_home_btn.grid(row=4, column=0, pady=30, padx=(20, 0))

        self.back_recon_btn = tb.Button(self,
                                        text="Back to Simulation",
                                        width=20,
                                        command=lambda: controller.show_frame("SimulationPage"),
                                        bootstyle="warning")
        self.back_recon_btn.grid(row=4, column=5, pady=30, padx=(0, 20))

    def update_result(self, original, result):
        from PIL import Image, ImageTk
        import numpy as np
        def to_tk_image(img_array, size):
            color_map = plt.get_cmap('gray')
            img_array = color_map(img_array / np.max(img_array))
            img_array = (img_array * 255.9999).astype(np.uint8)
            img_pil = Image.fromarray(img_array)
            img_pil = img_pil.resize(size)
            return ImageTk.PhotoImage(img_pil)

        self.result = result
        self.original_img = to_tk_image(original, (256, 256))  ## only for dispaly
        self.result_img = to_tk_image(self.result, (256, 256))  ## result output size will not change

        self.original_canvas.configure(image=self.original_img)
        self.simu_canvas.configure(image=self.result_img)

    def browse_file(self):
        directory = askdirectory(title="Select Save Location")
        if directory:
            self.path_var.set(directory)

    def save_recon(self):
        from src.utils.io_handler import save_result

        path = self.path_var.get().strip()
        filename = self.filename_var.get().strip()

        if not path or not filename:
            print("Path or filename is missing.")
            return

        # Use the full filename directly (with extension)
        full_path = os.path.join(path, filename)

        try:
            save_result(self.result, full_path)  # your utility handles h5/image
            Messagebox.ok(title="Save Result", message="File successfully saved.")
        except Exception as e:
            Messagebox.show_error(title="Save Result", message=str(e))
