from infi.systray import SysTrayIcon
from jaraco import clipboard

from dratools import dev_box
from dratools.dev_box import launch

hover_text = "SysTrayIcon Demo"


def hello(sysTrayIcon):
    print("Hello World.")


def simon(sysTrayIcon):
    print("Hello Simon.")


def bye(sysTrayIcon):
    print('Bye, then.')


def do_nothing(sysTrayIcon):
    pass


def do_launch_dev_box(sysTrayIcon):
    launch()


def copy_dev_box_hostname(sysTrayIcon):
    hostname = dev_box.get_hostname()
    if hostname is not None:
        clipboard.copy_text(hostname)


menu_options = (('Launch Dev Box', "hello.ico", do_launch_dev_box),
                ('Copy dev box host', None, copy_dev_box_hostname),
                ('Do nothing', None, do_nothing),
                ('A sub-menu', "submenu.ico", (('Say Hello to Simon', "simon.ico", simon),
                                               ('Do nothing', None, do_nothing),
                                               ))
                )
sysTrayIcon = SysTrayIcon("main.ico", hover_text, menu_options, on_quit=bye, default_menu_index=1)
sysTrayIcon.start()
print("started systray")

from dratools.remote_utils_server import app

app.run(port=9999)

print("started flask")
