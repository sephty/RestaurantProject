import json

def load_json(filename):
    """Load data from a JSON file, handling errors gracefully."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_json(filename, data):
    """Save data to a JSON file with indentation."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)