from dataclasses import dataclass
from pathlib import Path
from typing import List
from docx import Document
from docx.shared import Pt, RGBColor

@dataclass
class ScriptOutput:
    episode_code: str
    title: str
    script_text: str

def build_docx(outputs: List[ScriptOutput], out_path: Path) -> None:
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(14)
    font.color.rgb = RGBColor(0, 0, 0)

    for i, item in enumerate(outputs, start=1):
        doc.add_paragraph(f"Episode Code - {item.episode_code}")
        doc.add_paragraph(item.title.strip())
        doc.add_paragraph(item.script_text.strip())

        if i != len(outputs):
            doc.add_paragraph("") 

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
