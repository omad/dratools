import socket
import winreg
from contextlib import closing

import boto3
import click

INSTANCE_NAME = '*dra*'
PUTTY_KEY = r'Software\SimonTatham\PuTTY\Sessions'
PUTTY_SESSION = 'aws-dev-box'


@click.command()
def main():
    client = boto3.client('ec2')
    hosts = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [INSTANCE_NAME]}])

    instance_id = hosts['Reservations'][0]['Instances'][0]['InstanceId']

    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)

    if instance.state['Name'] == 'running':
        print(f'Dev Box Already Running at {instance.public_dns_name}. Launching Putty')
        set_putty_host_name(PUTTY_SESSION, instance.public_dns_name)
        launch_putty_session(PUTTY_SESSION)
    else:
        print(instance.state)
        instance.start()
        instance.wait_until_running()
        print(instance.public_dns_name)
        set_putty_host_name(PUTTY_SESSION, instance.public_dns_name)
        wait_for_open_port(instance.public_dns_name, port=22, timeout=30)
        launch_putty_session(PUTTY_SESSION)


def set_putty_host_name(session, new_hostname):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PUTTY_KEY + '\\' + session, 0, winreg.KEY_ALL_ACCESS) as key:
        old_val, reg_type = winreg.QueryValueEx(key, 'HostName')
        winreg.SetValueEx(key, 'HostName', 0, reg_type, new_hostname)


def launch_putty_session(session):
    import subprocess
    subprocess.Popen(['putty.exe', '-load', session], creationflags=subprocess.CREATE_NEW_CONSOLE)


def wait_for_open_port(host, port, timeout=2):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) == 0:
            return
        else:
            raise Exception("Cannot connect")


if __name__ == '__main__':
    main()
