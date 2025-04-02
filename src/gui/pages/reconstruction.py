from tkinter.filedialog import askopenfilename
import ttkbootstrap as tb
from src.config.ir_config import FilterType, InterpolationType
from src.core.services import reconstruct_from_file
from src.utils.io_handler import load_file


class ReconstructionPage(tb.Frame):
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
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        self.path_var = tb.StringVar()
        self.theta_var = tb.IntVar(value=180)
        self.filter_type_var = tb.StringVar(value="NONE")
        self.interpolation_var = tb.StringVar(value="LINEAR")
        self.output_size_var = tb.IntVar(value=256)
        self.preserve_range_var = tb.BooleanVar(value=True)

        # Label
        reconstruct = tb.Label(self,
                         text="FBP Reconstruction",
                         font=("helvetica neue", 28, "bold"),
                         bootstyle="dark"
                         )
        reconstruct.grid(row=0, column=1, columnspan=4, sticky="n", padx=5, pady=(30, 0))

        # Path selector
        path_lbl = tb.Label(self, text="File Path:", font=("Helvetica", 12), bootstyle="default")
        path_lbl.grid(row=1, column=0, padx=(50,0), sticky="w")
        path_entry = tb.Entry(self, textvariable=self.path_var, width=35, bootstyle="warning")
        path_entry.grid(row=1, column=1, columnspan=4, sticky="ew")
        browse_btn = tb.Button(self, text="Browse", command=self.browse_file, bootstyle="warning")
        browse_btn.grid(row=1, column=5)

        # === Theta ===
        theta_lbl = tb.Label(self, text="Theta:", font=("Helvetica", 12), bootstyle="default")
        theta_lbl.grid(row=2, column=0, padx=(50,0), sticky="w")
        theta_entry = tb.Entry(self, textvariable=self.theta_var, bootstyle="warning")
        theta_entry.grid(row=2, column=1, columnspan=4, sticky="ew")

        # === Filter Type ===
        tb.Label(self, text="Filter Type:", font=("Helvetica", 12), bootstyle="default").grid(row=3, column=0, padx=(50,0), sticky="w")
        tb.Combobox(self, textvariable=self.filter_type_var, values=[ft.name for ft in FilterType], bootstyle="warning").grid(
            row=3, column=1, columnspan=4, sticky="ew", padx=(0, 10))

        # === Interpolation Type ===
        tb.Label(self, text="Interpolation:", font=("Helvetica", 12), bootstyle="default").grid(row=4, column=0, padx=(50,0), sticky="w")
        tb.Combobox(self, textvariable=self.interpolation_var, values=[i.name for i in InterpolationType], bootstyle="warning").grid(
            row=4, column=1, columnspan=4, sticky="ew", padx=(0, 10))

        # === Output Size ===
        tb.Label(self, text="Output Size:", font=("Helvetica", 12), bootstyle="default").grid(row=5, column=0, padx=(50,0), sticky="w")
        tb.Entry(self, textvariable=self.output_size_var, bootstyle="warning").grid(
            row=5, column=1, columnspan=4, sticky="ew")

        # === Preserve Range ===
        tb.Label(self, text="Preserve Range:", font=("Helvetica", 12), bootstyle="default").grid(row=6, column=0, pady=(0, 50), padx=(50,0), sticky="w")
        tb.Checkbutton(self, variable=self.preserve_range_var, bootstyle="warning").grid(
            row=6, column=1, columnspan=3, sticky="ew", padx=(10, 10), pady=(0, 60))

        # Default buttons
        back_btn = tb.Button(self,
                             text="Back to Home",
                             width=10,
                             padding=(5, 5),
                             bootstyle="warning",
                             command=lambda: controller.show_frame("HomePage")
                             )
        back_btn.grid(row=6, column=0, sticky="sw", padx=(30, 2), pady=30)

        result_btn = tb.Button(self,
                               text="Reconstruct",
                               width=10,
                               padding=(5, 5),
                               bootstyle="warning",
                               command=self.reconstruct
                               )
        result_btn.grid(row=6, column=5, sticky="se", padx=(2, 30), pady=30)

    def browse_file(self):
        path = askopenfilename(
            title="Select file",
            filetypes=[("Supported files", "*.png *.jpg *.jpeg *.h5")]
        )
        if path:
            self.path_var.set(path)

    def reconstruct(self):
        path = self.path_var.get()
        theta = self.theta_var.get()
        filter_type = FilterType[self.filter_type_var.get()]
        interpolation = InterpolationType[self.interpolation_var.get()]
        output_size = self.output_size_var.get()
        preserve_range = bool(self.preserve_range_var.get())

        # Load original
        try:
            file = load_file(path)
        except ValueError as e:
            tb.Messgebox.show_error(message=str(e), title="Incorrect File Type")

        result = reconstruct_from_file(path, theta, filter_type, output_size, interpolation, preserve_range)

        self.controller.frames["ReconstructionResultPage"].update_result(file, result)
        self.controller.show_frame("ReconstructionResultPage")