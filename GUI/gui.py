import tkinter
from tkinter import ttk
from data_handler import DataHandler

class ThresholdSelectorApp:
    def __init__(self, root):
        self.data_handler = DataHandler()  # Initialize the data handler

        root.title("Threshold Selector")
        frame = tkinter.Frame(root)
        frame.pack()

        # Frame for selecting I2C addresses
        i2c_addres_frame = tkinter.Frame(frame)
        i2c_addres_frame.grid(row=0, column=0)

        self.combobox_A1 = self.create_combobox(i2c_addres_frame, "A1", 0, 0, ["Vcc", "Gnd"])
        self.combobox_A0 = self.create_combobox(i2c_addres_frame, "A0", 1, 0, ["Vcc", "Gnd"])
        self.combobox_C1 = self.create_combobox(i2c_addres_frame, "C1", 0, 2, ["Vcc", "Gnd", "Float"])
        self.combobox_C0 = self.create_combobox(i2c_addres_frame, "C0", 1, 2, ["Vcc", "Gnd", "Float"])

        # Frame for threshold selection
        threshold_frame = tkinter.Frame(frame)
        threshold_frame.grid(row=1, column=0, pady=20, sticky="w")

        self.threshold_entries = self.create_threshold_entries(threshold_frame)

        # Textbox to apply the same value to all thresholds
        set_all_frame = tkinter.Frame(frame)
        set_all_frame.grid(row=2, column=0, pady=10, sticky="w")

        tkinter.Label(set_all_frame, text="Set All Thresholds:").grid(row=0, column=0, padx=20)
        self.set_all_entry = tkinter.Entry(set_all_frame, width=20)
        self.set_all_entry.grid(row=0, column=1, padx=10)

        # "Apply" button
        apply_frame = tkinter.Frame(frame)
        apply_frame.grid(row=3, column=0, padx=20, pady=10)

        apply_button = tkinter.Button(apply_frame, text="Apply", width=20, command=self.apply_changes)
        apply_button.pack()

        # "Reset" button
        reset_frame = tkinter.Frame(frame)
        reset_frame.grid(row=4, column=0, padx=20, pady=10)

        reset_button = tkinter.Button(reset_frame, text="Reset", width=20, command=self.reset_values)
        reset_button.pack()

    def create_combobox(self, parent, label, row, col, values):
        # Create and return a combobox for selecting I2C addresses
        tkinter.Label(parent, text=label).grid(row=row, column=col, padx=10)
        combobox = ttk.Combobox(parent, values=values)
        combobox.grid(row=row, column=col + 1, padx=10, pady=10)
        return combobox

    def create_threshold_entries(self, parent):
        # Create and return dictionary of Entry widgets for threshold values
        labels = ["In0_A/Trigger", "In0_B", "In1", "In2", "In3", "In4", "In5", "In6", "In7", "In8", "In9", "In10", "In11", "In12", "In13", "In14"]
        entries = {}
        for i, label in enumerate(labels):
            tkinter.Label(parent, text=label).grid(row=i, column=0, padx=20, pady=5)
            entry = tkinter.Entry(parent)
            entry.grid(row=i, column=1, padx=20, pady=5)
            entries[label] = entry
        return entries

    def apply_changes(self):
        # Retrieve the data from comboboxes
        addrres = DataHandler.get_i2c_address(self)
        thresholds = DataHandler.get_threshold(self)
        # Pass the data to the handler
        self.data_handler.handle_data(addrres, thresholds)
    

    def reset_values(self):
        # Reset all the text boxes (In0_A/Trigger to In14) to zero, excluding the comboboxes
        for label, entry in self.threshold_entries.items():
            entry.delete(0, tkinter.END)
            entry.insert(0, "0")  # Set all entries to zero

        # Reset the "Set All Thresholds" entry to zero
        self.set_all_entry.delete(0, tkinter.END)
        self.set_all_entry.insert(0, "0")  # Set "Set All Thresholds" to zero

        # Create the data to pass to the handler, without touching A1, A0, C1, C0
        i2c_data = {
            "A1": self.combobox_A1.get(),
            "A0": self.combobox_A0.get(),
            "C1": self.combobox_C1.get(),
            "C0": self.combobox_C0.get(),
        }
        
        threshold_data = {}
        for label in self.threshold_entries:
            threshold_data[label] = "0"  # Set all thresholds to "0"

        # Update the data through the handler
        self.data_handler.handle_data(i2c_data, threshold_data)

if __name__ == "__main__":
    window = tkinter.Tk()
    app = ThresholdSelectorApp(window)
    window.mainloop()
