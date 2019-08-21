import rasterio
from tqdm import tqdm
from glob import glob


def check_files(src_datasets):
    broken_files = set()
    for src_dataset in tqdm(src_datasets):
        src_dataset = src_dataset
        with rasterio.open(src_dataset) as src:
            try:
                src.read()
            except Exception:
                broken_files.add(src_dataset)

    return broken_files


def check_from_file(filename):
    with open(filename) as f:
        src_datasets = [src_dataset.strip() for src_dataset in f]
    return src_datasets


def check_dirs(grid_cells):
    to_check = []
    for grid in grid_cells:
        found = ['NETCDF:%s:swir2' % fname for fname in glob('/g/data/rs0/datacube/002/LS8_OLI_NBAR/%s/*.nc' % grid)]
        to_check.extend(found)
    return to_check


if __name__ == '__main__':
#    filename = 'possibly_dodgy_files.txt'
#    broken_files = check_files(check_from_file(filename))

    to_check = check_dirs(['18_-34', '8_-42'])


    broken_files = check_files(to_check)

    print("Broken files are:")
    for b in broken_files:
        print(b)
