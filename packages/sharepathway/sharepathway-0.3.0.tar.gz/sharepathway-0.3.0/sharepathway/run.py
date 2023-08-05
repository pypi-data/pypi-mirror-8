# -*- coding: utf-8 -*-
from itertools import chain, groupby
from collections import defaultdict
import pickle
import numpy as np

from .enrichment import enrichment
from .geneIDconv import geneIDconv
from .genes2mat import genes2mat
from .linkpath2mat import linkpath2mat
from .out2html import out2html
from .parse_kegg import Request

def Run(*args, **kwargs):

    species = kwargs.get('species', 'hsa') #default: 'hsa'
    filein = kwargs.get('fi')
    fileout = kwargs.get('fo')

    fileout = fileout+'.html'
    ratio = kwargs.get('r',0.01)
    # parse gene lists into matrix
    KGID = geneIDconv(species=species)
    [Genes, genelists, GenesMat] = genes2mat(filein,KGID)
    # load KEGG data
    data=Request('link','path',species)
    pwid2name = Request('list','pathway',species)
    # parse KEGG into matrix
    [Pathways, pathwaycount, pathwayMat] = linkpath2mat(Genes, data)
    enrich = enrichment(GenesMat, pathwayMat)
    result = out2html(GenesMat, pathwayMat,enrich,Genes,Pathways,genelists,pathwaycount,ratio,fileout, pwid2name)
