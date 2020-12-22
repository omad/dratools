import pickle
from pathlib import Path
from typing import Optional
import typer
from tqdm import tqdm

app = typer.Typer()


@app.command()
def main(filename: Path):
    """Count the number of objects in a pickle file"""
    filesize = filename.stat().st_size
    count = 0
    with filename.open('rb') as f, tqdm(total=filesize, unit='B', unit_scale=True,
                                        ) as pbar:
        while True:
            try:
                pickle.load(f)
            except ImportError:
                pass
            except Exception as e:
                typer.echo(e)
                break
            count += 1
            filepos = f.tell()
            pbar.set_postfix(count=count, refresh=False)
            pbar.update(filepos - pbar.n)  # Update expects an increment, not a total


    typer.echo(f"Found {count} objects in {filename}.")


if __name__ == "__main__":
        typer.run(main)
