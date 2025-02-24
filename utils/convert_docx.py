import re
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

from utils.path_utils import PathManager, PathFlag


def docx_to_text(in_path: str | Path, out_path: str | Path):
    in_path = PathManager(in_path)
    out_path = PathManager(out_path, PathFlag.C)
    out_path.suffix = ".txt"
    doc: Document = Document(str(in_path.resolve_new_path))

    with open(out_path.resolve_new_path, 'w', encoding='utf-8') as file:
        def write_to_file(text):
            nonlocal txt
            text = re.sub(r'‎', '', text)
            if '{{' in text:
                print(re.match(r'(\{\{.*}})', text).group())
            file.write(text + '\n')

        for section in doc.sections:
            for item in section.iter_inner_content():
                if isinstance(item, Paragraph):
                    write_to_file(item.text)
                elif isinstance(item, Table):
                    for row in item.rows:
                        for cell in row.cells:
                            for paragraph in cell.paragraphs:
                                write_to_file(paragraph.text)


def docx_to_html(in_path: str | Path, out_path: str | Path):
    import mammoth
    in_path = PathManager(in_path)
    out_path = PathManager(out_path, PathFlag.C)
    out_path.suffix = ".html"
    with open(in_path.resolve_new_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html_script = result.value
        indents = 0
        with open(out_path.resolve_new_path, 'w', encoding='utf-8') as html_file:
            for line in html_script.splitlines():
                line = re.sub(r'\|.*?\|', '', line.strip())
                line = re.sub(r'(\[\[|]])', '', line)
                line = re.sub(r'‎', '', line)
                if '{{' in line:
                    print(re.match(r'(\{\{.*}})', line).group())
                if re.match(r'^<.*>', line.strip()):
                    indents += 1
                if re.match(r'</.*>$', line.strip()):
                    indents -= 1
                html_file.write('\t' * indents + line + '\n')
