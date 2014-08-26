import subprocess
import tempfile
import uuid

from flask import current_app as app
from flask import Response, g
from path import path

from mrt.utils import read_file


def stream_template(template_name, **context):
    app.update_template_context(context)
    template = app.jinja_env.get_template(template_name)
    rv = template.stream(context)
    rv.enable_buffering(5)
    return rv


def render_pdf(template_name, width=None, height=None,
               orientation="portrait", **context):
    g.is_rendered_as_pdf = True
    tmp_folder = path(tempfile.mkdtemp())
    template_path = tmp_folder / (str(uuid.uuid4()) + '.html')
    pdf_path = tmp_folder / (str(uuid.uuid4()) + '.pdf')
    with open(template_path, 'w+') as f:
        for chunk in stream_template(template_name, **context):
            f.write(chunk.encode('utf-8'))

    def generate():
        with open(tmp_folder / 'stderr.log', 'w+') as stderr:
            command = [
                'wkhtmltopdf',
                '-q',
                "--encoding", "utf-8",
                "--page-height", height,
                "--page-width", width,
                "--margin-bottom", "0",
                "--margin-top", "0",
                "--margin-left", "0",
                "--margin-right", "0",
                "--orientation", orientation,
                str(template_path), str(pdf_path), ]
            subprocess.check_call(command, stderr=stderr)

    try:
        generate()
        pdf = open(pdf_path, 'rb')
    finally:
        tmp_folder.rmtree()

    return Response(read_file(pdf), mimetype='application/pdf')
