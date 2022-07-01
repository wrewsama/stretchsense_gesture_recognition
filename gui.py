import tkinter as tk
import yaml

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

def confirm():
    config_dict = {
        'filenames': {
            'data': data.get(),
            'trained_model': trained_model.get()
            }, 
        'hyperparams': {
            'num_epochs': int(num_epochs.get()),
            'lr': float(lr.get()),
            'batch_size': int(batch_size.get()),
            'learning_capacity': int(learning_capacity.get())
            },
        'general': {
            'num_sensors': int(num_sensors.get()),
            'gestures': gestures.get().split(", "),
            'num_reps': int(num_reps.get()),
            'num_sets': int(num_sets.get())
            }
        }
    with open("src/config.yaml", 'w') as configyaml:
        yaml.dump(config_dict, configyaml, default_flow_style=False)

    switch_to(data_collector_frame)

confirm_btn = tk.Button(config_frame, text="CONFIRM", command=confirm)
confirm_btn.grid(row=10, column=0, columnspan=2)

"""Data Collector frame setup."""
data_collector_frame = tk.Frame(window)
data_collector_frame.grid(row=0, column=0, sticky="nsew")

"""TODO"""
def collect_data() -> None:
    pass

data_collector_btn = tk.Button(data_collector_frame,
                               text="COLLECT DATA",
                               command=collect_data)
data_collector_btn.grid(row=0, column=0)

"""Instructions frame setup"""
instructions_frame = tk.Frame(window)
tk.Label(instructions_frame, text="Current Gesture:").grid(row=0, column=0, sticky="w")

instructions_textbox = tk.Text(instructions_frame)
instructions_textbox.grid(row=1, column=0)

"""Trainer frame setup."""
trainer_frame = tk.Frame(window)
trainer_frame.grid(row=0, column=0, sticky="nsew")


switch_to(config_frame)
window.mainloop()
