import os
import sys

import jinja2
from lxml import etree
from z3c.rml import document

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.normpath(os.path.join(PROJECT_ROOT, 'static'))
TEMPLATE_ROOT = os.path.normpath(os.path.join(PROJECT_ROOT, 'templates'))

template_loader = jinja2.FileSystemLoader(TEMPLATE_ROOT)
jinja2_env = jinja2.Environment(loader=template_loader)


def main(pdf_output_filepath):

    template = jinja2_env.get_template(
        'template1.rml'
    )

    context = {
        "STATIC_ROOT": STATIC_ROOT,
    }

    rml = template.render(**context)

    rml = unicode(rml).encode('utf-8').strip()

    # create a buffer in memory
    buf = StringIO.StringIO()
    buf_in = StringIO.StringIO(rml)

    root = etree.parse(buf_in).getroot()
    doc = document.Document(root)
    doc.filename = "imax-feedback.pdf"

    doc.process(buf)

    # Rewind the buffer.
    buf.seek(0)

    with open(pdf_output_filepath, 'wb') as f:
        f.write(buf.getvalue())


if __name__ == '__main__':
    print sys.argv
    output_path = sys.argv[1]
    main(output_path)
