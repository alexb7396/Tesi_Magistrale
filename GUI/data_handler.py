import tkinter
from tkinter import ttk
import struct
import binascii

lookup_table_C1C0 = [
    ['Gnd',     'Gnd',      '00010000'],
    ['Gnd',     'Float',    '00010001'],
    ['Gnd',     'Vcc',      '00010010'],
    ['Float',   'Gnd',      '00010011'],
    ['Float',   'Float',    '00100000'],
    ['Float',   'Vcc',      '00100001'],
    ['Vcc',     'Gnd',      '00100010'],
    ['Vcc',     'Float',    '00100011'],
    ['Vcc',     'Vcc',      '00110000'],
]

lookup_table_A1A0 = [
    ['Gnd', 'Gnd', '00001100'],
    ['Gnd', 'Vcc', '00001101'],
    ['Vcc', 'Gnd', '00001110'],
    ['Vcc', 'Vcc', '00001111'],
]

dac_addresses = [
    "0000", "0001", "0010", "0011",
    "0100", "0101", "0110", "0111",
    "1000", "1001", "1010", "1011",
    "1100", "1101"
]

command = 48 # 0011 shifted by 4 in integer

array_of_bytes = []

class DataHandler:
    def __init__(self):
        # Dizionario per salvare i valori delle soglie precedenti
        self.previous_threshold_data = {}

    def find_address(self, address, lookup_table, key):
        for row in lookup_table:
            # Confronta i primi due elementi della riga con l'input
            if row[0] == address[key[0]] and row[1] == address[key[1]]:
                return row[2]  # Restituisci il terzo elemento
        return None 

# Funzione per trovare l'indirizzo
    def get_address(self, ca1, ca2):
        for row in lookup_table_C1C0:
            if row[0] == ca1 and row[1] == ca2:
                return row[2]  # Restituisce l'indirizzo
        return "Indirizzo non trovato: controlla i valori di ca1 e ca2"

    def handle_data(self, i2c_data, threshold_data):
    
            ltc_address = self.find_address(i2c_data, lookup_table_C1C0, ["C1", "C0"])
            ltc_addres_str = bin(int(ltc_address,2))[2:]
            ad56_address = self.find_address(i2c_data, lookup_table_A1A0, ["A1", "A0"])
            ad56_addres_str = bin(int(ad56_address,2))[2:]
            
            # first byte for i2c address
            ltc_address = int(ltc_address, 2)
            ad56_address = int(ad56_address, 2)
            # list of data received from gui
            threshold_data = list(threshold_data.values())

            for i in range(0,16):
            # third e fourth byte (composed by 12 bit of data and 4 bit of padding)
                msb, lsb = self.map_value_to_16bit(float(threshold_data[i]))
                msb_ = bin(msb)[2:]
                lsb_ = bin(lsb)[2:]
                if i<2 :
                    # second byte (command + dac address)
                    dac_address = command + int(dac_addresses[i],2)
                    #print concatenated binary
                    dac_address_str = bin(dac_address)[2:]
                    print("LTC:")
                    print(ltc_addres_str + dac_address_str + msb_+ lsb_)
                    #conversion to byte
                    dac_address = struct.pack('>B', dac_address)
                    ltc_address_ = struct.pack('>B', ltc_address)
                    msb = struct.pack('>B',msb)
                    lsb = struct.pack('>B',lsb)
                    # concatenate 4 bytes 
                    bytes_ = ltc_address_ + dac_address +  msb + lsb
                    print(f"LTC:")
                    print(bytes_)
                else:
                    # second byte (command + dac address)
                    dac_address = command + int(dac_addresses[i-2],2)
                    #print concatenated binary
                    dac_address_str = bin(dac_address)[2:]
                    print(f"AD56:") 
                    print(ad56_addres_str + dac_address_str + msb_+ lsb_)
                    #conversion to byte
                    dac_address = struct.pack('>B', dac_address)
                    ad56_address_ = struct.pack('>B', ad56_address)
                    msb = struct.pack('>B',msb)
                    lsb = struct.pack('>B',lsb)
                    # concatenate 4 bytes
                    bytes_ = ad56_address_ + dac_address + msb + lsb 
                    print("AD56:") 
                    print(bytes_)
                
                array_of_bytes.append(bytes_)

    def map_value_to_16bit(self, x):

        mapped_value = int(((x + 1.25) / 2.5) * 4095)
        # Assicurati che il valore rientri nei limiti (da -2048 a +2047)
        if mapped_value > 4095:
            mapped_value = 4095
        elif mapped_value < 0:
            mapped_value = 0

        msb = mapped_value >> 4
        lsb = (mapped_value & 0xF) << 4

        return msb, lsb
    
    def get_i2c_address(self):
        i2c_data = {
            "A1": self.combobox_A1.get(),
            "A0": self.combobox_A0.get(),
            "C1": self.combobox_C1.get(),
            "C0": self.combobox_C0.get(),
        }
        return i2c_data

    def get_threshold(self):
        # Controlla se un valore è stato inserito in "Set All Thresholds"
        set_all_value = self.set_all_entry.get()
        threshold_data = {}

        if set_all_value:  # Se è presente un valore, applicalo ai campi specificati
            for label, entry in self.threshold_entries.items():
                if label in [f"In{i}" for i in range(1, 15)]:  # Campi da In1 a In14
                    entry.delete(0, tkinter.END)  # Cancella il contenuto della casella di testo
                    entry.insert(0, set_all_value)  # Inserisci il nuovo valore
                    threshold_data[label] = set_all_value
                elif label in ["In0_A/Trigger", "In0_B"]:  # Controlla anche In0_A/Trigger e In0_B
                    current_value = entry.get()
                    if current_value.strip():  # Se è presente un valore, aggiornalo
                        threshold_data[label] = current_value
                    else:  # Mantieni il valore precedente se non è stato inserito nulla
                        if label in self.data_handler.previous_threshold_data:
                            threshold_data[label] = self.data_handler.previous_threshold_data[label]
                        else:
                            threshold_data[label] = ""  # Valore predefinito
        else:  # Altrimenti aggiorna solo i campi con valori inseriti
            for label, entry in self.threshold_entries.items():
                current_value = entry.get()
                if current_value.strip():  # Se il valore non è vuoto, usalo
                    threshold_data[label] = current_value
                else:  # Mantieni il valore precedente se il campo è vuoto
                    if label in self.data_handler.previous_threshold_data:
                        threshold_data[label] = self.data_handler.previous_threshold_data[label]
                    else:
                        threshold_data[label] = ""  # Valore predefinito come stringa vuota

        # Salva lo stato corrente come nuovo stato precedente
        self.data_handler.previous_threshold_data = threshold_data

        return threshold_data
        
    

