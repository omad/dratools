"""
RPC to enable a remote SSH login some control over the local machine.

Implemented as HTTP because it's easy and supported by everything.

Zero security, buyer beware
"""
import time
import webbrowser
from io import BytesIO

from ahk import AHK
from flask import Flask, request, send_file
from jaraco import clipboard
from jaraco.clipboard import paste_text

webbrowser.register('firefox', None,
                    instance=webbrowser.BackgroundBrowser(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"))

ahk = AHK()
app = Flask(__name__)

def get_current_page():
    win = ahk.find_window(lambda w: b'Google Chrome' in w.title)
    win.send('^l')
    time.sleep(0.2)
    win.send('^c')
    time.sleep(0.1)
    url = paste_text()
    title = win.title.decode('utf8')
    return url, title


@app.route("/openurl", methods=['POST'])
def openurl():
    url = request.form['url']
    webbrowser.get('firefox').open(url)
    return f"tried to launch firefox with {url}\n"


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


@app.route("/playpause", methods=['POST'])
def play_pause():
    ahk.send_input('{Media_Play_Pause}')


@app.route("/vol_up", methods=['POST'])
def vol_up():
    ahk.send_input('{Volume_Up}')

@app.route("/vol_down", methods=['POST'])
def vol_down():
    ahk.send_input('{Volume_Down}')

