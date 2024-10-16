# **ConvergentdNdS**

The simulator [SimuEvol](https://github.com/ThibaultLatrille/SimuEvol) is required to generate the alignments.

## Installing *SimuEvol*

Install the compiling toolchains:
```
sudo apt install -qq -y make cmake clang
```
In the root folder of **ConvergentdNdS**, clone and compile the C++ code for *SimuEvol*
```
git clone https://github.com/ThibaultLatrille/SimuEvol && cd SimuEvol && make tiny && cd ..
```

## Replicate experiments

Running `snakemake` will generate the alignments for the experiment described `config/config.yaml`:
```
snakemake -j ${CPU} -k
```

To run the experiments for all the configurations in the `config` folder, you can use the following script:
```
CPU=8
for EXPERIMENT in config/Mammals*.yaml; do
  cp -rf "${EXPERIMENT}" "config/config.yaml"
  snakemake -j ${CPU} -k
done
```

Running the script `dataset.py` will create a folder `dataset` containing the alignments (in fasta format), the tree used to generate the simulations (`rootedtree.OrthoMam.nhx`), and a `dataset.csv` table which contains the relationships between the name of the fasta and the parameters that were used for the simulations.