import threading
import time
import os
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification


DANGEROUS_EXTENSIONS = {
    'action', 'apk', 'app', 'bat', 'bin', 'cab', 'cmd', 'com', 'command', 'cpl', 'csh', 'exe',
    'gadget', 'inf', 'ins', 'inx', 'ipa', 'isu', 'job', 'jse', 'ksh', 'lnk', 'msc', 'msi', 'msp',
    'mst', 'out', 'pif', 'prg', 'reg', 'rgs', 'run', 'scr', 'sh', 'u3p', 'vb', 'vbe', 'vbs', 'workflow', 'ws', 'wsh'
}

class ExecutableEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def on_created(self, event):
        if event.is_directory:
            return
        file_name, file_extension = os.path.splitext(event.src_path)
        file_extension = file_extension[1:].lower()
    
        if file_extension in DANGEROUS_EXTENSIONS:
            print(f"Detected dangerous file: {event.src_path}")
            notification_title = 'Potentially Dangerous File Detected'
            notification_message = f'File with dangerous extension detected: {event.src_path}'
            
            notification.notify(
                title=notification_title,
                message=notification_message,
                app_name='Exec Watchdog',
                timeout=10
            )
            
            
            self.insert_notification(notification_title, notification_message, event.src_path)

    def insert_notification(self, title, message, file_path):
        with self.lock:
            with sqlite3.connect('/home/svrt/Documents/Scripts/notifications.db') as conn:
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO notifications (title, message, file_path, timestamp) VALUES (?, ?, ?, ?)",
                              (title, message, file_path, time.strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                    print("Notification inserted successfully.")
                except sqlite3.Error as e:
                    print(f"Database error: {e}")

    def stop(self):
        pass

def main():
    path = os.path.expanduser('~')
    event_handler = ExecutableEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
 
    with sqlite3.connect('/home/svrt/Documents/Scripts/notifications.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS notifications
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, message TEXT, file_path TEXT, timestamp DATETIME)''')
        conn.commit()
        print("Notifications table created or already exists.")

    main()
