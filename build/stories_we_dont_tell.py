import json

# Re-define the song data after code state reset
song_data = {
    "pdf_output": "Persistent_Misconduct_Stories_We_Dont_Tell.pdf",
    "midi_output": "Persistent_Misconduct_Stories_We_Dont_Tell.mid",
    "tempo": 136,
    "midi_duration": 4,
    "midi_volume": 80,
    "midi_chords": {
        "D": [50, 57, 62],
        "C": [48, 55, 60],
        "Bb": [46, 53, 58],
        "A": [45, 52, 57],
        "Bm": [47, 54, 59],
        "G": [43, 50, 55]
    },
    "midi_progression": ["D", "D", "C", "C", "D", "D", "C", "C", "Bb", "A"],
    "sections": []
}

# Helper for chord chart
def chord_diagram(name, frets):
    lines = ["e|" + frets[0], "B|" + frets[1], "G|" + frets[2], "D|" + frets[3], "A|" + frets[4], "E|" + frets[5]]
    return f"{name} Chord\n" + "\n".join(lines) + "\n"

# Chord diagrams
chord_charts = {
    "D": chord_diagram("D Major", ["-2-", "-3-", "-2-", "-0-", "---", "---"]),
    "C": chord_diagram("C Major", ["-0-", "-1-", "-0-", "-2-", "-3-", "---"]),
    "Bb": chord_diagram("Bb Major", ["-1-", "-3-", "-3-", "-3-", "-1-", "-1-"]),
    "A": chord_diagram("A Major", ["-0-", "-2-", "-2-", "-2-", "-0-", "---"]),
    "Bm": chord_diagram("Bm", ["-2-", "-3-", "-4-", "-4-", "-2-", "---"]),
    "G": chord_diagram("G Major", ["-3-", "-3-", "-0-", "-0-", "-2-", "-3-"])
}

# Song structure
song_data["sections"] = [
    {
        "title": "Chorus (Relationships)",
        "content": """Chorus Progression: D - D - C - C - D - D - C - C - Bb - A
Strumming Pattern: ↓ ↓ ↑ ↑ ↓ ↑

Persistent misconduct, under love’s disguise  
In silence we falter, avoiding each other's eyes  
Words unspoken build this living shell  
A house full of echoes—stories we don’t tell
"""
    },
    {
        "title": "Verse (Relationships)",
        "content": f"""Verse Progression: D - D - C - C - D - D - C - C - Bb - A
Strumming Pattern: ↓ ↓ ↑ ↑ ↓ ↑

We promised forever but spoke in delay  
Avoiding the mess in the things we won’t say  
Pride became silence, silence became a wall  
The louder we loved, the harder the fall

{chord_charts['D']}{chord_charts['C']}{chord_charts['Bb']}{chord_charts['A']}
"""
    },
    {
        "title": "Chorus (Culture)",
        "content": """Chorus Progression: D - D - C - C - D - D - C - C - Bb - A
Strumming Pattern: ↓ ↓ ↑ ↑ ↓ ↑

Persistent misconduct, in the songs we sing  
Legacies lost in the noise we bring  
We edit the truth like it never fell—  
These borrowed traditions, stories we don’t tell
"""
    },
    {
        "title": "Verse (Culture)",
        "content": f"""Verse Progression: D - D - C - C - D - D - C - C - Bb - A
Strumming Pattern: ↓ ↓ ↑ ↑ ↓ ↑

We dance to rhythms borrowed, tales retold  
Lost our roots while chasing gold  
Traded our tongue for market spell  
Shallow pride—stories we don’t tell

{chord_charts['D']}{chord_charts['C']}{chord_charts['Bb']}{chord_charts['A']}
"""
    },
    {
        "title": "Chorus (Politics)",
        "content": """Chorus Progression: D - D - C - C - D - D - C - C - Bb - A
Strumming Pattern: ↓ ↓ ↑ ↑ ↓ ↑

Persistent misconduct, behind every suit and tie  
Deals in the dark while the poor scrape by  
We pledge with hope but live in hell  
Underneath the anthem—stories we don’t tell
"""
    },
    {
        "title": "Verse (Politics)",
        "content": f"""Verse Progression: D - D - C - C - D - D - C - C - Bb - A
Strumming Pattern: ↓ ↓ ↑ ↑ ↓ ↑

They smile on screens, pretend to care  
While hunger lingers in the midnight air  
One hand signs while the other rebels  
Justice blindfolded—stories we don’t tell

{chord_charts['D']}{chord_charts['C']}{chord_charts['Bb']}{chord_charts['A']}
"""
    },
    {
        "title": "Bridge Section",
        "content": f"""Bridge Progression: Bm - G - D - A - Bm - G - Bb - A
Strumming Pattern: ↓ ↓ ↑ ↑ ↓ ↑

In the quiet corners, secrets learned to grow  
In stories never spoken, there’s more than we let show  
We dressed our pain in patience, called it something wise  
But every silent witness wears the same disguise…

{chord_charts['Bm']}{chord_charts['G']}{chord_charts['D']}{chord_charts['A']}{chord_charts['Bb']}
"""
    }
]

# Save the final JSON file
# Json output file path root
json_path = "/home/thunda/123_Labs/json/"
file_path=json_path + "Stories_We_Dont_Tell.json"
with open(file_path, "w") as f:
    json.dump(song_data, f, indent=4)

json_path
