from functools import partial
from infi.systray import SysTrayIcon
from jaraco import clipboard

from dratools import dev_box
from dratools.remote_utils_server import app

hover_text = "SysTrayIcon Demo"


def hello(sysTrayIcon):
    print("Hello World.")


def simon(sysTrayIcon):
    print("Hello Simon.")


def bye(sysTrayIcon):
    print('Bye, then.')


def do_nothing(sysTrayIcon):
    pass


def do_launch_dev_box(sysTrayIcon, name):
    dev_box.launch(name)


def copy_dev_box_hostname(sysTrayIcon):
    hostname = dev_box.get_hostname()
    if hostname is not None:
        clipboard.copy_text(hostname)


def main():
    menu_options = (('Launch Nix Box', "hello.ico", partial(do_launch_dev_box, name='nixos')),
                    ('Launch Ubuntu Box', "hello.ico", partial(do_launch_dev_box, name='ubuntu')),
                    ('Copy Nix Box hostname', None, partial(copy_dev_box_hostname, name='nixos')),
                    ('Copy Ubuntu Box hostname', None, partial(copy_dev_box_hostname, name='ubuntu')),
                    ('Do nothing', None, do_nothing),
                    ('A sub-menu', "submenu.ico", (('Say Hello to Simon', "simon.ico", simon),
                                                   ('Do nothing', None, do_nothing),
                                                   ))
                    )
    sysTrayIcon = SysTrayIcon("main.ico", hover_text, menu_options, on_quit=bye, default_menu_index=1)
    sysTrayIcon.start()
    print("started systray")

    app.run(port=9999)

    print("started flask")

if __name__ == '__main__':
    main()
