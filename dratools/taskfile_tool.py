import json
import pickle
import sys

import click


@click.command()
@click.argument('task_file')
def cli(task_file):
    count = 0
    with open(task_file, 'rb') as f:
        config = pickle.load(f)

        json.dump(config, sys.stdout, indent=4, sort_keys=True,
                  cls=MyJsonEncoder)
        print()

        try:
            while True:
                task = pickle.load(f)
                count += 1
        except EOFError:
            pass

    print(f'Found {count} tasks')


class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)


if __name__ == '__main__':
    cli()
