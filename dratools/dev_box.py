import socket

try:
    import winreg

    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False
    print('Not running on windows, some funcs will fail')
from time import sleep

import boto3
import click

INSTANCE_NAME = 'dra-new-dev-box'
INSTANCE_NAME = 'dra-ubuntu-dev-box'
PUTTY_KEY = r'Software\SimonTatham\PuTTY\Sessions'
# PUTTY_KEY = r'Software\Microsoft\AppV\Client\Packages\5AE56FD3-EBB7-437C-93FA-3B1247A40DBB\REGISTRY\USER\S-1-5-21-10245634-2577594509-1919486750-9548\Software\SimonTatham\PuTTY\Sessions'
PUTTY_SESSION = 'aws-dev-box'

INSTANCES = {
    'nixos': {
        'putty-session': 'aws-dev-box',
        'instance-name': 'dra-new-dev-box'
    },
    'ubuntu': {
        'putty-session': 'aws-dev-box',
        'instance-name': 'dra-ubuntu-dev-box'
    }
}


@click.command()
def main():
    launch('nixos')


def launch(name):
    instance_name = INSTANCES[name]['instance-name']
    putty_session = INSTANCES[name]['putty-session']
    instance = get_instance(instance_name)

    if instance.state['Name'] == 'running':
        print(f'Dev Box Already Running at {instance.public_dns_name}. Launching Putty')
    else:
        print(instance.state)
        instance.start()
        instance.wait_until_running()
        print(instance.public_dns_name)
        wait_for_open_port(instance.public_dns_name, port=22, timeout=30)

    if IS_WINDOWS:
        set_putty_host_name(putty_session, instance.public_dns_name)
        launch_putty_session(putty_session)
    else:
        import os
        os.execlp("ssh", "ssh", instance.public_dns_name)


def get_instance(instance_name):
    client = boto3.client('ec2')
    hosts = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
    instance_id = hosts['Reservations'][0]['Instances'][0]['InstanceId']
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    return instance


def get_hostname(name):
    instance = get_instance(INSTANCES[name]['instance_name'])
    if instance.state['Name'] == 'running':
        return instance.public_dns_name


def set_putty_host_name(session, new_hostname):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PUTTY_KEY + '\\' + session, 0, winreg.KEY_ALL_ACCESS) as key:
        old_val, reg_type = winreg.QueryValueEx(key, 'HostName')
        winreg.SetValueEx(key, 'HostName', 0, reg_type, new_hostname)


def launch_putty_session(session):
    import subprocess
    subprocess.Popen(['putty.exe', '-load', session], creationflags=subprocess.CREATE_NEW_CONSOLE)


def wait_for_open_port(host, port, timeout=2, retries=5):
    for _ in range(retries):
        try:
            with socket.create_connection((host, port)) as sock:
                if sock:
                    return True
        except Exception as e:
            print(e)
        sleep(5)

    raise Exception("Cannot connect")


if __name__ == '__main__':
    main()
