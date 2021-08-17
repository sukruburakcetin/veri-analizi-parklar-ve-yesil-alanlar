from markdown import markdown
import pdfkit

input_filename = '../../../Scripts/Working Scripts/Csv File Managing/README.md'
output_filename = '../../../Scripts/Working Scripts/Csv File Managing/README.pdf'

with open(input_filename, 'r') as f:
    html_text = markdown(f.read(), output_format='html4')

pdfkit.from_string(html_text, output_filename)