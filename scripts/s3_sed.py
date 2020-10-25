import click
from odc.aws import s3_client, s3_fetch, s3_dump
from tqdm import tqdm

s3 = None


@click.command('s3-find')
@click.option('--no-sign-request', is_flag=True,
              help='Do not sign AWS S3 requests')
@click.argument('file_list', type=click.File('r'), nargs=1)
def cli(file_list, no_sign_request=None):
    global s3
    s3 = s3_client(aws_unsigned=no_sign_request)

    urls = [line.rstrip() for line in file_list.readlines()]
    for url in tqdm(urls):
        if not url:
            continue
        tqdm.write(f"Updating {url}", end='')
        replace_in_s3_obj(url)


def replace_in_s3_obj(s3_url):
    try:
        original = s3_fetch(s3_url, s3)
    except ValueError as e:
        tqdm.write(str(e))
        return
    contents = original.replace(b'LANDSAT_8', b'LANDSAT_7')
    contents = contents.replace(b'OLI', b'ETM')

    if original != contents:
        s3_dump(contents, s3_url, s3)
        tqdm.write('.')
    else:
        tqdm.write(' - Skipped.')


if __name__ == '__main__':
    cli()
