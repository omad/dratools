"""
This tool is for bulk rotating AWS Keys in GH Actions and Travis-CI repos

"""

import typer

gh_repos = [
    'GeoscienceAustralia/COG-Conversion'
]


def main(name: str):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
