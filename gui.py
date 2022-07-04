from time import sleep
import tkinter as tk
import yaml


class View(tk.Tk):
    """The Graphical User Interface.
    
    Provides a GUI to facilitate the configuration, data collection, and
    model training processes.
    """

    def __init__(self, controller):
        super().__init__()
        self._controller = controller

        # Creating frames
        self._make_config_frame()
        self._make_data_collector_frame()
        self._make_instructions_frame()

        # Start from config frame
        self._switch_to(self._config_frame)

    def main(self) -> None:
        """Creates the GUI."""

        self.mainloop()

    def _switch_to(self, frame: tk.Frame) -> None:
        """Switches to a given frame."""

        frame.tkraise()

    """Methods to set up config frame."""

    def _make_config_frame(self) -> None:
        """Create the config frame."""

        # Frame
        self._config_frame = tk.Frame(self)
        self._config_frame.grid(row=0, column=0, sticky="nsew")
        
        # Labels and entries
        self._data = self._create_entry_param("data file path: ", 0)
        self._trained_model = self._create_entry_param("model file path: ", 1)
        self._num_epochs = self._create_entry_param("num_epochs: ", 2)
        self._lr = self._create_entry_param("learning rate: ", 3)
        self._batch_size = self._create_entry_param("batch size: ", 4)
        self._learning_capacity = self._create_entry_param("learning capacity: ", 5)
        self._num_sensors = self._create_entry_param("number of sensors: ", 6)
        self._gestures = self._create_entry_param("gestures: ", 7)
        self._num_reps = self._create_entry_param("number of repetitions: ", 8)
        self._num_sets = self._create_entry_param("number of sets: ", 9)

        # Confirm button
        self._confirm_btn = tk.Button(self._config_frame, text="CONFIRM", command=self._confirm)
        self._confirm_btn.grid(row=10, column=0, columnspan=2)

    def _create_entry_param(self,
                            name: str,
                            row: int) -> tk.Entry:
        """Creates the label and entry for a particular param.
    
        Returns:
            The corresponding entry instance.
        """

        tk.Label(self._config_frame, text=name).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(self._config_frame)
        entry.grid(row=row, column=1, sticky="e")
        return entry

    def _confirm(self) -> None:
        """Function that is called when the CONFIRM button is hit."""

        config_dict = {
            'filenames': {
                'data': self._data.get(),
                'trained_model': self._trained_model.get()
                }, 
            'hyperparams': {
                'num_epochs': int(self._num_epochs.get()),
                'lr': float(self._lr.get()),
                'batch_size': int(self._batch_size.get()),
                'learning_capacity': int(self._learning_capacity.get())
                },
            'general': {
                'num_sensors': int(self._num_sensors.get()),
                'gestures': self._gestures.get().split(", "),
                'num_reps': int(self._num_reps.get()),
                'num_sets': int(self._num_sets.get())
                }
            }
        with open("src/config.yaml", 'w') as configyaml:
            yaml.dump(config_dict, configyaml, default_flow_style=False)

        self._switch_to(self._data_collector_frame)

    def _collect_data(self) -> None:
        # Switch to instructions frame
        self._switch_to(self._instructions_frame)
        # Call the model(datacollector)'s run method
        for i in range(6):
            sleep(1) # Need this to slow the changes down
            self._controller.update_gesture('goodbye' if i%2 else 'hello')
            self.update_idletasks()
        
    def _make_data_collector_frame(self) -> None:
        self._data_collector_frame = tk.Frame(self)
        self._data_collector_frame.grid(row=0, column=0, sticky="nsew")

        data_collector_btn = tk.Button(self._data_collector_frame,
                                    text="COLLECT DATA",
                                    command=self._collect_data)
        data_collector_btn.grid(row=0, column=0)

    def _make_instructions_frame(self) -> None:
        self._instructions_frame = tk.Frame(self)
        self._instructions_frame.grid(row=0, column=0, sticky="nsew")

        self.curr_gesture = tk.StringVar()

        tk.Label(self._instructions_frame,
                 text="Current Gesture:").grid(row=0,
                                               column=0,
                                               sticky="w")

        tk.Label(self._instructions_frame,
                 textvariable=self.curr_gesture).grid(row=1, column=0)



