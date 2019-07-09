"""
RPC to enable a remote SSH login some control over the local machine.

Implemented as HTTP because it's easy and supported by everything.

Zero security, buyer beware
"""
import webbrowser
from io import BytesIO

from flask import Flask, request, send_file
from jaraco import clipboard

webbrowser.register('firefox', None,
                    instance=webbrowser.BackgroundBrowser(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"))

app = Flask(__name__)


@app.route("/openurl", methods=['POST'])
def openurl():
    url = request.form['url']
    webbrowser.get('firefox').open(url)
    return "tried to launch firefox"


@app.route("/copyhtml", methods=['POST'])
def copyhtml():
    content = request.form['content']
    clipboard.copy_html(content)


@app.route("/captureclipboard")
def captureclipboard():
    from jaraco.clipboard import paste, paste_html, paste_text, paste_image
    try:
        text = paste()
    except TypeError:
        pass
    try:
        from PIL import Image
        data = paste_image()
        im_data = BytesIO(data)
        image = Image.open(im_data)
        # Rewrite as in memory PNG
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except TypeError:
        pass


