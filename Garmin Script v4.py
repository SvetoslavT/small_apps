import os
import shutil

garmin_folder = "Garmin"
local_IMG_file_path = "C:/Users/Svetoslav/Desktop/LEG 1.img"
local_POI_file_path = "C:/Users/Svetoslav/Desktop/dsadasd.gpi"
device_counter = 0
usb_devices = ["D:\\", "F:\\"]
while True:
    for usb in usb_devices:
        if garmin_folder in os.listdir(usb):
            garmin_path = os.path.join(usb, garmin_folder)

            for root, dirs, files in os.walk(garmin_path):
                for filename in files:
                    if filename.startswith('FR'):
                        old_file = os.path.join(garmin_path, filename)
                        os.remove(old_file)
                        shutil.copy2(local_IMG_file_path, garmin_path)

                for folder_name in dirs:
                    if folder_name.endswith("POI"):
                        poi_folder = os.path.join(garmin_path, folder_name)
                        shutil.rmtree(poi_folder)
                        os.mkdir(poi_folder)
                        shutil.copy2(local_POI_file_path, poi_folder)


            print("Done with " + usb)
            device_counter += 1
    print(f"Devices done: {device_counter}")
    input("Press ENTER after connecting the new devices. :)")

