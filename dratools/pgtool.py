import importlib.resources
from os.path import normpath, join
from pathlib import PurePosixPath as Path
from pathlib import Path as NativePath

import click
import psycopg2
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


class PgShell:

    def __init__(self, pgcursor):
        self.pgcursor = pgcursor
        self.currdir = None

@click.command()
@click.option('host', '-h', envvar='PGHOST', default='localhost')
@click.option('port', '-p', envvar='PGPORT')
@click.option('user', '-U', envvar='PGUSER')
@click.option('dbname', '-d', envvar='PGDATABASE', default='postgres')
def cli(**kwargs):
    """
    Run a virtual shell session on a PostgreSQL server.

    Requires superuser permissions to the server.
    """

    conn = psycopg2.connect(**kwargs)
    print(conn)

    cur = conn.cursor()

    session = PromptSession()

    # Setup Database
    cur.execute('CREATE SCHEMA IF NOT EXISTS dratools;')
    cur.execute('SET search_path TO dratools;')

    try:
        create_execute_command_function = importlib.resources.read_text('dratools', 'execute_command.sql')
    except FileNotFoundError:
        create_execute_command_function = NativePath(__file__).parent.joinpath('execute_command.sql').read_text()


    cur.execute(create_execute_command_function)

    cur.callproc('dratools.execute_command', ['pwd'])
    currdir, = cur.fetchone()

    # Make Prompt
    cur.execute('SELECT current_role, inet_server_addr();')
    role, server_addr = cur.fetchone()

    cur.callproc('dratools.execute_command', ['hostname --fqdn'])
    hostname, = cur.fetchone()
    PS1 = f'{role}@{hostname}:{currdir} $ '


    cur.callproc('dratools.execute_command', ['ls'])
    filelist = cur.fetchall()
    completer = WordCompleter(list(name[0] for name in filelist))

    while True:
        try:
            command = session.prompt(PS1, completer=completer, complete_while_typing=False)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            if command.startswith('cd'):
                newdir = command.split()[1]
                if newdir.startswith('/'):
                    # absolute path, no joining necessary
                    pass
                else:
                    newdir = Path(currdir).joinpath(newdir)

                cur.callproc('dratools.execute_command', [f'cd {newdir}; pwd'])
                currdir, = cur.fetchone()

                cur.callproc('dratools.execute_command', [f'cd {currdir}; ls'])
                filelist = cur.fetchall()
                completer = WordCompleter(list(name[0] for name in filelist))

                PS1 = f'{role}@{hostname}:{currdir} $ '
            else:
                cur.callproc('dratools.execute_command', [f'cd {currdir}; ' + command])

                results = cur.fetchall()
                for row in results:
                    print(row[0])

    cur.close()
    conn.close()


if __name__ == '__main__':
    cli()
