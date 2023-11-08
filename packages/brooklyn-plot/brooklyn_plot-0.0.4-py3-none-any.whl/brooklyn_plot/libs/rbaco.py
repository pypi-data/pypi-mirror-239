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

def summary_baco(req_baycor_matt, query_genes, biomart, workDir, fileBase):
    gene_list = req_baycor_matt.columns.to_list()
    newdf = list()
    new_emptyList = list()
    for i in gene_list[1:len(gene_list)]:
        tempdf_sorted = req_baycor_matt.sort_values(i, ascending=False)
        tempdf_sorted2 = tempdf_sorted[tempdf_sorted[i] > 0].iloc[1:51][['chromo', i]]
        chr_nu = query_genes[i]
        denominator = int(tempdf_sorted2.shape[0])
        try:
            occurence = int(tempdf_sorted2['chromo'].value_counts()[chr_nu])
            #occurence = int(df_2['chromosome_name'].value_counts()[req_chr])
        except KeyError:
            occurence = 0
        if denominator > 0:
            percent_occurence = str(round((occurence / denominator) * 100,2))
        else:
            percent_occurence = "0"
        df_1 = tempdf_sorted2.iloc[:1,:]
        base_r2 = (df_1.values.tolist())
        r2 = base_r2[0][1]
        base = biomart.loc[biomart['gene_ids']==i].values.tolist()[0]
        newbase = base + [r2] + [str(occurence), str(denominator), percent_occurence]
        new_emptyList.append(newbase)
    newColOrder = ['gene', 'r', 'hgnc_symbol','chromosome_name', 'start_position', 'xMean', 'end_position', 'band', 'occurence', 'denominator', 'percent_occurence']
    summarizedDF = pd.DataFrame(new_emptyList, columns = ['gene', 'xMean', 'start_position', 'end_position', 'chromosome_name', 'hgnc_symbol', 'band', 'r', 'occurence', 'denominator', 'percent_occurence'])
    brookSum = Path(workDir)/str(str(fileBase) + "_summary.csv")
    brookSumSorted = Path(workDir)/str(str(fileBase) + "_sorted_summary.csv")
    summarizedDF = summarizedDF.round(decimals = 2)
    summarizedDF_ordered = summarizedDF[newColOrder]
    summarizedDF_ordered.to_csv(brookSum, index=False)
    df2 = summarizedDF_ordered

    # Create chromosome order and sort accordingly
    chrOrder = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X', 'Y', 'M', 'MT']
    chrIndex = dict(zip(chrOrder, range(len(chrOrder)))) # Creates a dictionary of chromosomes and a serial number as value
    df2 = df2[df2['chromosome_name'].notna()] # Filter out any rows which don't represent any chromosomes (such as blank lines at the EOF)
    df2['chromosome_name'] = df2['chromosome_name'].astype('string') # Making sure the column chromosome name is a string data type
    df2 = df2.loc[df2['chromosome_name'].isin(chrOrder)] # Check for only chromosomes and avoid any patches
    df2['ChrOrder'] = df2['chromosome_name'].map(chrIndex) # Creating a new column chrOrder which defines the order of each chromosomes.
    df2['ChrOrder'] = df2['ChrOrder'].astype('int') # Making sure the column chrOrder is a integer
    df2.sort_values(['ChrOrder', 'end_position'], ascending = True, inplace = True) # Sort based on chromosome order and end position of each gene
    df2.drop(columns='ChrOrder', inplace = True) # Drop column chromosome order which is no longer required
    df2.to_csv(brookSumSorted, index=False) # Write the sorted dataframe to a CSV file



def bayesian_cor(data, geneList, h5ad_cm, outdir, biomart, workDir, fileBase):
    from rpy2 import robjects
    import rpy2.robjects as ro
    from rpy2.robjects.conversion import localconverter
    from rpy2.robjects import pandas2ri
    import rpy2.robjects.numpy2ri as numpy2ri
    Baco = robjects.r('''
        function(X){
            alpha0 <- rep(1/nrow(X),ncol(X))
            beta0=1-alpha0
            nrowsX <- nrow(X)
            k <- ncol(X)
            cs <- colSums(X)
            alphas <- alpha0 + X
            betas  <- matrix(rep(beta0,nrowsX), nrow=nrowsX, byrow=TRUE) + matrix(rep(cs,nrowsX), nrow=nrowsX, byrow=TRUE) - X
            alphasPLUSbetas <- alphas + betas
            Psi <- alphas/alphasPLUSbetas - matrix(rep(rowSums(alphas/alphasPLUSbetas)/k, k), ncol=k, byrow=FALSE)
            var_vec <- as.matrix( ( rowSums( (alphas*betas)/( (alphasPLUSbetas^2)*(alphasPLUSbetas+1) ) ) + rowSums(Psi^2) )/k )
            cov_mtrx <- (Psi %*% t(Psi))/k
            Bcorrvals <- cov_mtrx / sqrt( var_vec %*% t(var_vec) )
            diag(Bcorrvals) <- 1
            Bcorrvals
        }
    ''')
    data2 = np.transpose(data)
    with localconverter(ro.default_converter + numpy2ri.converter + pandas2ri.converter):
        rdata = ro.conversion.py2rpy(data2)

    z = Baco(rdata)

    a_results = np.array(z)
    b_results = pd.DataFrame(a_results) # This will be 3500 x 3500 matrix of Bayesian correlation
    b_results.columns = h5ad_cm.var_names.tolist()
    b_results.index = h5ad_cm.var_names.tolist()
    baycor_matt = b_results.loc[:, b_results.columns.isin(geneList)]
    query_genes =  pd.Series(biomart.chromosome_name.values,index=biomart.gene_ids).to_dict()
    col_order = ['chromo']
    col_order.extend(geneList)
    #col_order.extend(baycor_matt.columns.tolist())
    #baycor_matt['chromo'] = baycor_matt.index.to_series().map(query_genes)
    #baycor_matt['chromo'] = baycor_matt.index.map(query_genes)
    #baycor_matt.loc['chromo'] = baycor_matt.index.map(mapper=(lambda x: query_genes[x]))
    #baycor_matt['chromo'] = baycor_matt.apply(lambda x: query_genes.get(x,x))
    baycor_matt['chromo'] = baycor_matt.index.map(query_genes)
    req_baycor_matt = baycor_matt[col_order]
    #c_results = b_results[geneList]
    outname = outdir + "/bayesian_correlation.csv"
    req_baycor_matt.index.name = "gene_ids"
    req_baycor_matt.to_csv(outname)
    
    # Summarize it here
    summary_baco(req_baycor_matt, query_genes, biomart, workDir, fileBase)
