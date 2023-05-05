import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from cloudflare_kv import Namespace

kv_namespace = Namespace(
    account_id=os.environ["CF_ACCOUNT_ID"],
    namespace_id=os.environ["CF_NAMESPACE_ID"],
    api_key=os.environ["CF_API_KEY"],
)


def load_files():
    # Set the folder path
    folder_path = Path("output")

    # Initialize an empty list to store the contents of all JSON files
    combined_data = []

    # Iterate through all JSON files in the folder
    for json_file in folder_path.glob("*.json"):
        # Read the contents of the file as text
        json_text = json_file.read_text()

        # Load the JSON data from the text
        json_data = json.loads(json_text)

        # Append the JSON data to the combined_data list
        combined_data.extend(json_data)
    return combined_data


def group_by_date(items):
    # Initialize a defaultdict with list as the default factory
    grouped_data = defaultdict(list)

    # Iterate through the list of dictionaries
    for item in items:
        # Parse the datetime value from the "time_start" key
        dt = datetime.fromisoformat(item["time_start"])

        # Extract the date part from the datetime object
        date_key = dt.date().isoformat()

        # Append the item to the corresponding list in the grouped_data dictionary
        grouped_data[date_key].append(item)

    return [{"date": date, "items": items} for date, items in grouped_data.items()]


if __name__ == "__main__":
    items = load_files()
    items = sorted(items, key=lambda x: datetime.fromisoformat(x["time_start"]))
    grouped_classes = group_by_date(items)
    json_data = json.dumps(grouped_classes)
    kv_namespace.write({"data": json_data})
