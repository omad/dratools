"""
RPC to enable a remote SSH login some control over the local machine.

Implemented as HTTP because it's easy and supported by everything.

Zero security, buyer beware
"""
import webbrowser

from flask import Flask, request
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
