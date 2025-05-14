# 🎸 PDF & MIDI Song Generator 🎼  
A command-line Python tool to generate a **Guitar Chord Progression PDF** and a **MIDI file** from structured JSON input.

> Built with ❤️ using [`fpdf`](https://pyfpdf.github.io/fpdf2/) and [`midiutil`](https://github.com/MarkCWirt/MIDIUtil)

---

## 📦 Requirements

Install the required Python packages:

```bash
pip install fpdf midiutil
```

## 🚀 Usage
```bash
python pdf_midi_generator.py [json_file1.json json_file2.json ...] [--json_dir PATH] [--output_dir PATH]
```
### 🎯 Positional Arguments:
  ```json_file1.json json_file2.json ...``` 
  - The path(s) to one or more JSON files that contain your song data.

### ⚙️ Optional Flags:
| Flag           | Description                                                                  |
| -------------- | ---------------------------------------------------------------------------- |
| ```json_files```  | Paths to one or more JSON files containing song data. (default: **None (interactive)**) |
| `--json_dir`   | Directory to search for JSON files if none are specified (default: `./json`) |
| `--output_dir` | Directory to store the output PDF and MIDI files (default: `./output`)       |
| `--verbosity` | Set the verbosity level of the script (ERROR, INFO, DEBUG). Default: INFO      |

### 📁 JSON Format Example
```json
{
  "tempo": 120,
  "midi_duration": 4,
  "midi_volume": 80,
  "midi_chords": {
    "F": [53, 57, 60],
    "G": [55, 59, 62],
    "Am": [57, 60, 64],
    "C": [60, 64, 67]
  },
  "midi_progression": ["F", "G", "Am", "C"],
  "sections": [
    {
      "title": "Chorus Section",
      "content": "Chorus Progression: F - G - Am - C\nStrumming Pattern: D D U D U D - U\n\n..."
    }
  ]
}
```

### 🧪 Examples
✅ Generate PDF and MIDI from one file (default output directory):
- Default Verbosity (INFO):
```
python pdf_midi_generator.py ./json/my_song.json
```
✅ Generate from multiple files:
```
python pdf_midi_generator.py ./json/song1.json ./json/song2.json
```
✅ Use a custom JSON directory and let the script prompt you:
```
python pdf_midi_generator.py --json_dir ./custom_json
```
Output files will be saved in ```./custom_output```

✅ Set a different output folder:
```
python pdf_midi_generator.py --output_dir ./results
```
✅ Verbosity Options:
```
python pdf_midi_generator.py song1.json --verbosity DEBUG
python pdf_midi_generator.py song1.json --verbosity ERROR
```


✅ Interactive Mode: 
The script will prompt you to select files interactively if none are provided.
```bash
python pdf_midi_generator.py --json_dir ./json
Searching for JSON files in directory: ./json
Available JSON files:
 - song1.json
 - song2.json
Please enter the paths to the JSON files (comma-separated): song1.json, song2.json
``` 
****
### 📚 Features
- 🎵 Generates a MIDI file with chord progressions.

- 📝 Creates a printable PDF with chord diagrams and strumming patterns.

- ✨ ASCII-safe formatting ensures compatibility.

- 🔍 The script supports tab completion for file paths when entering input interactively. This feature is enabled using the readline module.

- 🧩 Designed to support modular updates and flexible structures.


----

### 🔒 Security Features
#### Path Validation
The script validates all file paths to prevent path traversal attacks.
Only files within the specified --json_dir are allowed.
Invalid paths (e.g., ```../outside_dir/file.json```) will raise an error:

### 👨‍💻 Development Notes
[ ] Update or extend the midi_chords dictionary for new chord voicings.

[ ] Add more sections to the JSON (e.g. bridge, intro) to expand your song.

[ ] Consider structuring sections dynamically in future improvements.

### 🔧 Directory Structure
```bash
project-root/
│
├── pdf_midi_generator.py
├── json/
│   └── your_song.json
└── output/
    ├── your_song_Guitar_Progression.pdf
    └── your_song_Chorus.mid
```

### 🧹 Troubleshooting
No JSON Files Found
- Ensure the --json_dir directory exists and contains .json files.
- Example:
  ```  mkdir -p ./json```
Invalid JSON Format
Ensure the input JSON file follows the required structure.
Use a JSON validator to check for syntax errors.
Debugging
Run the script with --verbosity DEBUG to see detailed logs