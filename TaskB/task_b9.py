# B9: Markdown to HTML Conversion
from TaskB.task_b12 import B12
import markdown

def B9(md_path, output_path):
    if not B12(md_path):
        return None
    if not B12(output_path):
        return None
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)
