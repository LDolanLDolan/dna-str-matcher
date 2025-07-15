
import csv
import re
from typing import Dict, List, Tuple

def read_database(csv_path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    """Return header STRs list and rows of database as dicts."""
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        header_strs = reader.fieldnames[1:]  # skip 'name'
        rows = [row for row in reader]
    return header_strs, rows

def longest_match(sequence: str, subsequence: str) -> int:
    """Return length of longest run of subsequence in sequence (CS50 logic)."""
    pattern = f'(?:{re.escape(subsequence)})+'
    matches = re.finditer(pattern, sequence)
    longest = 0
    for m in matches:
        run_length = (m.end() - m.start()) // len(subsequence)
        longest = max(longest, run_length)
    return longest

def str_counts(sequence: str, strs: List[str]) -> Dict[str, int]:
    return {s: longest_match(sequence, s) for s in strs}

def match_profile(db_rows: List[Dict[str, str]], counts: Dict[str, int]) -> str:
    for row in db_rows:
        if all(int(row[str_]) == counts[str_] for str_ in counts):
            return row['name']
    return "No match"

def regions(sequence: str, strs: List[str]) -> List[Dict]:
    """Return list of dicts with start/end for each longest region."""
    regions = []
    for s in strs:
        pattern = f'(?:{re.escape(s)})+'
        best = None
        for m in re.finditer(pattern, sequence):
            run_length = (m.end() - m.start()) // len(s)
            if run_length > 1:
                if not best or run_length > best[2]:
                    best = (m.start(), m.end(), run_length)
        if best:
            regions.append({'str': s, 'start': best[0], 'end': best[1]})
    return regions
