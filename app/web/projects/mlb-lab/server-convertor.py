import os
import markdown
import json
import re
from flask import Flask, render_template, send_file, request, redirect, url_for
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# Directory containing Markdown files
markdown_dir = "content"
json_output_file = "markdown_output.json"

# Function to save form data to Markdown file
def save_to_markdown(data):
    # Create a filename based on current timestamp or unique identifier
    filename = os.path.join(markdown_dir, f"{data['title']}.md")
    # Write form data to Markdown file
    with open(filename, "w") as file:
        file.write(f"---\n")
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
        file.write(f"---\n\n{data['content']}")
        
# Function to convert Markdown to HTML and update JSON file
def convert_markdown_to_json():
    json_data_list = []

    for filename in os.listdir(markdown_dir):
        if filename.endswith(".md"):
            with open(os.path.join(markdown_dir, filename), "r", encoding="utf-8") as file:
                markdown_content = file.read()

            metadata_match = re.match(r'^---(.*?)---(.*)', markdown_content, re.DOTALL)
            if metadata_match:
                metadata, content = metadata_match.groups()
                metadata_dict = {}
                for line in metadata.strip().split('\n'):
                    key_value = line.split(':', 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        metadata_dict[key.strip()] = value.strip()

                html_content = markdown.markdown(content)
                json_data = {
                    "metadata": metadata_dict,
                    "content": html_content
                }
                json_data_list.append(json_data)
            else:
                print(f"Could not parse metadata in file: {filename}")

    with open(json_output_file, "w", encoding="utf-8") as output_file:
        json.dump(json_data_list, output_file, indent=4)

# Define a custom event handler to monitor file system changes
class MarkdownFileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.event_type in ('created', 'modified'):
            if event.src_path.endswith(".md"):
                convert_markdown_to_json()

# Flask route to serve the JSON data
#@app.route("/data", methods=["GET"])
#def get_data():
#    with open(json_output_file, "r", encoding="utf-8") as json_file:
#        data = json.load(json_file)
#    return json.dumps(data)

# Flask route to serve the HTML content
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
    
# Route to render the form
@app.route("/admin", methods=["GET"])
def form_admin():
    return render_template("form.html")

# Route to handle form submission
@app.route("/submit", methods=["POST"])
def submit_form():
    form_data = {
        "title": request.form.get("title"),
        "category": request.form.get("category"),
        "content": request.form.get("content")
    }
    save_to_markdown(form_data)
    return redirect(url_for("index"))   

@app.route('/markdown_output.json')
def get_markdown_output():
    return send_file('markdown_output.json')

if __name__ == "__main__":
    # Initial conversion from Markdown to JSON
    convert_markdown_to_json()

    # Start the watchdog observer to monitor file changes
    event_handler = MarkdownFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=markdown_dir, recursive=True)
    observer.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=7000)
    # Cleanup
    observer.stop()
    observer.join()
