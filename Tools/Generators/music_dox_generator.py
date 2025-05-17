# Extended script: Generate PDF, MIDI, ABC notation* , and a MusicXML file for any song
# Required Libraries: fpdf, midiutil, music21
# Install with: pip install fpdf midiutil music21


import json
import argparse
import readline
import os
import datetime
import logging
from fpdf import FPDF
from midiutil import MIDIFile
from music21 import stream, chord, note, metadata, meter, tempo, key, duration

# Configure logging
def configure_logging(verbosity):
    log_levels = {
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG
    }
    logging.basicConfig(
        level=log_levels.get(verbosity, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
# File validation
def validate_file_path(file_path, base_dir):
    abs_base_dir = os.path.abspath(base_dir)
    abs_file_path = os.path.abspath(file_path)
    if not abs_file_path.startswith(abs_base_dir):
        raise ValueError(f"Invalid file path: {file_path}. Path traversal detected.")
    return abs_file_path

# Tab completion setup
def enable_file_completion(search_dir="./json"):
    def complete_path(text, state):
        line = readline.get_line_buffer().split()
        dirname, partial = os.path.split(text)
        if not dirname:
            dirname = search_dir
        matches = [f for f in os.listdir(dirname) if f.startswith(partial) and f.endswith(".json")]
        matches = [os.path.join(dirname, m) for m in matches]
        try:
            return matches[state]
        except IndexError:
            return None
    readline.set_completer(complete_path)
    readline.parse_and_bind("tab: complete")

# Text cleaning
def clean_text_ascii(text):
    replacements = {"–": "-", "—": "-", "’": "'", "“": '"', "”": '"', "‘": "'", "↓": "D", "↑": "U", "•": "*", "…": "..."}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode('ascii', errors='ignore').decode()

# PDF Class
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Guitar Progression & Strumming Guide', 0, 1, 'C')
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    def chapter_body(self, body):
        self.set_font('Courier', '', 10)
        self.multi_cell(0, 5, clean_text_ascii(body))
        self.ln()

def generate_pdf(song_data, output_path):
    try:
        content = ""
        sections = song_data.get("sections") or []
        if sections:
            for section in sections:
                if section is None:
                    continue
                content += f"Section: {section.get('title', '')}\n"
                content += f"Progression: {section.get('progression') or []}\n"
                content += f"Lyrics: {section.get('lyrics') or []}\n"
                content += f"Strumming Pattern: {section.get('strumming_pattern') or ''}\n\n"
        else:
            content = str(song_data)
        pdf = PDF()
        pdf.add_page()
        pdf.chapter_body(content)
        pdf.output(output_path)
        logging.info(f"PDF saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to generate PDF: {e}")

def generate_midi(song_data, output_path):
    try:
        midi_progression = []
        sections = song_data.get("sections") or []
        midi_chords = song_data.get("midi_chords") or {}
        if sections and midi_chords:
            for section in sections:
                if section is None:
                    continue
                for chord_name in section.get("progression") or []:
                    midi_progression.append(midi_chords.get(chord_name, []))
        else:
            midi_progression = song_data.get("midi_progression") or []
        mf = MIDIFile(1)
        track = 0
        time = 0
        mf.addTrackName(track, time, "Chords")
        mf.addTempo(track, time, song_data.get("tempo", 120))
        duration_val = song_data.get("midi_duration", 1)
        volume = song_data.get("midi_volume", 100)
        for chord_notes in midi_progression:
            if chord_notes is None:
                continue
            for note_val in chord_notes:
                mf.addNote(track, 0, note_val, time, duration_val, volume)
            time += duration_val
        with open(output_path, "wb") as f:
            mf.writeFile(f)
        logging.info(f"MIDI saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to generate MIDI: {e}")

def generate_musicxml(song_data, output_path):
    try:
        chord_notes = song_data.get("midi_chords") or {}
        score = stream.Score()
        score.insert(0, metadata.Metadata())
        score.metadata.title = song_data.get("title", "Untitled")
        score.append(tempo.MetronomeMark(number=song_data.get("tempo", 120)))
        score.append(meter.TimeSignature('4/4'))
        score.append(key.KeySignature(0))
        part = stream.Part()
        measure_num = 1
        sections = song_data.get("sections") or []
        for section in sections:
            if section is None:
                continue
            lyrics_lines = section.get("lyrics") or []
            progression = section.get("progression") or []
            lyric_idx = 0
            for chord_name in progression:
                if chord_name in chord_notes:
                    chord_obj = chord.Chord(chord_notes[chord_name])
                    chord_obj.quarterLength = 4
                    if lyric_idx < len(lyrics_lines):
                        chord_obj.addLyric(lyrics_lines[lyric_idx])
                        lyric_idx += 1
                    measure = stream.Measure(number=measure_num)
                    measure.append(chord_obj)
                    part.append(measure)
                    measure_num += 1
        score.append(part)
        score.write("musicxml", fp=output_path)
        logging.info(f"MusicXML saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to generate MusicXML: {e}")

def generate_abc(song_data, output_path):
    try:
        abc_notation = song_data.get("abc_notation") or {}
        reference_number = abc_notation.get("reference_number", 1)
        title = abc_notation.get("title", "Untitled")
        composer = abc_notation.get("composer", "Unknown")
        meter_val = abc_notation.get("meter", "4/4")
        unit_note_length = abc_notation.get("unit_note_length", "1/8")
        tempo_val = abc_notation.get("tempo", "1/4=120")
        key_val = abc_notation.get("key", "C")
        abc_lines = [
            f"X:{reference_number}",
            f"T:{title}",
            f"C:{composer}",
            f"M:{meter_val}",
            f"L:{unit_note_length}",
            f"Q:{tempo_val}",
            f"K:{key_val}",
        ]
        for section in abc_notation.get("sections") or []:
            if section is None:
                continue
            abc_lines.append(f"%% {section.get('title', '')}")
            chords_line = " ".join([f"[{ch}]" for ch in section.get("chords") or []])
            abc_lines.append(chords_line)
            lyrics_lines = " | ".join(section.get("lyrics") or [])
            abc_lines.append(f"w: {lyrics_lines}")
        with open(output_path, "w") as f:
            f.write("\n".join(abc_lines))
        logging.info(f"ABC notation saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to generate ABC notation: {e}")

def load_song_data(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        raise

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        logging.info(f"Directory '{directory}' not found. Creating it...")
        os.makedirs(directory)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PDF, MIDI, and ABC for songs from JSON.")
    parser.add_argument("json_files", nargs="*", help="Paths to JSON files.")
    parser.add_argument("--json_dir", default="./json", help="Directory to search for JSON files.")
    parser.add_argument("--output_dir", default="./output", help="Directory to save output.")
    # TODO: change add -v -vv -vvv options to verbosity
    parser.add_argument("--verbosity", choices=["ERROR", "INFO", "DEBUG"], default="INFO")
    args = parser.parse_args()

    configure_logging(args.verbosity)
    ensure_directory_exists(args.json_dir)
    ensure_directory_exists(args.output_dir)
    enable_file_completion(args.json_dir)

    logging.debug(f"JSON directory: {args.json_dir}")

    if not args.json_files:
        logging.info(f"Looking in {args.json_dir}")
        json_files = [f for f in os.listdir(args.json_dir) if f.endswith(".json")]
        if not json_files:
            logging.error("No JSON files found.")
            exit(1)
        print("Available JSON files:")
        for file in json_files:
            print(f" - {file}")
        print("Options:")
        print("  [1] Enter file names (comma-separated)")
        print("  [2] Process ALL files in the directory")
        choice = input("Choose an option [1/2]: ").strip()
        if choice == '2':
            confirm = input(f"Are you sure you want to process ALL {len(json_files)} files in '{args.json_dir}'? (y/n): ").strip().lower()
            if confirm == 'y':
                args.json_files = [os.path.join(args.json_dir, f) for f in json_files]
            else:
                print("Aborted.")
                exit(0)
        else:
            selected = input("Enter JSON files (comma-separated): ")
            args.json_files = [
                os.path.abspath(f.strip()) if os.path.isabs(f.strip()) else os.path.normpath(os.path.join(args.json_dir, f.strip()))
                for f in selected.split(",")
            ]

    # Process each JSON file
    for json_file in args.json_files:
        try:
            # Ensure both paths are absolute before comparison
            abs_json_file = os.path.abspath(json_file)
            abs_base_dir = os.path.abspath(args.json_dir)
            base_dir = os.path.commonpath([abs_json_file, abs_base_dir])

            json_file = validate_file_path(abs_json_file, base_dir)
            logging.info(f"Processing file: {json_file}")

            # Load and process the song data
            song_data = load_song_data(json_file)

            # Create a unique output folder for the song
            base = os.path.splitext(os.path.basename(json_file))[0]
            date = datetime.datetime.now().strftime("%Y%m%d")
            song_output_dir = os.path.join(args.output_dir, f"{base}_{date}")

            # Check if the directory already exists
            if os.path.exists(song_output_dir):
                timestamp = datetime.datetime.now().strftime("%H%M%S")
                user_input = input(f"Directory '{song_output_dir}' already exists. Overwrite? (y/n): ")
                if user_input.lower() != 'y':
                    song_output_dir = os.path.join(args.output_dir, f"{base}_{date}_{timestamp}")

            ensure_directory_exists(song_output_dir)

            # Generate and save files in the song-specific folder
            pdf_output = validate_file_path(os.path.join(song_output_dir, f"{base}_Guitar_Progression.pdf"), song_output_dir)
            midi_output = validate_file_path(os.path.join(song_output_dir, f"{base}_Chorus.mid"), song_output_dir)
            abc_output = validate_file_path(os.path.join(song_output_dir, f"{base}.abc"), song_output_dir)
            xml_output = validate_file_path(os.path.join(song_output_dir, f"{base}_Full_Score.musicxml"), song_output_dir)

            generate_pdf(song_data, output_path=pdf_output)
            generate_midi(song_data, output_path=midi_output)
            generate_abc(song_data, output_path=abc_output)
            generate_musicxml(song_data, output_path=xml_output)

            logging.info(f"Files for '{base}' saved in {song_output_dir}")
        except Exception as e:
            logging.error(f"Error processing {json_file}: {e}")
