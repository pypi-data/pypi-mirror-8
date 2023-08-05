#!/usr/bin/env python
# encoding: utf-8
"""
variant_consumer.py

Class that takes a list of objects and return all unordered pairs as a generator.

If only one object? Raise Exception
 
Created by Måns Magnusson on 2013-03-01.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import multiprocessing
import sqlite3
import operator
from functools import reduce
from math import log10
from pysam import Tabixfile, asTuple

from pprint import pprint as pp

from genmod import genetic_models, warning

class VariantConsumer(multiprocessing.Process):
    """Yeilds all unordered pairs from a list of objects as tuples, like (obj_1, obj_2)"""
    
    def __init__(self, task_queue, results_queue, family=None, phased=False, vep=False, cadd_raw=False,
                    cadd_file=None, cadd_1000g=None, cadd_ESP=None, cadd_InDels=None, 
                    thousand_g=None, chr_prefix=False, strict=False, verbosity=False):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.family = family
        self.results_queue = results_queue
        self.verbosity = verbosity
        self.phased = phased
        self.vep = vep
        self.cadd_raw = cadd_raw
        self.cadd_file = cadd_file
        self.cadd_1000g = cadd_1000g
        self.cadd_ESP = cadd_ESP
        self.cadd_InDels = cadd_InDels
        self.thousand_g = thousand_g
        self.chr_prefix = chr_prefix
        self.strict = strict
        if self.cadd_file:
            self.cadd_file = Tabixfile(self.cadd_file)
        if self.cadd_1000g:
            self.cadd_1000g = Tabixfile(self.cadd_1000g)
        if self.cadd_ESP:
            self.cadd_ESP = Tabixfile(self.cadd_ESP)
        if self.cadd_InDels:
            self.cadd_InDels = Tabixfile(self.cadd_InDels)
        if self.thousand_g:
            self.thousand_g = Tabixfile(self.thousand_g)
        
        
    def fix_variants(self, variant_batch):
        """Merge the variants into one dictionary, make shure that the compounds are treated right."""
        fixed_variants = {} # dict like {variant_id:variant, ....}
        for feature in variant_batch:
            for variant_id in variant_batch[feature]:
                if variant_id in fixed_variants:
                    # We need to add compound information from different features
                    if len(variant_batch[feature][variant_id].get('Compounds', [])) > 0:
                        fixed_variants[variant_id]['Compounds'] = (
                         dict(list(variant_batch[feature][variant_id]['Compounds'].items()) +
                                    list(fixed_variants[variant_id]['Compounds'].items())))
                else:
                    fixed_variants[variant_id] = variant_batch[feature][variant_id]
        
        return fixed_variants
    
    
    def get_model_score(self, individuals, variant):
        """Return the model score for this variant."""
        model_score = None
        genotype_scores = []
        
        for individual in individuals:
            gt_call = variant['genotypes'].get(individual, None)
            if gt_call:
                if gt_call.genotype_quality > 0:
                    genotype_scores.append(10**-(float(gt_call.genotype_quality)/10))
        if len(genotype_scores) > 0:
            model_score = (str(round(-10*log10(1-reduce(operator.mul, [1-score for score in genotype_scores])))))
        
        return model_score
    
    def get_cadd_score(self, tabix_reader, chrom, start, alt=None):
        """Return the record from a cadd file."""
        score = None
        # CADD values are only for snps:
        cadd_key = int(start)
        try:
            for record in tabix_reader.fetch(str(chrom), cadd_key-1, cadd_key):
                record = record.split('\t')
                if record[3] == alt:
                    #We need to send both cadd values
                    return (record[-1], record[-2])
        except (IndexError, KeyError, ValueError) as e:
            pass
        
        return score
    
    def add_cadd_score(self, variant):
        """Add the CADD relative score to this variant."""
        cadd_score = None
        cadd_relative_scores = []
        cadd_absolute_scores = []
        #Check CADD file(s):
        for alt in variant['ALT'].split(','):
            if self.cadd_file:
                cadd_score = self.get_cadd_score(self.cadd_file, variant['CHROM'], 
                                                variant['POS'], alt)
            # If variant not found in big CADD file check the 1000G file:
            if not cadd_score and self.cadd_1000g:
                cadd_score = self.get_cadd_score(self.cadd_1000g, variant['CHROM'], variant['POS'], alt)
            
            if not cadd_score and self.cadd_ESP:
                cadd_score = self.get_cadd_score(self.cadd_ESP, variant['CHROM'], variant['POS'], alt)
            
            if not cadd_score and self.cadd_ESP:
                cadd_score = self.get_cadd_score(self.cadd_ESP, variant['CHROM'], variant['POS'], alt)
            
            if not cadd_score and self.cadd_ESP:
                cadd_score = self.get_cadd_score(self.cadd_ESP, variant['CHROM'], variant['POS'], alt)
            
            if cadd_score:
                cadd_relative_scores.append(str(cadd_score[0]))
                cadd_absolute_scores.append(str(cadd_score[1]))
        
        if len(cadd_relative_scores) > 0:
            variant['CADD'] = ','.join(cadd_relative_scores)
            if self.cadd_raw:
                variant['CADD_raw'] = ','.join(cadd_absolute_scores)
        return

    def get_thousandg_freq(self, tabix_reader, chrom, start, alt):
        """Return the record from a cadd file."""
        freq = None
        # CADD values are only for snps:
        cadd_key = int(start)
        try:
            for record in tabix_reader.fetch(str(chrom), cadd_key-1, cadd_key):
                record = record.split('\t')
                i = 0
                #We can get multiple rows so need to check each one
                #We also need to check each one of the alternatives per row
                for alternative in record[4].split(','):
                    if alternative == alt:
                        for info in record[7].split(';'):
                            info = info.split('=')
                            if info[0] == 'AF':
                                frequencies = info[-1].split(',')
                                return frequencies[i]
                    i += 1
                
        except (IndexError, KeyError, ValueError) as e:
            pass
        
        return freq
    
    def add_frequency(self, variant):
        """Add the thousand genome frequency if present."""
        #Check 1000G frequency:
        thousand_g_freq = self.get_thousandg_freq(self.thousand_g, 
                            variant['CHROM'], variant['POS'], variant['ALT'].split(',')[0])
        if thousand_g_freq:
                variant['1000GMAF'] = thousand_g_freq
        return
    
    
    def make_print_version(self, variant_dict):
        """Get the variants ready for printing"""
        for variant_id in variant_dict:
            variant = variant_dict[variant_id]
            
            if self.chr_prefix:
                variant['CHROM'] = 'chr'+variant_dict[variant_id]['CHROM']
            
            vcf_info = variant_dict[variant_id]['INFO'].split(';')
            
            #Remove the 'Genotypes' post since we will not need them for now
            
            feature_list = variant_dict[variant_id].get('Annotation', [])
            
            if 'Compounds' not in variant['info_dict']:
            
                if len(variant_dict[variant_id].get('Compounds', [])) > 0:
                    #We do not want reference to itself as a compound:
                    variant_dict[variant_id]['Compounds'].pop(variant_id, None)
                    compounds_list = list(variant_dict[variant_id]['Compounds'].keys())
                    vcf_info.append('Compounds=' + ','.join(compounds_list))
            
            # Check if any genetic models are followed
            if 'GeneticModels' not in variant['info_dict']:
                
                model_list = []
                for model in variant_dict[variant_id].get('Inheritance_model',[]):
                    if variant_dict[variant_id]['Inheritance_model'][model]:
                        model_list.append(model)
                if len(model_list) > 0:
                    vcf_info.append('GeneticModels=' + ','.join(model_list))
                    model_score = self.get_model_score(self.family.individuals, variant_dict[variant_id])
                    if model_score:
                        if float(model_score) > 0:
                            vcf_info.append('ModelScore=' +  model_score)
            
            # We only want to include annotations where we have a value
            
            if not self.vep:
                if 'Annotation' not in variant['info_dict']:
                    if len(feature_list) != 0 and feature_list != ['-']:
                        vcf_info.append('Annotation=' + ','.join(feature_list))
            
            if variant.get('CADD', None):
                if 'CADD' not in variant['info_dict']:
                    vcf_info.append('CADD=%s' % str(variant.pop('CADD', '.')))
            
            if self.cadd_raw:
                if 'CADD_raw' not in variant['info_dict']:
                    if variant.get('CADD_raw', None):
                        vcf_info.append('CADD_raw=%s' % str(variant.pop('CADD_raw', '.')))
            
            if variant.get('1000GMAF', None):
                if '1000GMAF' not in variant['info_dict']:
                    vcf_info.append('1000GMAF=%s' % str(variant.pop('1000GMAF', '.')))
            
            variant_dict[variant_id]['INFO'] = ';'.join(vcf_info)
            
        return
    
    def run(self):
        """Run the consuming"""
        proc_name = self.name
        if self.verbosity:
            print('%s: Starting!' % proc_name)
        while True:
            # A batch is a dictionary on the form {gene:{variant_id:variant_dict}}
            next_batch = self.task_queue.get()
            # if self.verbosity:
                # if self.results_queue.full():
                #     print('Batch results queue Full! %s' % proc_name)
                # if self.task_queue.full():
                #     print('Variant queue full! %s' % proc_name)
            if next_batch is None:
                self.task_queue.task_done()
                if self.verbosity:
                    print('%s: Exiting' % proc_name)
                break
            
            
            if self.family:
                genetic_models.check_genetic_models(next_batch, self.family, self.verbosity, 
                                                    self.phased, self.strict, proc_name)
            # Make shure we only have one copy of each variant:
            fixed_variants = self.fix_variants(next_batch)
            
            for variant_id in fixed_variants:
                if self.cadd_file or self.cadd_1000g:
                    self.add_cadd_score(fixed_variants[variant_id])
                if self.thousand_g:
                    self.add_frequency(fixed_variants[variant_id])
            
            # Now we want to make versions of the variants that are ready for printing.
            self.make_print_version(fixed_variants)
            self.results_queue.put(fixed_variants)
            self.task_queue.task_done()
        return
        
    

def main():
    pass

if __name__ == '__main__':
    main()