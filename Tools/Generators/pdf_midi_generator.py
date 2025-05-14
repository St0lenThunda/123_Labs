# Consolidated Python script to generate a PDF chord sheet and a MIDI file for any song
# Required Libraries: fpdf, midiutil
# Install with: pip install fpdf midiutil

import json
import argparse
import readline  # For enabling tab completion
import os        # For file path handling
from fpdf import FPDF  # PDF generation library
from midiutil import MIDIFile  # MIDI generation library
import logging  # For logging

# Configure logging
def configure_logging(verbosity):
    """
    Configures the logging level based on the verbosity argument.
    """
    log_levels = {
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG
    }
    logging.basicConfig(
        level=log_levels.get(verbosity, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Validate file paths to prevent path traversal attacks
def validate_file_path(file_path, base_dir):
    """
    Validates that the given file path is within the allowed base directory.
    Prevents path traversal attacks by resolving the absolute path and checking its prefix.
    """
    abs_base_dir = os.path.abspath(base_dir)
    abs_file_path = os.path.abspath(file_path)

    if not abs_file_path.startswith(abs_base_dir):
        raise ValueError(f"Invalid file path: {file_path}. Path traversal detected.")
    return abs_file_path

# Enable tab completion for file paths
def enable_file_completion(search_dir="./json"):
    """
    Enables tab completion for file paths in the specified directory.
    """
    def complete_path(text, state):
        """
        Completes file paths based on the current input and state.
        """
        line = readline.get_line_buffer().split()
        if not line:
            return [text][state]
        else:
            dirname, partial = os.path.split(text)
            if not dirname:
                dirname = search_dir  # Default to the search directory if no directory is specified
            matches = [f for f in os.listdir(dirname) if f.startswith(partial) and f.endswith(".json")]
            matches = [os.path.join(dirname, m) for m in matches]
            try:
                return matches[state]
            except IndexError:
                return None

    readline.set_completer(complete_path)
    readline.parse_and_bind("tab: complete")

# Clean text for PDF (ASCII-friendly)
def clean_text_ascii(text):
    replacements = {
        "–": "-",  # En dash
        "—": "-",  # Em dash
        "’": "'",  # Curly apostrophe
        "“": '"',  # Left double quote
        "”": '"',  # Right double quote
        "‘": "'",  # Left single quote
        "↓": "D",  # Strumming
        "↑": "U",
        "•": "*",  # Bullet
        "…": "...",  # Ellipsis
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode('ascii', errors='ignore').decode()


# Create PDF class for chord sheet
class PDF(FPDF):
    """
    Custom PDF class for generating chord sheets.
    Inherits from the FPDF library and adds custom headers and formatting.
    """
    def header(self):
        """
        Adds a header to each page of the PDF.
        """
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Guitar Progression & Strumming Guide', 0, 1, 'C')

    def chapter_title(self, title):
        """
        Adds a chapter title to the PDF.
        """
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        """
        Adds the body content of a chapter to the PDF.
        """
        self.set_font('Courier', '', 10)
        self.multi_cell(0, 5, clean_text_ascii(body))
        self.ln()

# Generate PDF
def generate_pdf(song_data, output_path):
    """
    Generates a PDF file from the song data.
    """
    try:
        pdf = PDF()
        pdf.add_page()
        for section in song_data["sections"]:
            pdf.chapter_title(section["title"])
            pdf.chapter_body(section["content"])
        pdf.output(output_path)
        logging.info(f"PDF saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to generate PDF: {e}")

# Generate MIDI
def generate_midi(song_data, output_path):
    """
    Generates a MIDI file from the song data.
    """
    try:
        mf = MIDIFile(1)  # Create a single-track MIDI file
        track = 0
        time = 0
        mf.addTrackName(track, time, "Chords")
        mf.addTempo(track, time, song_data["tempo"])

        chords = song_data["midi_chords"]
        duration = song_data["midi_duration"]
        volume = song_data["midi_volume"]

        for chord in song_data["midi_progression"]:
            for note in chords[chord]:
                mf.addNote(track, 0, note, time, duration, volume)
            time += duration

        with open(output_path, "wb") as f:
            mf.writeFile(f)
        logging.info(f"MIDI saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to generate MIDI: {e}")

# Load song data from JSON file
def load_song_data(file_path):
    """
    Loads song data from a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        raise

# Ensure directory exists
def ensure_directory_exists(directory):
    """
    Ensures the specified directory exists. Creates it if it doesn't exist.
    """
    if not os.path.exists(directory):
        logging.info(f"Directory '{directory}' not found. Creating it...")
        os.makedirs(directory)

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a PDF chord sheet and a MIDI file for a song.")
    parser.add_argument("json_files", nargs="*", help="Paths to the JSON files containing song data.")
    parser.add_argument("--json_dir", default="./json", help="Directory to search for JSON files (default: ./json).")
    parser.add_argument("--output_dir", default="./output", help="Directory to save output files (default: ./output).")
    parser.add_argument("--verbosity", choices=["ERROR", "INFO", "DEBUG"], default="INFO",
                        help="Set the verbosity level of the script (default: INFO).")
    args = parser.parse_args()

    # Configure logging based on verbosity level
    configure_logging(args.verbosity)

    # Ensure the JSON and output directories exist
    ensure_directory_exists(args.json_dir)
    ensure_directory_exists(args.output_dir)

    # Enable tab completion for the specified directory
    enable_file_completion(search_dir=args.json_dir)

    # If no JSON files are provided, prompt the user to select from the directory
    if not args.json_files:
        logging.info(f"Searching for JSON files in directory: {args.json_dir}")
        json_files = [f for f in os.listdir(args.json_dir) if f.endswith(".json")]
        if json_files:
            logging.info("Available JSON files:")
            for file in json_files:
                logging.info(f" - {file}")
            selected_files = input("Please enter the paths to the JSON files (comma-separated): ")
            # Resolve and validate each file path
            args.json_files = [
                validate_file_path(
                    os.path.abspath(os.path.join(args.json_dir, os.path.relpath(f.strip(), args.json_dir))) if not os.path.isabs(f.strip()) else os.path.abspath(f.strip()),
                    args.json_dir
                )
                for f in selected_files.split(",")
            ]
        else:
            logging.error("No JSON files found in the specified directory.")
            exit(1)

    logging.debug(f"Resolved file paths after validation: {args.json_files}")

    # Process each JSON file
    for json_file in args.json_files:
        try:
            json_file = validate_file_path(json_file, args.json_dir)
            logging.info(f"Processing file: {json_file}")
            song_data = load_song_data(json_file)
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            pdf_output = validate_file_path(os.path.join(args.output_dir, f"{base_name}_Guitar_Progression.pdf"), args.output_dir)
            midi_output = validate_file_path(os.path.join(args.output_dir, f"{base_name}_Chorus.mid"), args.output_dir)
            generate_pdf(song_data, output_path=pdf_output)
            generate_midi(song_data, output_path=midi_output)
        except Exception as e:
            logging.error(f"Failed to process file {json_file}: {e}")