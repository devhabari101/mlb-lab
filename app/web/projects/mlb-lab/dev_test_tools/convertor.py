import os
import markdown
import json
import re
from bleach.sanitizer import Cleaner
from bs4 import BeautifulSoup

# Directory containing Markdown files
markdown_dir = "content"

# Initialize an empty list to store JSON data for each file
json_data_list = []

# Configure cleaner to remove all tags
cleaner = Cleaner(tags=[], attributes={})

# Iterate over each file in the directory
for filename in os.listdir(markdown_dir):
    if filename.endswith(".md"):
        # Read the Markdown content from the file
        with open(os.path.join(markdown_dir, filename), "r", encoding="utf-8") as file:
            markdown_content = file.read()

        # Split metadata and content
        metadata_match = re.match(r'^---(.*?)---(.*)', markdown_content, re.DOTALL)
        if metadata_match:
            metadata, content = metadata_match.groups()

            # Parse metadata
            metadata_dict = {}
            for line in metadata.strip().split('\n'):
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    metadata_dict[key.strip()] = value.strip()

            # Parse Markdown content and remove HTML tags
            html_content = markdown.markdown(content)
            clean_content = cleaner.clean(html_content)
            soup = BeautifulSoup(clean_content, "html.parser")
            text_content = soup.get_text()

            # Remove '|' symbol from content
            text_content = text_content.replace('|', '')

            # Structure the parsed content into a JSON object
            json_data = {
                "metadata": metadata_dict,
                "content": text_content
            }

            # Append JSON data to the list
            json_data_list.append(json_data)
        else:
            print(f"Could not parse metadata in file: {filename}")

# Serialize the list of JSON data
json_output = json.dumps(json_data_list, indent=4)

# Write the JSON output to a file
with open("markdown_output.json", "w", encoding="utf-8") as output_file:
    output_file.write(json_output)

print("Conversion completed.")

