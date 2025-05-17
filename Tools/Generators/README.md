# 🎸 PDF & MID & ABC Notation Generator 🎼  
**A** command-line Python tool to generate a **Guitar Chord Progression PDF**, **MIDI file**, **ABC notation**, and **MusicXML** from structured JSON input.

> Built with ❤️ using [`fpdf`](https://pyfpdf.github.io/fpdf2/), [`midiutil`](https://github.com/MarkCWirt/MIDIUtil), and MusicXML standards.

---

## 📦 Requirements

Install the required Python packages:

```bash
pip install fpdf midiutil
```

## 🚀 Usage
```bash
python music_dox_generator.py [json_file1.json json_file2.json ...] [--json_dir PATH] [--output_dir PATH]
```

### 🎯 Interactive & Batch Processing
- If you do **not** specify any JSON files, the script will prompt you to:
  1. Enter file names (comma-separated), **or**
  2. Process **ALL** JSON files in the selected directory (with confirmation).

### ⚙️ Optional Flags:
| Flag           | Description                                                                  |
| -------------- | ---------------------------------------------------------------------------- |
| ```json_files```  | Paths to one or more JSON files containing song data. (default: **None (interactive)**) |
| `--json_dir`   | Directory to search for JSON files if none are specified (default: `./json`) |
| `--output_dir` | Directory to store the output files (default: `./output`)                    |
| `--verbosity`  | Set the verbosity level of the script (ERROR, INFO, DEBUG). Default: INFO    |

### 📁 JSON Format Example
```json
{
  "title": "Build or Destroy",
  "composer": "Stolen Thunda",
  "tempo": 120,
  "midi_duration": 4,
  "midi_volume": 80,
  "midi_chords": {
    "D": [62, 66, 69],
    "C": [60, 64, 67],
    "Bb": [58, 62, 65],
    "A": [57, 61, 64]
  },
  "midi_progression": ["D", "C", "Bb", "A", "D", "C", "Bb", "A", "D"],
  "sections": [
    {
      "title": "Verse 1: Relationship",
      "content": "...",
      "progression": ["D", "C", "Bb", "A", "D", "C", "Bb", "A"],
      "lyrics": ["You always said we’d work it out,", ...],
      "strumming_pattern": ["↓(rake) ↓ ↑ ↓(rake) ↑ ↓ ↑"]
    }
  ],
  "abc_notation": {
    "reference_number": 1,
    "title": "Build or Destroy",
    "composer": "Stolen Thunda",
    "meter": "4/4",
    "unit_note_length": "1/8",
    "tempo": "1/4=120",
    "key": "C",
    "sections": [
      {
        "title": "Verse 1: Relationship",
        "chords": ["D", "C", "Bb", "A", "D", "C", "Bb", "A"],
        "lyrics": ["You always said we’d work it out,", ...]
      }
    ]
  }
}
```

### 🧪 Examples
✅ Generate PDF, MIDI, ABC notation, and MusicXML from one file (default output directory):
- Default Verbosity (INFO):
```bash
python music_dox_generator.py ./json/my_song.json
```

✅ Generate from multiple files:
```bash
python music_dox_generator.py ./json/song1.json ./json/song2.json
```

✅ Use a custom JSON directory and let the script prompt you:
```bash
python music_dox_generator.py --json_dir ./custom_json
```

✅ Set a different output folder:
```bash
python music_dox_generator.py --output_dir ./results
```

✅ Verbosity Options:
```bash
python music_dox_generator.py song1.json --verbosity DEBUG
python music_dox_generator.py song1.json --verbosity ERROR
```

✅ Interactive Mode: 
The script will prompt you to select files interactively if none are provided.
```bash
python music_dox_generator.py --json_dir ./json
Searching for JSON files in directory: ./json
Available JSON files:
 - song1.json
 - song2.json
Please enter the paths to the JSON files (comma-separated): song1.json, song2.json
``` 

---

### 📂 Output Directory Structure
For each song, the script creates a unique folder named `song_{datetime}` in the `./output` directory. The `{datetime}` is a timestamp in the format `YYYYMMDD_HHMMSS`.

Example:
```bash
output/
├── song_20250514_154500/
│   ├── my_song_Guitar_Progression.pdf
│   ├── my_song_Chorus.mid
│   ├── my_song.abc
│   └── my_song.musicxml
├── song_20250514_154600/
│   ├── another_song_Guitar_Progression.pdf
│   ├── another_song_Chorus.mid
│   ├── another_song.abc
│   └── another_song.musicxml
```

---

### 📚 Features
- 🎵 Generates a MIDI file with chord progressions.
- 📝 Creates a printable PDF with chord diagrams and strumming patterns.
- 🎼 Generates ABC notation for the song.
- 🎶 Generates MusicXML for full score.
- ✨ ASCII-safe formatting ensures compatibility.
- 🔍 The script supports tab completion for file paths when entering input interactively. This feature is enabled using the `readline` module.
- 🧩 Designed to support modular updates and flexible structures.

---

### 🔒 Security Features
#### Path Validation
The script validates all file paths to prevent path traversal attacks.
Only files within the specified `--json_dir` are allowed.
Invalid paths (e.g., `../outside_dir/file.json`) will raise an error.

---

### 🧹 Automated JSON Fixing
A script (`tests/auto_fix_json_fields.py`) is provided to automatically populate missing fields in your JSON files (e.g., set `composer` to `Stolen Thunda`, ensure lists/dicts are not null). This helps ensure all files pass validation and are compatible with the generator.

---

### 🧹 Troubleshooting
#### No JSON Files Found
- Ensure the `--json_dir` directory exists and contains `.json` files.
- Example:
  ```bash
  mkdir -p ./json
  ```

#### Invalid JSON Format
- Ensure the input JSON file follows the required structure.
- Use a JSON validator to check for syntax errors.

#### Debugging
- Run the script with `--verbosity DEBUG` to see detailed logs:
  ```bash
  python music_dox_generator.py song1.json --verbosity DEBUG
  ```

---

### 👨‍💻 Development Notes
- [ ] Update or extend the `midi_chords` dictionary for new chord voicings.
- [ ] Add more sections to the JSON (e.g., bridge, intro) to expand your song.
- [ ] Consider structuring sections dynamically in future improvements.