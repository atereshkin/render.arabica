import os
import subprocess
import string
import random
import tempfile
import hashlib
import re

from flask import Flask, request, send_file

import svgwrite

app = Flask(__name__)

def random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

def sanitize_fname(value):
    return re.sub('[^\w\s-]', '', value)

@app.route('/text-to-svg/', methods=['POST'])
def hello_world():
    if 'text' not in request.form:
        return #TODO 405 bad request
    text = request.form['text']
    assert len(text) < 10000
    download_fname = sanitize_fname(request.form['filename'])
    assert len(download_fname) <= 16
    fname = os.path.join(tempfile.gettempdir(), '{}-{}.svg'.format(hashlib.md5(text.encode('utf-8')).hexdigest(),
                                                                   random_string(5)))
    dwg = svgwrite.Drawing(fname,  size=('100px', '100px'),)
    txt_el = dwg.text('', font_size='64px', direction='rtl', text_anchor='middle', writing_mode='rl-tb', font_family='Noto Sans Arabic')
    for idx, line in enumerate(text.split('\n')):
        tspan = dwg.tspan(line, x='0', dy=['0.6em'] if idx == 0 else ['1.2em'])
        txt_el.add(tspan)
    dwg.add(txt_el)
    dwg.save()
    subprocess.run(['xvfb-run', 'inkscape', '--with-gui', '--verb', 'EditSelectAll;ObjectToPath;FitCanvasToDrawing;FileSave;FileQuit', fname])


    return send_file(fname, mimetype='image/svg+xml', as_attachment=True, download_name='{}.svg'.format(download_fname))
