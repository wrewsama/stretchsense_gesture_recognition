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
        self._make_trainer_frame()
        self._make_peripheral_selection_frame()
        self._make_final_frame()

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

        if self._controller.load_peripheral_list():
            self._switch_to(self._peripheral_selection_frame)
        else:
            tk.messagebox.showerror("Error", "No Available Peripherals.")
        


    def _make_data_collector_frame(self) -> None:
        self._data_collector_frame = tk.Frame(self)
        self._data_collector_frame.grid(row=0, column=0, sticky="nsew")

        connect_btn = tk.Button(self._data_collector_frame,
                                text="COLLECT DATA",
                                command=self._collect_data)
        connect_btn.grid(row=0, column=0)

    def _connect_to_peripheral(self) -> None:
        self._controller.connect_to_peripheral()
        self._switch_to(self._data_collector_frame)


    def _make_peripheral_selection_frame(self) -> None:
        self._peripheral_selection_frame = tk.Frame(self)
        self._peripheral_selection_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(self._peripheral_selection_frame,
                 text="Select Peripheral:").grid(row=0,
                                                 column=0)

        self.peripherals = tk.Listbox(self._peripheral_selection_frame)
        self.peripherals.grid(row=2, column=0)

        data_collector_btn = tk.Button(self._peripheral_selection_frame,
                                    text="CONNECT",
                                    command=self._connect_to_peripheral)
        data_collector_btn.grid(row=3, column=0)

    def _make_instructions_frame(self) -> None:
        self._instructions_frame = tk.Frame(self)
        self._instructions_frame.grid(row=0, column=0, sticky="nsew")

        self.curr_text = tk.StringVar()

        tk.Label(self._instructions_frame,
                 text="Current Gesture:").grid(row=0,
                                               column=0)

        tk.Label(self._instructions_frame,
                 textvariable=self.curr_text).grid(row=1, column=0)

    def _collect_data(self) -> None:
        # Switch to instructions frame
        self._switch_to(self._instructions_frame)

        # Set the description
        tk.Label(self._instructions_frame,
                 text="Current Gesture:").grid(row=0,
                                               column=0)

        # Run the data collector
        self._controller.run_data_collector()

        # Switch to trainer frame
        self._switch_to(self._trainer_frame)
    
    def _make_trainer_frame(self) -> None:
        self._trainer_frame = tk.Frame(self)
        self._trainer_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(self._trainer_frame,
                 text="Data Collected").grid(row=0,
                                             column=0)
    
        train_btn = tk.Button(self._trainer_frame,
                                    text="TRAIN",
                                    command=self._train)
        train_btn.grid(row=1, column=0)

    def _train(self) -> None:
        self._controller.train()
        self._switch_to(self._final_frame)

    def _make_final_frame(self) -> None:
        self._final_frame = tk.Frame(self)
        self._final_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(self._final_frame,
                 text="Model Trained").grid(row=0,
                                            column=0)
    
        train_btn = tk.Button(self._final_frame,
                                    text="EXIT",
                                    command=self.destroy)
        train_btn.grid(row=1, column=0)

