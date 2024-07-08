import os

import numpy as np
import glob
import shutil
from collections import defaultdict
import pandas as pd

# Clear the dataset directory
shutil.rmtree('dataset', ignore_errors=True)
# Create the dataset directory
os.makedirs('dataset', exist_ok=True)
shutil.copy("data/trees/rootedtree.OrthoMam.nhx", "dataset/rootedtree.OrthoMam.nhx")

random_set = set()
if __name__ == '__main__':
    # Find all the fasta files in the directory experiments/*/*/*.fasta
    fasta_files = glob.glob('experiments/*/*/*.fasta')
    outdict = defaultdict(list)
    for fasta_file in fasta_files:
        print(fasta_file)
        exp, lambda_value, replicate = fasta_file.split('/')[1:]
        # Generate a random integer
        random_int = np.random.randint(1e3, 1e9)
        while random_int in random_set:
            random_int = np.random.randint(1e3, 1e9)
        random_set.add(random_int)
        # Create a new file name
        new_file_name = f'dataset/{random_int}.fasta'
        # copy the file to the new file name
        shutil.copy(fasta_file, new_file_name)
        outdict["experiment"].append(exp)
        outdict["lambda"].append(lambda_value)
        outdict["key"].append(random_int)

    df = pd.DataFrame(outdict)
    df.to_csv('dataset/dataset.csv', index=False)
