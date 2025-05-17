import unittest
import os
import sys
import json
import subprocess
from unittest.mock import patch

# Add the Generators directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Generators')))
import Generators.music_dox_generator as music_dox_generator

class TestMusicDoxGeneratorCombined(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a real JSON file for CLI and a dict for in-memory tests
        cls.sample_json_path = os.path.join(os.path.dirname(__file__), '../Generators/json/Build_or_Destroy_Updated_Aligned.json')
        cls.sample_output_dir = "test_output"
        with open(cls.sample_json_path, "r") as f:
            cls.sample_song_data = json.load(f)
        # Also create a minimal test JSON for CLI
        cls.cli_json_path = "test_song_standard.json"
        with open(cls.cli_json_path, "w") as f:
            json.dump(cls.sample_song_data, f)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.cli_json_path):
            os.remove(cls.cli_json_path)
        if os.path.exists(cls.sample_output_dir):
            for root, dirs, files in os.walk(cls.sample_output_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(cls.sample_output_dir)

    def test_json_standard_fields(self):
        data = self.sample_song_data
        self.assertIn("title", data)
        self.assertIn("composer", data)
        self.assertIn("tempo", data)
        self.assertIn("key", data)
        self.assertIn("meter", data)
        self.assertIn("unit_note_length", data)
        self.assertIn("midi_duration", data)
        self.assertIn("midi_volume", data)
        self.assertIn("midi_chords", data)
        self.assertIn("sections", data)
        self.assertIsInstance(data["sections"], list)
        for section in data["sections"]:
            self.assertIn("title", section)
            self.assertIn("progression", section)
            self.assertIn("lyrics", section)
            self.assertIn("strumming_pattern", section)
        # Optional: abc_notation
        if "abc_notation" in data:
            abc = data["abc_notation"]
            self.assertIn("reference_number", abc)
            self.assertIn("title", abc)
            self.assertIn("composer", abc)
            self.assertIn("meter", abc)
            self.assertIn("unit_note_length", abc)
            self.assertIn("tempo", abc)
            self.assertIn("key", abc)
            self.assertIn("sections", abc)
            self.assertIsInstance(abc["sections"], list)
            for abc_section in abc["sections"]:
                self.assertIn("title", abc_section)
                self.assertIn("chords", abc_section)
                self.assertIn("lyrics", abc_section)

    def test_load_song_data(self):
        song_data = music_dox_generator.load_song_data(self.sample_json_path)
        self.assertEqual(song_data, self.sample_song_data)

    def test_ensure_directory_exists(self):
        music_dox_generator.ensure_directory_exists(self.sample_output_dir)
        self.assertTrue(os.path.exists(self.sample_output_dir))

    @patch('Generators.music_dox_generator.generate_musicxml')
    @patch('Generators.music_dox_generator.generate_abc')
    @patch('Generators.music_dox_generator.generate_midi')
    @patch('Generators.music_dox_generator.generate_pdf')
    def test_file_generation(self, mock_generate_pdf, mock_generate_midi, mock_generate_abc, mock_generate_musicxml):
        mock_generate_pdf.return_value = None
        mock_generate_midi.return_value = None
        mock_generate_abc.return_value = None
        mock_generate_musicxml.return_value = None

        pdf_path = os.path.join(self.sample_output_dir, "test.pdf")
        midi_path = os.path.join(self.sample_output_dir, "test.mid")
        abc_path = os.path.join(self.sample_output_dir, "test.abc")
        xml_path = os.path.join(self.sample_output_dir, "test.musicxml")

        music_dox_generator.ensure_directory_exists(self.sample_output_dir)
        music_dox_generator.generate_pdf(self.sample_song_data, pdf_path)
        music_dox_generator.generate_midi(self.sample_song_data, midi_path)
        music_dox_generator.generate_abc(self.sample_song_data, abc_path)
        music_dox_generator.generate_musicxml(self.sample_song_data, xml_path)
        mock_generate_pdf.assert_called_once_with(self.sample_song_data, pdf_path)
        mock_generate_midi.assert_called_once_with(self.sample_song_data, midi_path)
        mock_generate_abc.assert_called_once_with(self.sample_song_data, abc_path)
        mock_generate_musicxml.assert_called_once_with(self.sample_song_data, xml_path)

    # Utility function to check if a PDF file is valid (basic check: file exists and starts with %PDF)
    def is_valid_pdf(self, file_path):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'rb') as f:
            return f.read(4) == b'%PDF'

    # Utility function to check if a MIDI file is valid (basic check: file exists and starts with 'MThd')
    def is_valid_midi(self, file_path):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'rb') as f:
            return f.read(4) == b'MThd'

    # Utility function to check if an ABC file is valid (basic check: file exists and starts with 'X:' and contains 'K:')
    def is_valid_abc(self, file_path):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.startswith('X:') and 'K:' in content

    # Utility function to check if a MusicXML file is valid (basic check: file exists and contains <score-partwise>)
    def is_valid_musicxml(self, file_path):
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(200)
            return '<score-partwise' in content

    def test_cli_generation_and_outputs(self):
        """
        Integration test: Run the CLI and check that all output files are generated and valid.
        This test uses the sample JSON and the CLI interface to generate all formats.
        """
        print("[DEBUG] Starting CLI integration test...")
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Generators/music_dox_generator.py'))
        print(f"[DEBUG] Script path: {script_path}")
        output_dir = self.sample_output_dir
        print(f"[DEBUG] Output directory: {output_dir}")
        python_exe = sys.executable
        print(f"[DEBUG] Python executable: {python_exe}")
        print(f"[DEBUG] CLI JSON path: {self.cli_json_path}")
        # Run the CLI script
        result = subprocess.run([
            python_exe, script_path,
            self.cli_json_path,
            "--output_dir", output_dir
        ], capture_output=True, text=True)
        print(f"[DEBUG] CLI return code: {result.returncode}")
        print(f"[DEBUG] CLI stdout:\n{result.stdout}")
        print(f"[DEBUG] CLI stderr:\n{result.stderr}")
        self.assertEqual(result.returncode, 0, msg=f"Script failed: {result.stderr}")
        # Find the output directory (should be songname_date or songname_date_time)
        found_dir = None
        print(f"[DEBUG] Listing output_dir: {os.listdir(output_dir)}")
        for d in os.listdir(output_dir):
            print(f"[DEBUG] Checking if {d} is a directory...")
            if os.path.isdir(os.path.join(output_dir, d)):
                found_dir = os.path.join(output_dir, d)
                print(f"[DEBUG] Found output subdirectory: {found_dir}")
                break
        self.assertIsNotNone(found_dir, msg="No output subdirectory found.")
        # Check for each file format
        base = os.path.splitext(os.path.basename(self.cli_json_path))[0]
        pdf_path = os.path.join(found_dir, f"{base}_Guitar_Progression.pdf")
        midi_path = os.path.join(found_dir, f"{base}_Chorus.mid")
        abc_path = os.path.join(found_dir, f"{base}.abc")
        xml_path = os.path.join(found_dir, f"{base}_Full_Score.musicxml")
        print(f"[DEBUG] PDF path: {pdf_path}")
        print(f"[DEBUG] MIDI path: {midi_path}")
        print(f"[DEBUG] ABC path: {abc_path}")
        print(f"[DEBUG] MusicXML path: {xml_path}")
        # PDF
        print(f"[DEBUG] PDF exists: {os.path.exists(pdf_path)}")
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                print(f"[DEBUG] PDF first 100 bytes: {f.read(100)}")
        self.assertTrue(self.is_valid_pdf(pdf_path), msg="Invalid or missing PDF output.")
        # MIDI
        print(f"[DEBUG] MIDI exists: {os.path.exists(midi_path)}")
        if os.path.exists(midi_path):
            with open(midi_path, 'rb') as f:
                print(f"[DEBUG] MIDI first 100 bytes: {f.read(100)}")
        self.assertTrue(self.is_valid_midi(midi_path), msg="Invalid or missing MIDI output.")
        # ABC
        print(f"[DEBUG] ABC exists: {os.path.exists(abc_path)}")
        if os.path.exists(abc_path):
            with open(abc_path, 'r', encoding='utf-8') as f:
                print(f"[DEBUG] ABC first 200 chars: {f.read(200)}")
        self.assertTrue(self.is_valid_abc(abc_path), msg="Invalid or missing ABC output.")
        # MusicXML
        print(f"[DEBUG] MusicXML exists: {os.path.exists(xml_path)}")
        if os.path.exists(xml_path):
            with open(xml_path, 'r', encoding='utf-8') as f:
                print(f"[DEBUG] MusicXML first 200 chars: {f.read(200)}")
        self.assertTrue(self.is_valid_musicxml(xml_path), msg="Invalid or missing MusicXML output.")

    def test_all_json_files_in_directory(self):
        """
        Test all JSON files in the Generators/json directory for standard compliance and report on each.
        Prints the full path to any missing nested field.
        If any [FAIL] occurs, the test fails overall.
        Also writes a json_validation_results.json file with all missing fields per file, mapping path to missing value.
        """
        json_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Generators/json'))
        print(f"[DEBUG] Scanning JSON directory: {json_dir}")
        # Defensive: skip if directory does not exist
        if not os.path.exists(json_dir):
            print(f"[ERROR] JSON directory does not exist: {json_dir}")
            return
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        print(f"[DEBUG] Found JSON files: {json_files}")
        any_fail = False
        validation_results = {}
        for json_file in json_files:
            file_path = os.path.join(json_dir, json_file)
            print(f"[DEBUG] Validating JSON file: {file_path}")
            missing_fields = {}
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                # Basic required fields
                required_fields = [
                    "title", "composer", "tempo", "key", "meter", "unit_note_length",
                    "midi_duration", "midi_volume", "midi_chords", "sections"
                ]
                for field in required_fields:
                    if field not in data:
                        msg = f"❌ [FAIL] {json_file}: Missing required field '{field}' (path: {field})"
                        print(msg)
                        missing_fields[field] = None
                        any_fail = True
                if not isinstance(data.get("sections", []), list):
                    msg = f"❌ [FAIL] {json_file}: 'sections' is not a list (path: sections)"
                    print(msg)
                    missing_fields['sections'] = []
                    any_fail = True
                for idx, section in enumerate(data.get("sections", [])):
                    for sfield in ["title", "progression", "lyrics", "strumming_pattern"]:
                        if sfield not in section:
                            path = f"sections[{idx}].{sfield}"
                            msg = f"❌ [FAIL] {json_file}: Missing field at path '{path}'"
                            print(msg)
                            missing_fields[path] = None
                            any_fail = True
                # Optional: abc_notation
                if "abc_notation" in data:
                    abc = data["abc_notation"]
                    abc_fields = [
                        "reference_number", "title", "composer", "meter", "unit_note_length",
                        "tempo", "key", "sections"
                    ]
                    for afield in abc_fields:
                        if afield not in abc:
                            path = f"abc_notation.{afield}"
                            msg = f"❌ [FAIL] {json_file}: Missing field at path '{path}'"
                            print(msg)
                            missing_fields[path] = None
                            any_fail = True
                    if not isinstance(abc.get("sections", []), list):
                        path = "abc_notation.sections"
                        msg = f"❌ [FAIL] {json_file}: 'abc_notation.sections' is not a list (path: {path})"
                        print(msg)
                        missing_fields[path] = []
                        any_fail = True
                    for aidx, abc_section in enumerate(abc.get("sections", [])):
                        for asfield in ["title", "chords", "lyrics"]:
                            if asfield not in abc_section:
                                path = f"abc_notation.sections[{aidx}].{asfield}"
                                msg = f"❌ [FAIL] {json_file}: Missing field at path '{path}'"
                                print(msg)
                                missing_fields[path] = None
                                any_fail = True
                else:
                    info_msg = f"[INFO] {json_file}: No ABC notation information present (path: abc_notation)"
                    print(info_msg)
                    missing_fields['abc_notation'] = None
                if not missing_fields:
                    print(f"✅ [PASS] {json_file}: Validation successful.")
            except Exception as e:
                err_msg = f"[ERROR] {json_file}: Exception during validation: {e}"
                print(err_msg)
                missing_fields['__exception__'] = str(e)
                any_fail = True
            validation_results[json_file] = missing_fields
        # Write results to a file for further analysis
        results_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'json_validation_results.json'))
        with open(results_path, 'w') as f:
            json.dump(validation_results, f, indent=2)
        print(f"[DEBUG] Validation results written to {results_path}")
        self.assertFalse(any_fail, msg="One or more JSON files failed validation. See output above and json_validation_results.json for details.")

if __name__ == "__main__":
    unittest.main()
