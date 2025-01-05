import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title("Threshold Selecter")

frame = tkinter.Frame(window)
frame.pack()

# Frame for select i2c address
i2c_addres_frame = tkinter.Frame(frame)
i2c_addres_frame.grid(row = 0, column=0)

A1_label_addres = tkinter.Label(i2c_addres_frame, text = "A1")
A0_label_addres = tkinter.Label(i2c_addres_frame, text = "A0")
C1_label_addres = tkinter.Label(i2c_addres_frame, text = "C1")
C0_label_addres = tkinter.Label(i2c_addres_frame, text = "C0")

A1_label_addres.grid(row=0, column=0, padx=10)
A0_label_addres.grid(row=1, column=0, padx=10)
C1_label_addres.grid(row=0, column=2, padx=10)
C0_label_addres.grid(row=1, column=2, padx=10)

combobox_A1 = ttk.Combobox(i2c_addres_frame, values=["Vcc","Gnd"])
combobox_A0 = ttk.Combobox(i2c_addres_frame, values=["Vcc","Gnd"])
combobox_C1 = ttk.Combobox(i2c_addres_frame, values=["Vcc","Gnd","Float"])
combobox_C0 = ttk.Combobox(i2c_addres_frame, values=["Vcc","Gnd","Float"])

combobox_A1.grid(row=0, column=1, padx=10, pady=10)
combobox_A0.grid(row=1, column=1, padx=10)
combobox_C1.grid(row=0, column=3, padx=10)
combobox_C0.grid(row=1, column=3, padx=10)

# Frame for selection threshold
threshold_frame = tkinter.Frame(frame)
threshold_frame.grid(row=1, column=0, pady=20, sticky="w")

threshold_labels = ["In0_A/Trigger", "In0_B", "In1", "In2", "In3", "In4", "In5", "In6", "In7", "In8", "In9", "In10", "In11", "In12", "In13", "In14"]

for i, label in enumerate(threshold_labels):
    tkinter.Label(threshold_frame, text=label).grid(row=i, column=0, padx=20, pady=5)

    entry = tkinter.Entry(threshold_frame)
    entry.grid(row=i, column=1, padx=20, pady=5) 

# Apply button Frame
apply_frame = tkinter.Frame(frame)
apply_frame.grid(row = 3, column=0, padx=20, pady=10 )

apply_button = tkinter.Button(apply_frame, text="Apply", width=20)
apply_button.pack()

window.mainloop()

lookup_table_C1C0 = [
    ['Gnd',     'Gnd',      '0010000'],
    ['Gnd',     'Float',    '0010001'],
    ['Gnd',     'Vcc',      '0010010'],
    ['Float',   'Gnd',      '0010011'],
    ['Float',   'Float',    '0100000'],
    ['Float',   'Vcc',      '0100001'],
    ['Vcc',     'Gnd',      '0100010'],
    ['Vcc',     'Float',    '0100011'],
    ['Vcc',     'Vcc',      '0110000'],
]

lookup_table_A1A0 = [
    ['Gnd', 'Gnd', b'0001100'],
    ['Gnd', 'Vcc', b'0001101'],
    ['Vcc', 'Gnd', b'0001110'],
    ['Vcc', 'Vcc', b'0001111'],
]

# Funzione per trovare l'indirizzo
def get_address(ca1, ca2):
    for row in lookup_table_C1C0:
        if row[0] == ca1 and row[1] == ca2:
            return row[2]  # Restituisce l'indirizzo
    return "Indirizzo non trovato: controlla i valori di ca1 e ca2"