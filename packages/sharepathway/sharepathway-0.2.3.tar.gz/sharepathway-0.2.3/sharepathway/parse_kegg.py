# -*- coding: utf-8 -*-
from itertools import chain, groupby
from collections import defaultdict
import pickle
import urllib2

''' Use NCBI-geneid as internal id '''

def Request(*args, **kwargs):
    """return and save the blob of data that is returned
    from kegg without caring to the format"""
    downloaded = kwargs.get('force', False)
    save = kwargs.get('force', True)

    # so you can copy paste from kegg
    '''URL form
        http://rest.kegg.jp/<operation>/<argument>/<argument2 or option>

        <operation> = info | list | find | get | conv | link
        <argument> = <database> | <dbentries>
    '''
    args = list(chain.from_iterable(a.split('/') for a in args))
    args = [a for a in args if a]
    request = 'http://rest.kegg.jp/' + "/".join(args)
    print("KEGG API: " + request)
    filename = "KEGG_" + "_".join(args)
    try:
        if downloaded:
            raise IOError()
        print("loading the cached file " + filename)
        with open(filename, 'r') as f:
            data = pickle.load(f)
    except IOError:
        print("downloading the library,it may take some time")
        try:
            req = urllib2.urlopen(request)
            data = req.read()
            data = [tuple(d.split('\t')) for d in data.split('\n')][:-1]
            if save:
                with open(filename, 'w') as f:
                    print("saving the file to " + filename)
                    pickle.dump(data, f)
        # clean the error stacktrace
        except urllib2.HTTPError as e:
            raise e
    return data


def Parse_KEGG(*args, **kwargs):
    species = kwargs.get('species', 'hsa') #default: 'hsa'
    data=Request('link','path',species)
    return data
