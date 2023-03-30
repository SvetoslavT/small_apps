import os
import shutil
import tkinter as tk
from tkinter import filedialog
import win32api
from win32file import GetDriveType, DRIVE_REMOVABLE


class GarminUSBUtility:
    def __init__(self):
        self.garmin_folder = "Garmin"
        self.local_IMG_file_path = ""
        self.local_POI_file_path = ""
        self.usb_devices = ["D:\\", "F:\\", "H:\\", "J:\\", "L:\\", "N:\\", "P:\\", "R:\\"]
        self.device_counter = 0
        self.output_text = ""

        self.root = tk.Tk()
        self.root.title("Garmin USB Utility")
        self.root.geometry("500x300")

        self.img_file_label = tk.Label(self.root, text="Select IMG file:")
        self.img_file_label.pack(pady=(10, 0))
        self.img_file_button = tk.Button(self.root, text="Browse", command=self.browse_img_file)
        self.img_file_button.pack(pady=(0, 10))

        self.poi_file_label = tk.Label(self.root, text="Select POI file:")
        self.poi_file_label.pack()
        self.poi_file_button = tk.Button(self.root, text="Browse", command=self.browse_poi_file)
        self.poi_file_button.pack(pady=(0, 10))

        self.process_button = tk.Button(self.root, text="Start Process", command=self.start_processing)
        self.process_button.pack(pady=(10, 0))

        self.output_label = tk.Label(self.root, text="")
        self.output_label.pack()

    def browse_img_file(self):
        self.local_IMG_file_path = filedialog.askopenfilename(filetypes=[("IMG Files", "*.img")])

    def browse_poi_file(self):
        self.local_POI_file_path = filedialog.askopenfilename(filetypes=[("POI Files", "*.gpi")])


    def start_processing(self):
        if not self.local_IMG_file_path or not self.local_POI_file_path:
            self.output_label.config(text="Please select IMG and POI files")
            return

        self.usb_devices = self.get_usb_devices()
        if not self.usb_devices:
            self.output_label.config(text="No USB devices found")
            return

        for usb in self.usb_devices:
            if self.garmin_folder in os.listdir(usb):
                garmin_path = os.path.join(usb, self.garmin_folder)

                for root, dirs, files in os.walk(garmin_path):
                    for filename in files:
                        if filename.startswith('FR') or filename.startswith('Fenix'):
                            old_file = os.path.join(garmin_path, filename)
                            os.remove(old_file)
                            shutil.copy2(self.local_IMG_file_path, garmin_path)

                    for folder_name in dirs:
                        if folder_name.endswith("POI"):
                            poi_folder = os.path.join(garmin_path, folder_name)
                            shutil.rmtree(poi_folder)
                            os.mkdir(poi_folder)
                            shutil.copy2(self.local_POI_file_path, poi_folder)

                    for filename in files:
                        if "OSM" in filename and "Tunisia" in filename and filename.endswith(".img"):
                            if filename.startswith("OSM"):
                                continue
                            os.remove(filename)

                self.device_counter += 1
                self.output_text += f"Done with {usb}\n"

                self.output_text += f"Devices done: {self.device_counter}\n"
            else:
                self.output_text += f"Garmin folder not found in {usb}\n"

        self.output_text += "Process completed\n"
        self.output_label.config(text=self.output_text)

    def get_usb_devices(self):
        usb_devices = []
        for drive in range(1, 26):
            drive_letter = f"{chr(65 + drive)}:"
            if os.path.exists(drive_letter):
                drive_type = GetDriveType(drive_letter)
                if drive_type == DRIVE_REMOVABLE:
                    usb_devices.append(drive_letter)

        return usb_devices

    def run(self):
        self.root.mainloop()


app = GarminUSBUtility()
app.run()
