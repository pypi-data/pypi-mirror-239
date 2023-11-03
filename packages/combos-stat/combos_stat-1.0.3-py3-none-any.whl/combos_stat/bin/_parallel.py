from multiprocessing import Pool

import click
import pandas as pd

from combos_stat.stat import CombosStat



def process_chunk(chunk: pd.DataFrame):
    print('*' * 200)
    print(chunk.head())


@click.command()
@click.option('-i', '--input-file', help='Path to the input data file', type=click.Path(exists=True))
@click.option('-c', '--chunksize', help='The chunksize to use for the parallel processing', type=int, default=1000)
def main(**kwargs):
    chunks = pd.read_csv(kwargs['input_file'], chunksize=kwargs['chunksize'], sep='\t', header=0)

    with Pool(2) as pool:
        results = pool.map(process_chunk, chunks)




if __name__ == '__main__':
    main()
