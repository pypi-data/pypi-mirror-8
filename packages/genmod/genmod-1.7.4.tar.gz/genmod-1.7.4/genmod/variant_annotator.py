#!/usr/bin/env python
# encoding: utf-8
"""
variant_annotator.py

Annotates variants.

Creates batches and put them into a queue object.
The batches are dictionary objects with overlapping features where the feature id:s are keys and the values are dictionarys with variants.


Batch = {feature_1_id:{variant_1_id:variant_1_info, variant_2_id: variant_2_info}, feature_2_id:... }   

Created by Måns Magnusson on 2014-03-17.
Copyright (c) 2014 __MyCompanyName__. All rights reserved.
"""

from __future__ import print_function, unicode_literals

import sys
import os
import argparse
from datetime import datetime
from codecs import open
import genmod
try:
    import cPickle as pickle
except:
    import pickle

from pprint import pprint as pp

from interval_tree import interval_tree


class VariantAnnotator(object):
    """Creates parser objects for parsing variant files"""
    def __init__(self, variant_parser, batch_queue, gene_trees={}, exon_trees={}, phased=False, 
                    vep=False, whole_genes=False, verbosity=False):
        super(VariantAnnotator, self).__init__()
        self.variant_parser = variant_parser
        self.batch_queue = batch_queue
        self.individuals = self.variant_parser.individuals
        self.verbosity = verbosity
        self.phased = phased
        self.vep = vep
        self.whole_genes = whole_genes
        self.gene_trees  = gene_trees
        self.exon_trees = exon_trees
        self.chromosomes = []
        self.interesting_so_terms = set(
            ['transcript_ablation',
            'splice_donor_variant',
            'splice_acceptor_variant',
            'stop_gained',
            'frameshift_variant',
            'stop_lost',
            'initiator_codon_variant',
            'inframe_insertion',
            'inframe_deletion',
            'missense_variant',
            'transcript_amplification',
            'splice_region_variant',
            'incomplete_terminal_codon_variant',
            'synonymous_variant',
            'stop_retained_variant',
            'coding_sequence_variant']
        )
        
    
    def annotate(self):
        """Start the parsing"""
        beginning = True
        batch = {}
        new_chrom = None
        current_chrom = None
        current_features = []
        haploblock_id = 1
        # Haploblocks is a dictionary with list of lists like {ind_id:[[start, stop, id],[start, stop,id],...], ...}
        haploblocks = {ind_id:[] for ind_id in self.individuals}
        nr_of_batches = 0
        # Parse the vcf file:
        if self.verbosity:
            start_parsing_time = datetime.now()
            start_chrom_time = start_parsing_time
            start_twenty_time = start_parsing_time
            if self.batch_queue.full():
                genmod.warning('Queue full!!')
        
        nr_of_variants = 0
        nr_of_comp_cand = 0
        
        for variant in self.variant_parser:
            
            self.annotate_variant(variant)
            new_chrom = variant['CHROM']
            nr_of_variants += 1
            if variant['comp_candidate']:
                nr_of_comp_cand += 1
            
            new_features = variant['Annotation']
            
            if self.verbosity:
                if nr_of_variants % 20000 == 0:
                    print('%s variants parsed!' % nr_of_variants)
                    print('Last 20.000 took %s to parse.\n' % str(datetime.now() - start_twenty_time))
                    start_twenty_time = datetime.now()
            
            # If we look at the first variant, setup boundary conditions:
            if beginning:
                current_features = new_features
                beginning = False
                # Add the variant to each of its features in a batch
                batch = self.add_variant(batch, variant)
                current_chrom = new_chrom
                batch['haploblocks'] = {}
                if self.phased:
                    haploblock_starts = {ind_id:int(variant['POS']) for ind_id in self.individuals}
            else:
                # If we should put the batch in the queue:
                send = True
                
                if self.phased:
                    for ind_id in self.individuals:
                        #A new haploblock is indicated by '/' if the data is phased
                        if '/' in variant.get(ind_id, './.'):
                        #If call is not passed we consider it to be on same haploblock(GATK recommendations)
                            if variant.get('FILTER', '.') == 'PASS':
                                haploblocks[ind_id].append([haploblock_starts[ind_id], int(variant['POS']) - 1,
                                                             str(haploblock_id)])
                                haploblock_id += 1
                                haploblock_starts[ind_id] = int(variant['POS'])
                
            # Check if we are in a space between features:
                if len(new_features) == 0:
                    if len(current_features) == 0:
                        send = False
            #If not check if we are in a region with overlapping genes
                elif len(new_features.intersection(current_features)) > 0:
                    send = False
                
                if new_chrom != current_chrom:
                    self.chromosomes.append(current_chrom)
                    # New chromosome means new batch
                    send = True
                    current_chrom = new_chrom
                    
                    if self.verbosity:
                        print('Chromosome %s parsed!' % current_chrom)
                        print('Time to parse chromosome %s' % str(datetime.now()-start_chrom_time))
                        start_chrom_time = datetime.now()
                
                # If we are in a large intergenic region we limit the batch size to 10000
                if len(new_features) == 0 and len(batch) > 10000:
                    send = True
                
                if send:
                    if self.phased:
                    # Create an interval tree for each individual with the phaing intervals 
                        for ind_id in self.individuals:
                            #Check if we have just finished an interval
                            if haploblock_starts[ind_id] != int(variant['POS']):                                        
                                haploblocks[ind_id].append([haploblock_starts[ind_id], int(variant['POS']), 
                                                            str(haploblock_id)])
                                haploblock_id += 1
                            batch['haploblocks'][ind_id] = interval_tree.IntervalTree(haploblocks[ind_id], 
                                                haploblocks[ind_id][0][0]-1, haploblocks[ind_id][-1][1]+1)
                        haploblocks = {ind_id:[] for ind_id in self.individuals}
                    # Put the job in the queue
                    self.batch_queue.put(batch)
                    nr_of_batches += 1
                    #Reset the variables
                    current_features = new_features
                    batch = self.add_variant({}, variant)
                    batch['haploblocks'] = {}
                else:
                    current_features = current_features.union(new_features)
                    batch = self.add_variant(batch, variant) # Add variant batch
        
        self.chromosomes.append(current_chrom)
        
        if self.verbosity:
            print('Chromosome %s parsed!' % current_chrom)
            print('Time to parse chromosome %s \n' % str(datetime.now()-start_chrom_time))
            print('Variants parsed!')
            print('Time to parse variants:%s' % str(datetime.now() - start_parsing_time))
            print('Number of variants in variant file:%s' % nr_of_variants)
        
        if self.phased:
        # Create an interval tree for each individual with the phasing intervals
            for ind_id in self.individuals:
                #check if we have just finished an interval
                if haploblock_starts[ind_id] != int(variant['POS']):
                    haploblocks[ind_id].append([haploblock_starts[ind_id], int(variant['POS']), str(haploblock_id)])
                    haploblock_id += 1
                try:
                    batch['haploblocks'][ind_id] = interval_tree.IntervalTree(haploblocks[ind_id], 
                                                haploblocks[ind_id][0][0]-1, haploblocks[ind_id][-1][1]+1)
                except IndexError:
                    pass
        
        self.batch_queue.put(batch)
        nr_of_batches += 1
        
        return nr_of_batches
    
    def add_variant(self, batch, variant):
        """Adds the variant to the proper gene(s) in the batch."""
        # We need to make this construction since there can be multiple alternatives:
        variant_id = variant['variant_id']
        # If we are in a region between features:
        batch[variant_id] = variant
        
        return batch
    
    def check_vep_annotation(self, variant):
        """Return a set with the genes that vep has annotated this variant with.
            
            Input: A variant
            
            Returns: A set with genes"""
        
        annotation = set()
        # vep_info is a dictionary with genes as key and annotation as values
        for gene in variant.get('vep_info',{}):
            for consequence in variant['vep_info'][gene].get('Consequence', '').split('&'):
                if consequence in self.interesting_so_terms:
                    annotation.add(gene)
        
        return annotation
        
    
    def annotate_variant(self, variant):
        """Annotate variants with what regions the belong.
            Adds 'Annotation' = set(set, of, genes)
            and 'compound_candidate' = Boolean
            to variant dictionary
            
            Input: variant_dictionary
            
            Returns: variant_dictionary with annotation added
            
        """
        
        variant['comp_candidate'] = False
        variant['Annotation'] = set()
        
        variant_chrom = variant['CHROM'].lstrip('chr')
        alternatives = variant['ALT'].split(',')
        # When checking what features that are overlapped we use the longest alternative
        longest_alt = max([len(alternative) for alternative in alternatives])
        # Internally we never use 'chr' in the chromosome names:
        variant_position = int(variant['POS'])
        
        variant_interval = [variant_position, (variant_position + longest_alt-1)]
        
        #If annotated with vep we do not need to check interval trees
        if self.vep:
            
            variant['Annotation'] = self.check_vep_annotation(variant)
        
        else:
            
            try:
                variant['Annotation'] = set(self.gene_trees[variant_chrom].find_range(variant_interval))
                
            except KeyError:
                if self.verbosity:
                    genmod.warning(''.join('Chromosome', variant_chrom, 'is not in annotation file!'))
        
        if self.whole_genes:
            # If compounds are to be checked in whole genes (including introns):
            if len(variant['Annotation']) > 0:
                variant['comp_candidate'] = True
        else:
            #Check if exonic:
            try:
                if len(self.exon_trees[variant_chrom].find_range(variant_interval)):
                    variant['comp_candidate'] = True
            except KeyError:
                if self.verbosity:
                    genmod.warning(''.join('Chromosome', variant_chrom, 'is not in annotation file!'))
                    
        return

def main():
    from multiprocessing import JoinableQueue
    from vcf_parser import vcf_parser
    parser = argparse.ArgumentParser(description="Parse different kind of pedigree files.")
    parser.add_argument('variant_file', 
                            type=str, nargs=1, 
                            help='A file with variant information.'
    )
    parser.add_argument('-an', '--annotation_file', 
                            type=str, nargs=1, 
                            help='A file with feature annotations.'
    )
    parser.add_argument('-at', '--annotation_type', 
                            type=str, nargs=1,default=['gene_pred'], 
                            choices=['gene_pred', 'bed', 'gtf', 'ccds'], 
                            help='Specify annotation type.'
    )
    parser.add_argument('-phased', '--phased', 
                            action="store_true", 
                            help='If variant file is phased.'
    )
    parser.add_argument('-gene', '--whole_gene', 
                            action="store_true", 
                            help='If whole genes shall be checked for compounds.'
    )
    parser.add_argument('-v', '--verbose', 
                            action="store_true", 
                            help='Increase output verbosity.'
    )
    parser.add_argument('-vep', '--vep', 
                            action="store_true", 
                            help='If variants are annotated with vep.'
    )
    
    args = parser.parse_args()
    infile = args.variant_file[0]
    
    gene_trees = {}
    exon_trees = {}
    
    my_vcf_parser = vcf_parser.VCFParser(infile)
    if not args.vep:
        if args.annotation_file:
            anno_file = args.annotation_file[0]
            if args.verbose:
                print('Parsing annotationfile...')
                start_time_annotation = datetime.now()
            file_name, file_extension = os.path.splitext(anno_file)
            zipped = False
            if file_extension == '.gz':
                zipped = True
                file_name, file_extension = os.path.splitext(file_name)
            
            my_anno_parser = annotation_parser.AnnotationParser(anno_file, args.annotation_type[0], zipped=zipped)
            gene_trees = my_anno_parser.gene_trees
            exon_trees = my_anno_parser.exon_trees
            if args.verbose:
                print('annotation parsed. Time to parse annotation: %s\n' % str(datetime.now() - start_time_annotation))
        else:
            annopath = os.path.join(os.path.split(os.path.dirname(genmod.__file__))[0], 'annotations/')
            gene_db = os.path.join(annopath, 'genes.db')
            exon_db = os.path.join(annopath, 'exons.db')
        
            try:
                with open(gene_db, 'rb') as f:
                    gene_trees = pickle.load(f)
                with open(exon_db, 'rb') as g:
                    exon_trees = pickle.load(g)
            except FileNotFoundError:
                print('You need to build annotations! See documentation.')
                pass
            
        
    # print(my_head_parser.__dict__)
    variant_queue = JoinableQueue()
    start_time = datetime.now()        
    my_anno_parser = VariantAnnotator(my_vcf_parser, variant_queue, args, gene_trees, exon_trees)
    nr_of_batches = my_anno_parser.annotate()
    for i in range(nr_of_batches):
        variant_queue.get()
        variant_queue.task_done()
    
    variant_queue.join()
    if args.verbose:
        print('Time to parse variants: %s ' % str(datetime.now()-start_time))

if __name__ == '__main__':
    main()
