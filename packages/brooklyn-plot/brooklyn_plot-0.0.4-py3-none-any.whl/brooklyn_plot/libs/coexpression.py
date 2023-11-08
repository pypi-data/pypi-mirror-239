#!/usr/bin/python
# This is used to calculate pearson correlations of a user defined set of genes against a user defined set of targets.
# The purpose is to generate data for a Brooklyn plot - evaluating coexpression patterns in single cell datasets
# which inform on chromosomal bursting and coexpression.
# Code by Arun Patil and Marc Halushka (2022)

import numpy as np
import scipy as sp
import scanpy as sc
import pandas as pd
import scipy
import time
import concurrent.futures
from pathlib import Path
from scipy import stats

from .rbaco import bayesian_cor
#import glob
#import bbknn
#import os, fnmatch
#import requests
#import io
#import seaborn as sns
#sc.settings.verbosity = 3
#sc.settings.set_figure_params(dpi = 120, color_map = 'RdBu_r')

# This function will execute the co-expression either serially or in parallel
def coex_fun(geneList_chunk, data, outdir, refseq, againstList, corMethod, h5ad_cm):
    # Ignore numpy error 
    np.seterr(divide = 'ignore')
    for gs in geneList_chunk:
        i1 = np.where(h5ad_cm.var_names == gs)[0][0]
        out = []
        for gene in againstList:
            i2 = np.where(h5ad_cm.var_names == gene)[0][0]
            if corMethod == 'pr':
                res = stats.pearsonr(data[:, i1], data[:, i2])
            elif corMethod == 'kt':
                res = stats.kendalltau(data[:, i1], data[:, i2])
            out.append([gene, res[0], res[1]])
        df = pd.DataFrame(out, columns = ['gene', 'r', 'p'])
        df['bon'] = df.p * len(df)
        df['neg_log10_p'] = -np.log10(df.p)
        df = df[df.bon < 0.05].sort_values('bon').reset_index(drop = True)
        required_df = pd.merge(df, refseq[['gene_ids','hgnc_symbol', 'chromosome_name', 'start_position', 'xMean', 'end_position', 'band']], how='left', left_on='gene', right_on='gene_ids').drop(columns = ['gene_ids'])
        outname= outdir + "/gene_" + str(gs) + ".csv"
        required_df.to_csv(outname, index=False)


# This function, will break the gene list in to m-chunks where m is determined below
def chunkifyList(glist, numChunks):
    for i in range(0, len(glist), numChunks):
        yield glist[i:i + numChunks]



def brooklyn_arch(h5file, workDir, annotations, gl, agl, threads, cm, fileBase):
    #Start time
    brooklyn_start = time.perf_counter()
    # Set/initialize global input items
    global h5ad_cm, outdir, refseq, geneList, againstList, data, corMethod
    geneList = gl
    againstList = agl
    corMethod = cm
    if not corMethod == 'pr' and not corMethod == 'kt' and not corMethod == 'bc':
        print(f"\ncorMethodError: Incorrect correlation measure suplied\nCheck -cm <option>, it should be one of [pr, kt or bc] and not {corMethod}\n")
        exit()
    # refering the output directory - and creating cor_gene sub-directory
    newSubDir = Path(workDir)/"cor_genes"
    Path(newSubDir).mkdir(exist_ok=True, parents=True)
    outdir = str(newSubDir)
    # Determining chunkSize i.e., number of genes to send in each CPU and is determined by length of the list over number of threads. 
    chunkSize = round(len(geneList)/threads)
    # Read the h5ad file 
    h5ad_cm2 = sc.read_h5ad(str(h5file))
    h5ad_cm = h5ad_cm2[:, againstList].copy()
    # Read the Biomart gene annotations
    refseq = pd.read_csv(str(annotations))
    # determine the data based on either dense matrix or sparse matrix 
    try:
        data = h5ad_cm.X.toarray()
    except AttributeError:
        data = h5ad_cm.X
    
    # Check for the correlation method
    if corMethod == 'bc':
        bayesian_cor(data, geneList, h5ad_cm.copy(), outdir, refseq, workDir, fileBase)
    else:
        # Create chunks of list using the chunk size 
        clist = list(chunkifyList(geneList, int(chunkSize)))
        # Print statement to display number of threads specified to use
        if threads >= 2:
            print(f"\nEntering parallel mode with {threads} CPU's.\n")
            print(f"With chunk size of {chunkSize}, {len(clist)} chunks are created\n")
    
        # Ignore numpy error 
        np.seterr(divide = 'ignore')
    
        # Core of parallel processing 
        with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as executor:
            future = [executor.submit(coex_fun, i, data, outdir, refseq, againstList, corMethod, h5ad_cm) for i in clist]

        # Reset to default warning - numpy error 
        np.seterr(divide = 'warn')
        brooklyn_endTime = time.perf_counter()
        print(f'\nThe brooklyn_arch execution is completed in {abs(round(brooklyn_start-brooklyn_endTime, 4))} second(s)\n')
    return True 

