import ttkbootstrap as tb

class HomePage(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        inner = tb.Frame(self, bootstyle="default")
        inner.pack(padx=150, pady=150)

        # title
        title = tb.Label(
            inner,
            text="Select Services",
            font=("helvetica neue", 28, "bold"),
            bootstyle="dark",
            anchor="center"
        )
        title.pack(pady=(0, 20))

        # buttons
        reconstruct_btn = tb.Button(
            inner,
            text="Reconstruction",
            bootstyle="warning-outline",
            width=30,
            padding=(10, 10),
            command=lambda: controller.show_frame("ReconstructionPage")
        )
        reconstruct_btn.pack(pady=10)

        simulate_btn = tb.Button(
            inner,
            text="Simulation",
            bootstyle="warning-outline",
            width=30,
            padding=(10, 10),
            command=lambda: controller.show_frame("SimulationPage")
        )
        simulate_btn.pack(pady=10)