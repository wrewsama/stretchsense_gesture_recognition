import tkinter as tk

window = tk.Tk()
window.title("test")

def switch_to(frame: tk.Frame) -> None:
    frame.tkraise()

"""Config frame setup."""
config_frame = tk.Frame(window)
config_frame.grid(row=0, column=0, sticky="nsew")

confirm_txt = tk.Label(config_frame, text="param")
confirm_txt.grid(row=0, column=0, sticky="w")

confirm_input = tk.Entry(config_frame)
confirm_input.grid(row=0, column=1, sticky="e")

confirm_btn = tk.Button(config_frame, text="CONFIRM", command=lambda:switch_to(data_collector_frame))
confirm_btn.grid(row=1, column=0, columnspan=2)

"""Data Collector frame setup."""
data_collector_frame = tk.Frame(window)
data_collector_frame.grid(row=0, column=0, sticky="nsew")

data_txt = tk.Label(data_collector_frame, text="data")
data_txt.pack()
data_collector_btn = tk.Button(config_frame, text="CONFIRM", command=lambda:switch_to(data_collector_frame))

"""Trainer frame setup."""
trainer_frame = tk.Frame(window)
trainer_frame.grid(row=0, column=0, sticky="nsew")


switch_to(config_frame)
window.mainloop()