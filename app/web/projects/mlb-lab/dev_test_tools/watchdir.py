import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Path to the Markdown directory and markdown_output.json file
markdown_dir = "content"
json_file_path = "markdown_output.json"

# Define a handler to handle file creation and modification events
class MarkdownFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # When a new file is created, update the JSON file
        self.update_json_file()

    def on_modified(self, event):
        # When an existing file is modified, update the JSON file
        self.update_json_file()

    def update_json_file(self):
        print("Detected changes in Markdown files. Updating markdown_output.json...")
        # Run the conversion script to update the JSON file
        subprocess.run(["python3", "convertor.py"])
        print("Update completed.")


# Create an observer to monitor the Markdown directory
observer = Observer()
event_handler = MarkdownFileHandler()

observer.schedule(event_handler, markdown_dir, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
