import click
import psycopg2
from prompt_toolkit.history import InMemoryHistory


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

    history = InMemoryHistory()

    # Setup Database
    cur.execute('CREATE SCHEMA IF NOT EXISTS dratools;')
    cur.execute('SET search_path TO dratools;')
    with open('execute_command.sql') as fin:
        create_execute_command_function = fin.read()
    cur.execute(create_execute_command_function)

    # Make Prompt
    cur.execute('SELECT current_role, inet_server_addr();')
    role, server_addr = cur.fetchone()

    cur.callproc('dratools.execute_command', ['hostname --fqdn'])
    hostname, = cur.fetchone()
    prompt = f'{role}@{hostname} $ '

    while True:
        try:
            command = input(prompt)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            cur.callproc('dratools.execute_command', [command])

            results = cur.fetchall()
            for row in results:
                print(row[0])

    cur.close()
    conn.close()


if __name__ == '__main__':
    cli()
