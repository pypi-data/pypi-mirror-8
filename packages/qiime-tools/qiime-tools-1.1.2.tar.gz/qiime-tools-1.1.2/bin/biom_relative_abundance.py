#!/usr/bin/env python

from __future__ import division
import argparse
from collections import defaultdict
import json

from qiime_tools import otu_calc as oc


def write_relative_abundance(biom, out_fn, sort_by=None):
    """
    Given a BIOM table, calculate per-sample relative abundance for 
    each OTU and write out to a tab-separated file listing OTUs as
    rows and Samples as columns.
    :@type biom: dict (translated json string)
    :@param biom: BIOM-formatted OTU/Sample abundance data
    :@type out_fn: str
    :@param out_fn: The full path to the desired output file.
    :@type sort_by: function
    :@param sort_by: A function acting as a sorting key that will determine
                     the order in which the Sample IDs appear as columns in
                     the output file.
    """
    rel_abd = oc.relative_abundance(biom)
    
    with open(out_fn, 'w') as out_f:
        sids = sorted(set([col['id'] for col in biom['columns']]), key=sort_by)
        out_f.write('#OTU ID\t{}\n'.format('\t'.join(sids)))
        for row in biom['rows']:
            otuName = oc.otu_name_biom(row)
            sabd = [str(rel_abd[otuName][sid]) if sid in rel_abd[otuName] else '0' for sid in sids]
            out_f.write('{}\t{}\n'.format(otuName, '\t'.join(sabd)))


def handle_program_options():
    parser = argparse.ArgumentParser(description="Convert a BIOM file of OTU abundance \
                                                  data into a TSV file of relative \
                                                  abundance data.")
    parser.add_argument('-i', '--input_biom_fp',
                        help="The BIOM file path.")
    parser.add_argument('-o', '--output_tsv_fp', default='relative_abundance.tsv',
                        help="A TSV table of relative OTU abundance data.")
    
    return parser.parse_args()


def main():
    args = handle_program_options()
    
    with open(args.input_biom_fp, 'rU') as in_f:
        biom = json.load(in_f)
        write_relative_abundance(biom, args.output_tsv_fp)
    
if __name__ == '__main__':
    main()
