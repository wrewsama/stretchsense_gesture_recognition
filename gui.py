import tkinter as tk

window = tk.Tk()
window.title("test")

def switch_to(frame: tk.Frame) -> None:
    frame.tkraise()

"""Config frame setup."""
config_frame = tk.Frame(window)
config_frame.grid(row=0, column=0, sticky="nsew")

def create_param(name: str, row: int) -> tk.Entry:
    """Creates the label and entry for a particular param.
    
    Returns:
        The corresponding entry instance.
    """
    tk.Label(config_frame, text=name).grid(row=row, column=0, sticky="w")
    entry = tk.Entry(config_frame)
    entry.grid(row=row, column=1, sticky="e")
    return entry

data = create_param("data file path: ", 0)
trained_model = create_param("model file path: ", 1)
num_epochs = create_param("num_epochs: ", 2)
lr = create_param("learning rate: ", 3)
batch_size = create_param("batch size: ", 4)
learning_capacity = create_param("learning capacity: ", 5)
num_sensors = create_param("number of sensors: ", 6)
gestures = create_param("gestures: ", 7)
num_reps = create_param("number of repetitions: ", 8)
num_sets = create_param("number of sets: ", 9)

confirm_btn = tk.Button(config_frame, text="CONFIRM", command=lambda:switch_to(data_collector_frame))
confirm_btn.grid(row=10, column=0, columnspan=2)

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