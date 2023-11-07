import argparse
import numpy as np
import pandas as pd
import scanpy as sc
import os

sc.settings.verbosity = 3             # verbosity: errors (0), warnings (1), info (2), hints (3)

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--genes_file", required=True, help="tsv file containing gene names")
parser.add_argument("-m", "--matrix_file", required=True, help="file containing the geneXcell matrix")
parser.add_argument("-b", "--barcodes_file", required=True, help="file containing the cell ids(barcodes)")
parser.add_argument("-i", "--input_path", required=True, help="file containing the starsolo data")
parser.add_argument("--output_hdf5", required=True, help="path to the output hdf5 file")
args = parser.parse_args()

# Check if genes_file exists and is in the .gz format
if not os.path.exists(args.genes_file):
    raise FileNotFoundError(f"{args.genes_file} does not exist")

# Check if matrix_file exists and is in the .gz format
if not os.path.exists(args.matrix_file):
    raise FileNotFoundError(f"{args.matrix_file} does not exist")


# Check if barcodes_file exists and is in the .gz format
if not os.path.exists(args.barcodes_file):
    raise FileNotFoundError(f"{args.barcodes_file} does not exist")

adata = sc.read_10x_mtx(args.input_path,  # the directory with the `.mtx` file
    var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
    cache=True)                              # write a cache file for faster subsequent reading

adata.var_names_make_unique()  # this is unnecessary if using `var_names='gene_ids'` in `sc.read_10x_mtx`
adata.raw = adata
adata.raw.to_adata().write(args.output_barcode)