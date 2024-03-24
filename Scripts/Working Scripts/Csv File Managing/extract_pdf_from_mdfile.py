import os

from markdown import markdown
import pdfkit
# Get the absolute filepath
dirname = os.path.dirname(__file__)
final_dirname = '\\'.join(dirname.split("\\")[0:6])
input_filename = final_dirname + '\\README.md'
output_filename = final_dirname + '\\README.pdf'

with open(input_filename, 'r', encoding="utf8") as f:
    html_text = markdown(f.read(), output_format='html4')

pdfkit.from_string(html_text, output_filename)
