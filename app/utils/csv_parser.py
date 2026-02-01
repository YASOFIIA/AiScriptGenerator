from dataclasses import dataclass
from typing import List
from pathlib import Path
import csv

@dataclass
class CsvRow:
    episode_code: str
    raw_text: str

def parse_csv(file_path: Path) -> List[CsvRow]:
    rows: List[CsvRow] = []
    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for line in reader:
            if not line:
                continue
            raw = " | ".join([x.strip() for x in line if x.strip()]).strip()
            if not raw:
                continue

            episode_code = raw.split()[0].strip()
            rows.append(CsvRow(episode_code=episode_code, raw_text=raw))

    return rows