import os
import json

# Path to the validation results and JSON directory
VALIDATION_RESULTS_PATH = os.path.join(os.path.dirname(__file__), 'json_validation_results.json')
JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Generators/json'))

# Load validation results
def load_validation_results():
    with open(VALIDATION_RESULTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def guess_stub_value(field_path, value):
    # Use the field name to guess if it should be a list, dict, or None
    # If the stub is None, but the field name suggests a list or dict, use that
    list_like = ["progression", "lyrics", "strumming_pattern", "sections", "chords"]
    dict_like = ["abc_notation", "midi_chords"]
    # Special case for composer
    if field_path.endswith("composer"):
        return "Stolen Thunda"
    # If the stub is already a list or dict, keep it
    if isinstance(value, (list, dict)):
        return value
    # Guess by field name
    for part in reversed(field_path.split('.')):
        if any(part.startswith(name) for name in list_like):
            return []
        if any(part.startswith(name) for name in dict_like):
            return {}
    return None

def set_nested_field(obj, field_path, value):
    """
    Set a nested field in a dict/list structure given a dotted path with optional [index] for lists.
    """
    import re
    parts = re.split(r'\.(?![^\[]*\])', field_path)  # split on . not inside []
    curr = obj
    for i, part in enumerate(parts):
        m = re.match(r'([\w_]+)(\[(\d+)\])?', part)
        if not m:
            raise ValueError(f"Invalid field path part: {part}")
        key = m.group(1)
        idx = m.group(3)
        # If last part, set value
        if i == len(parts) - 1:
            if idx is not None:
                if key not in curr or not isinstance(curr[key], list):
                    curr[key] = []
                idx = int(idx)
                # Extend list if needed
                while len(curr[key]) <= idx:
                    curr[key].append(None)
                curr[key][idx] = value
            else:
                curr[key] = value
        else:
            # Not last part, descend
            if key not in curr or (idx is not None and not isinstance(curr[key], list)):
                curr[key] = [] if idx is not None else {}
            if idx is not None:
                idx = int(idx)
                while len(curr[key]) <= idx:
                    curr[key].append({})
                curr = curr[key][idx]
            else:
                curr = curr[key]

def update_json_files():
    validation = load_validation_results()
    for filename, missing_fields in validation.items():
        json_path = os.path.join(JSON_DIR, filename)
        if not os.path.exists(json_path):
            print(f"File not found: {json_path}")
            continue
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
                continue
        changed = False
        for field_path, value in missing_fields.items():
            # Only set if missing or None
            try:
                # Traverse to check if already set
                import re
                parts = re.split(r'\.(?![^\[]*\])', field_path)
                curr = data
                exists = True
                for part in parts:
                    m = re.match(r'([\w_]+)(\[(\d+)\])?', part)
                    key = m.group(1)
                    idx = m.group(3)
                    if idx is not None:
                        idx = int(idx)
                        if key not in curr or not isinstance(curr[key], list) or len(curr[key]) <= idx:
                            exists = False
                            break
                        curr = curr[key][idx]
                    else:
                        if key not in curr:
                            exists = False
                            break
                        curr = curr[key]
                if not exists or curr is None:
                    stub = guess_stub_value(field_path, value)
                    set_nested_field(data, field_path, stub)
                    changed = True
            except Exception as e:
                print(f"Error setting {field_path} in {filename}: {e}")
        if changed:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated: {filename}")
        else:
            print(f"No changes needed: {filename}")

if __name__ == "__main__":
    update_json_files()
