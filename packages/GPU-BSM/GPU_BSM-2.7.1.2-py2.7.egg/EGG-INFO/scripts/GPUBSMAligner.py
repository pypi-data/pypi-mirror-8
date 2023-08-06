
# This file is part of GPU-BSM.

# GPU-BSM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GPU-BSM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GPU-BSM.  If not, see <http://www.gnu.org/licenses/>.


# GPU-BSM is a GPU based program to map bisulfite treated reads
# rel. 2.7.1 2014-10-20
#
# contact andrea.manconi@itb.cnr.it

import ntpath
import fileinput
import string
import os
import time 
import shelve
import subprocess
import random
import math
import logging
import sys
import pickle 
import marshal
import shutil
import threading
from subprocess import Popen
from utilities import *
from multiprocessing import Process#, Queue
from multiprocessing import Manager
from itertools import groupby, count

#from Queue import Queue


def parse_cigar(cigar):
    '''
    to calculate the overall indels
    '''
    cigar_op = 'MIDNSHP=X'
    p_cigar_op = dict([(j, cigar[j]) for j in range(len(cigar)) if cigar[j] in cigar_op])

    operators = {'M': list(), 'I': list(), 'D': list()}
    i = 0
    for j in sorted(p_cigar_op.iterkeys()):
        slice_size = int(cigar[i:j])
        i = j+1
        if p_cigar_op[j]=='I': operators['I'].append(slice_size)
        elif p_cigar_op[j]=='D': operators['D'].append(slice_size)
        else: operators['M'].append(slice_size)
    return operators

def alignment_score(cigar, edit_distance):
    '''
    Calculate the alignment score
    '''

    # MatchScore defines the score for match
    MatchScore=1
    # MismatchScore defines the score for mismatch
    MismatchScore=-2
    # GapOpenScore defines the score for opening a gap
    GapOpenScore=-3
    # GapExtendScore defines the score for extending a gap
    GapExtendScore=-1

    operators = parse_cigar(cigar)
    gaps_penalty = 0; mismatches_penalty = 0; matches_score = 0
    nb_of_gaps = 0; nb_of_mismatches = 0; nb_of_matches = 0

    seq_size = 0
    for op in ['I', 'D']:
        for gap in operators[op]:
            seq_size+=gap*(op=='I')
            nb_of_gaps+=gap
            gaps_penalty += GapOpenScore + (gap>1)*(gap-1)*GapExtendScore

    for item in operators['M']: seq_size+=item
    
    nb_of_mismatches = edit_distance - nb_of_gaps
    nb_of_matches = seq_size - edit_distance

    mismatches_penalty = nb_of_mismatches*MismatchScore
    matches_score = nb_of_matches*MatchScore

    return matches_score + mismatches_penalty + gaps_penalty

def get_alignments_single(fname, m, strand, all_valid):
    '''
    Get alignments performed by SOAP3-dp (for single-end alignments)
    '''

    edit_distances = {} # mismatches and indels
    positions = {}
    fname+='.out'
    started_alignments = False 
    for line in fileinput.input(fname):
        if not line.startswith('@'): #started_alignments=True
            data=line.split()
            if data[2]!='*': # the read has been aligned
		if not edit_distances.has_key(data[0]): edit_distances[data[0]]=dict(zip(range(m+1), (m+1)*[0]))
		ed = int(data[12].split(':')[-1]) # NM field in the SAM file: the edit distance (mismatches, indels and ambiguous bases)
                if not edit_distances[data[0]].has_key(ed): edit_distances[data[0]][ed]=0
                edit_distances[data[0]][ed]+=1
                if not positions.has_key(data[0]): positions[data[0]]=list()
                cigar = data[5]
                score = alignment_score(cigar, ed)
                strand_fa = {'0':'+', '1':'-'}[bin(int(data[1]))[2]] # bit 0x10
                positions[data[0]].append({'seq_id': data[2], 'position': int(data[3]), 'strand_fa':strand_fa, 'ed':ed, 'strand': strand, 'cigar': cigar, 'score': score})
		
		'''
                To take into account multiple alignments
		'''
                if all_valid:
		  if len(data)==20:
		    xa = data[19][5:] # remove XA:Z tag
		    xa = xa.split(';')[:-1]
		    if True:
		    #try:
		      for item in xa:
			item = item.split(',')
			seq_id = item[0]
			position = int(item[1])
			cigar = item[2]
			score = alignment_score(cigar, ed)
			positions[data[0]].append({'seq_id': seq_id, 'position': position, 'strand_fa':strand_fa, 'ed':ed, 'strand': strand, 'cigar': cigar, 'score': score})
		    #except: pass
		    
    fileinput.close()
    return edit_distances, positions

def get_alignments_paired(fname, m, strand, all_valid):
    '''
    Get alignments performed by SOAP3-dp (for paired-end alignments)
    '''

    edit_distances = {} # mismatches and indels
    positions = {}
    ed=list()
    fname+='.out'
    started_alignments = False 
    mate=0
    pairs_positions = list()
    read_aligned=[False, False]
    
    for line in fileinput.input(fname):
        if not line.startswith('@'): #started_alignments=True
        #if started_alignments:
	    data=line.split()
	    mate+=1
	    
	    if data[5]!="*": read_aligned[mate-1]=True
	    if mate==1 and read_aligned[mate-1]==True: 
	      ed.append(int(data[12].split(':')[-1])) # NM field in the SAM file: the edit distance (mismatches, indels and ambiguous bases)
	      cigar = data[5]
	      score = alignment_score(cigar, ed[mate-1])
	      strand_fa = {'0':'+', '1':'-'}[bin(int(data[1]))[2]] # bit 0x10
	      pairs_positions.append({'seq_id': data[2], 'position': int(data[3]), 'strand_fa':strand_fa, 'ed':ed, 'strand': strand, 'cigar': cigar, 'score': score})
	        
	    elif mate==2:
	      if read_aligned[0]==True and read_aligned[1]==True:
		ed.append(int(data[12].split(':')[-1])) # NM field in the SAM file: the edit distance (mismatches, indels and ambiguous bases)
		cigar = data[5]
		score = alignment_score(cigar, ed[mate-1])
		strand_fa = {'0':'+', '1':'-'}[bin(int(data[1]))[2]] # bit 0x10
		pairs_positions.append({'seq_id': data[2], 'position': int(data[3]), 'strand_fa':strand_fa, 'ed':ed, 'strand': strand, 'cigar': cigar, 'score': score})
	      
		
		if not edit_distances.has_key(data[0]): edit_distances[data[0]]=dict(zip(range(m+1), (m+1)*[0]))
		ed = max(ed)
		if not edit_distances[data[0]].has_key(ed): edit_distances[data[0]][ed]=0
		edit_distances[data[0]][ed]+=1
		if not positions.has_key(data[0]): positions[data[0]]=list()
		positions[data[0]].append({'seq_id': (pairs_positions[0]['seq_id'], pairs_positions[1]['seq_id']), 'position': (pairs_positions[0]['position'], pairs_positions[1]['position']), 'strand_fa': (pairs_positions[0]['strand_fa'], pairs_positions[1]['strand_fa']), 'ed':ed, 'strand': (pairs_positions[0]['strand'], pairs_positions[1]['strand']), 'cigar': (pairs_positions[0]['cigar'], pairs_positions[1]['cigar']), 'score': max(pairs_positions[0]['score'], pairs_positions[1]['score'])})
	      ed = list() 	
	      pairs_positions = list()
	      mate=0
	      read_aligned=[False, False]
	    '''
            To take into account multiple alignments
	    '''
	    if all_valid:
	      if len(data)==20:
		xa = data[19][5:] # remove XA:Z tag
		xa = xa.split(';')[:-1]
		try:
		  for item in xa:
		    item = item.split(',')
		    seq_id = item[0]
		    position = int(item[1])
		    cigar = item[2]
		    positions[data[0]].append({'seq_id': seq_id, 'position': position, 'strand_fa':strand_fa, 'ed':ed, 'strand': strand, 'cigar': cigar, 'score': score})
		except: pass
	    
	    
	    
    fileinput.close()
    return edit_distances, positions


def get_alignments(fname, m, strand, single_end, all_valid):
  if single_end: return get_alignments_single(fname, m, strand, all_valid)
  else: return get_alignments_paired(fname, m, strand, all_valid)

def remove_multi_best_score(edit_distances, alignments):
    '''
    Remove those reads with at least two best score alignments
    '''
    for read in alignments.keys():
        scores = [alignment['score'] for alignment in alignments[read]]
        best_score = max(scores)
        if scores.count(best_score)>1:
            del(edit_distances[read]); del(alignments[read])
        else: # no best alignments are discarded
            alignments[read]=[alignments[read][scores.index(best_score)]]
    return


def split_reads_files(reads_fnames, query_format, N=None):
    '''
    Split the data file(s) in files with up n reads
    '''
    fname = reads_fnames.items()[0][1]
    processes = list()
    p = subprocess.Popen(["wc", "-l", fname], stdout=subprocess.PIPE)
    out, err = p.communicate()
      
    if N!=None:
      n_lines=N
      if query_format=="Illumina GAII FastQ":n_lines = N*4
      chunks = int(out.split()[0])/n_lines
      chunks = int(out.split()[0])%n_lines==0 and chunks or (chunks+1)
    else: 
      chunks=2
      n_lines=int(out.split()[0])/2
    
    for fname in reads_fnames:
      split=Popen('nohup split -a %s -dl %s %s %s'%(len(str(chunks)), n_lines, reads_fnames[fname], reads_fnames[fname]+'.'),shell=True)
      processes.append(split)
	
    for p in processes: p.wait()
    for fname in reads_fnames: os.remove(reads_fnames[fname])
    
    return chunks
    
  
  
def converted_reads_files(reads_file, reads_file1, reads_file2, library, single_end, out_path):
    '''
    Create the files where to store the converted reads
    '''
    if single_end: # single-end alignment
        head, tail = ntpath.split(reads_file)
        fileName, fileExtension = os.path.splitext(tail)

        FW_C2T_fname = out_path+'/'+'FW_C2T'+fileExtension+'.tmp'
        RC_G2A_fname = out_path+'/'+'RC_G2A'+fileExtension+'.tmp'
        reads_fnames = {'FW_C2T':FW_C2T_fname, 'RC_G2A':RC_G2A_fname}

        if library == 2: # for Cokus library
            FW_G2A_fname = out_path+'/'+'FW_G2A'+fileExtension+'.tmp'
            RC_C2T_fname = out_path+'/'+'RC_C2T'+fileExtension+'.tmp'
            reads_fnames['FW_G2A'] = FW_G2A_fname
            reads_fnames['RC_C2T'] = RC_C2T_fname
        return reads_fnames

    else: # pair-end alignment
        head1, tail1 = ntpath.split(reads_file1)
        fileName1, fileExtension1 = os.path.splitext(tail1)
        head2, tail2 = ntpath.split(reads_file2)
        fileName2, fileExtension2 = os.path.splitext(tail2)
        
        FW_C2T_fname_1 = out_path+'/'+'FW_C2T_1'+fileExtension1+'.tmp'
        RC_C2T_fname_2 = out_path+'/'+'RC_C2T_2'+fileExtension1+'.tmp'
        RC_G2A_fname_1 = out_path+'/'+'RC_G2A_1'+fileExtension1+'.tmp'
        FW_G2A_fname_2 = out_path+'/'+'FW_G2A_2'+fileExtension1+'.tmp'
        
        reads_fnames = {'FW_C2T_1':FW_C2T_fname_1, 'RC_C2T_2':RC_C2T_fname_2, 'RC_G2A_1':RC_G2A_fname_1, 'FW_G2A_2':FW_G2A_fname_2}

        if library == 2: # for Cokus library
	    FW_C2T_fname_2 = out_path+'/'+'FW_C2T_2'+fileExtension1+'.tmp'
	    RC_C2T_fname_1 = out_path+'/'+'RC_C2T_1'+fileExtension1+'.tmp'
	    RC_G2A_fname_2 = out_path+'/'+'RC_G2A_2'+fileExtension1+'.tmp'
	    FW_G2A_fname_1 = out_path+'/'+'FW_G2A_1'+fileExtension1+'.tmp'
	    reads_fnames['FW_C2T_2'] = FW_C2T_fname_2
            reads_fnames['RC_C2T_1'] = RC_C2T_fname_1
            reads_fnames['RC_G2A_2'] = RC_G2A_fname_2
            reads_fnames['FW_G2A_1'] = FW_G2A_fname_1
        
        return reads_fnames


def reverse_compl(seq):
    '''
    Return the reverse complement of a nucleotide sequence
    '''
    seq=seq.upper()
    rc_seq=seq.translate(string.maketrans("ATCG", "TAGC"))[::-1]
    return rc_seq;

def reads_conversion_single_end(converted_reads_fnames, reads_file, query_format, out_path, bs_reads_fname, library):
    '''
    Convert the reads according to the library
    '''

    idx=''

    FW_C2T = open(converted_reads_fnames['FW_C2T'+idx],'w')
    RC_G2A = open(converted_reads_fnames['RC_G2A'+idx],'w')
    if library == 2: # for Cokus library
        FW_G2A = open(converted_reads_fnames['FW_G2A'+idx],'w')
        RC_C2T = open(converted_reads_fnames['RC_C2T'+idx],'w')

    bs_reads = open(bs_reads_fname, 'w')

    c = 1
    inc=0
    for line in fileinput.input(reads_file):
        seq=None
        if query_format=="Illumina GAII FastQ":
            if (c==1):
                c+=1
                id = line[:-1]
                FW_C2T.write(id+"\n")
                RC_G2A.write(id+"\n")
                if library == 2:
                    FW_G2A.write(id+"\n")
                    RC_C2T.write(id+"\n")

            elif (c==2):
                c+=1
                seq = line[:-1]
                FW_C2T.write(seq.replace('C','T')+"\n")
                RC_G2A.write(reverse_compl(seq).replace('G','A')+"\n")
                if library == 2:
                    FW_G2A.write(seq.replace('G','A')+"\n")
                    RC_C2T.write(reverse_compl(seq).replace('C','T')+"\n")
            else:
                if c==4: c=1
                else: c+=1
                FW_C2T.write(line)
                RC_G2A.write(line)
                if library == 2:
                    FW_G2A.write(line)
                    RC_C2T.write(line)
            if seq!=None:
                inc+=1
                bs_reads.write(str(inc)+'\t')
                bs_reads.write(id+'\t')
                bs_reads.write(seq+'\n')

        elif query_format=="fasta":
            if line[0]=='>':
                id = line[:-1]
                FW_C2T.write(id+"\n")
                RC_G2A.write(id+"\n")
                if library == 2:
                    FW_G2A.write(id+"\n")
                    RC_C2T.write(id+"\n")
            else:
	      seq = line[:-1]
              FW_C2T.write(seq.replace('C','T')+"\n")
              RC_G2A.write(reverse_compl(seq).replace('G','A')+"\n") 
              if library == 2:
		FW_G2A.write(seq.replace('G','A')+"\n")
                RC_C2T.write(reverse_compl(seq).replace('C','T')+"\n")
	      inc+=1
	      bs_reads.write(str(inc)+'\t')
	      bs_reads.write(id+'\t')
	      bs_reads.write(seq+'\n')

    fileinput.close()

    FW_C2T.close()
    RC_G2A.close()
    if library == 2:
        FW_G2A.close()
        RC_C2T.close()
    bs_reads.close()
    return inc
    
    
def reads_conversion_paired_end(converted_reads_fnames, reads_file, query_format, out_path, bs_reads_fname, library, pair=None):
    '''
    Convert the reads according to the library
    '''

    if pair==None: idx=''
    else: idx='_'+str(pair)
    
    if pair==1: # first read
      FW_C2T = open(converted_reads_fnames['FW_C2T'+idx],'w')
      RC_G2A = open(converted_reads_fnames['RC_G2A'+idx],'w')
      if library == 2: # for Cokus library
	  FW_G2A = open(converted_reads_fnames['FW_G2A'+idx],'w')
	  RC_C2T = open(converted_reads_fnames['RC_C2T'+idx],'w')
    else: # second read
      FW_G2A = open(converted_reads_fnames['FW_G2A'+idx],'w')
      RC_C2T = open(converted_reads_fnames['RC_C2T'+idx],'w')
      if library == 2: # for Cokus library
	  FW_C2T = open(converted_reads_fnames['FW_C2T'+idx],'w')
	  RC_G2A = open(converted_reads_fnames['RC_G2A'+idx],'w')
   	  

    bs_reads = open(bs_reads_fname[pair-1], 'w')

    c = 1
    inc=0
    for line in fileinput.input(reads_file):
        seq=None
        if query_format=="Illumina GAII FastQ":
            if (c==1):
                c+=1
                id = '@'+(str(inc+1))#line[:-1]
                if pair==1:
		  FW_C2T.write(id+"\n")
		  RC_G2A.write(id+"\n")
		  if library == 2:
		      FW_G2A.write(id+"\n")
		      RC_C2T.write(id+"\n")
		else: 
		  FW_G2A.write(id+"\n")
		  RC_C2T.write(id+"\n")
		  if library == 2:
		      FW_C2T.write(id+"\n")
		      RC_G2A.write(id+"\n")      

            elif (c==2):
                c+=1
                seq = line[:-1]
                if pair==1: # read 1
		  FW_C2T.write(seq.replace('C','T')+"\n")
		  RC_G2A.write(seq.replace('C','T')+"\n")
		  if library == 2:
		      FW_G2A.write(reverse_compl(seq).replace('G','A')+"\n")
		      RC_C2T.write(reverse_compl(seq).replace('G','A')+"\n")
		else: # read 2
		  FW_G2A.write(seq.replace('G','A')+"\n")
		  RC_C2T.write(seq.replace('G','A')+"\n")
		  if library == 2:
		      FW_C2T.write(seq.replace('C','T')+"\n")
		      RC_G2A.write(seq.replace('C','T')+"\n")      
		 	
            else:
                if c==4: c=1
                else: c+=1
                if pair==1:
		  FW_C2T.write(line)
		  RC_G2A.write(line)
		  if library == 2:
		      FW_G2A.write(line)
		      RC_C2T.write(line)
		else:
		  FW_G2A.write(line)
		  RC_C2T.write(line)
		  if library == 2:
		      FW_C2T.write(line)
		      RC_G2A.write(line)
		  
            if seq!=None:
                inc+=1
                bs_reads.write(str(inc)+'\t')
                bs_reads.write(id+'\t')
                bs_reads.write(seq+'\n')

        elif query_format=="fasta":
            if line[0]=='>':
                id = '>'+(str(inc+1))#line[:-1]
                if pair==1:
		  FW_C2T.write(id+"\n")
		  RC_G2A.write(id+"\n")
		  if library == 2:
		      FW_G2A.write(id+"\n")
		      RC_C2T.write(id+"\n")
		else:
		  FW_G2A.write(id+"\n")
		  RC_C2T.write(id+"\n")
		  if library == 2:
		      FW_C2T.write(id+"\n")
		      RC_G2A.write(id+"\n")
            else:
	      seq = line[:-1]
	      if pair==1:
		FW_C2T.write(seq.replace('C','T')+"\n")
		RC_G2A.write(reverse_compl(seq).replace('G','A')+"\n") 
		if library == 2:
		  FW_G2A.write(seq.replace('G','A')+"\n")
		  RC_C2T.write(reverse_compl(seq).replace('C','T')+"\n")
	      else:
		FW_G2A.write(seq.replace('G','A')+"\n")
		RC_C2T.write(reverse_compl(seq).replace('C','T')+"\n") 
		if library == 2:
		  FW_C2T.write(seq.replace('C','T')+"\n")
		  RC_G2A.write(reverse_compl(seq).replace('G','A')+"\n")
	      inc+=1
	      bs_reads.write(str(inc)+'\t')
	      bs_reads.write(id+'\t')
	      bs_reads.write(seq+'\n')

    fileinput.close()
    
    if pair==1:
      FW_C2T.close()
      RC_G2A.close()
      if library == 2:
	  FW_G2A.close()
	  RC_C2T.close()
    else:
      FW_G2A.close()
      RC_C2T.close()
      if library == 2:
        FW_C2T.close()
        RC_G2A.close()
    bs_reads.close()
    return inc    
    




def map_single_end_reads(soap3_path, indexes_path, reads_fnames, mismatches, logger, library, gpu_id, type_of_hits, ungapped, length):
    '''
    Invoke SOAP3-dp to map the reads
    '''

    n_dev = len(gpu_id)

    # a single GPU used
    if n_dev==1:
        if ungapped==False: # indels support enabled
	    FW_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T'], type_of_hits, gpu_id[0], length),shell=True)
            FW_C2T_map.wait()
            logger.info('Forward reads with Cs converted to Ts mapped to the first index')
            RC_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A'], type_of_hits, gpu_id[0], length),shell=True)
            RC_G2A_map.wait()
            logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
        else: # indels support disabled
            FW_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T'], type_of_hits, mismatches, gpu_id[0], length),shell=True)
            FW_C2T_map.wait()
            logger.info('Forward reads with Cs converted to Ts mapped to the first index')
            RC_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A'], type_of_hits, mismatches, gpu_id[0], length),shell=True)
            RC_G2A_map.wait()
            logger.info('Reverse complement reads with Gs converted to As mapped to the first index')

        merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T']),shell=True)
        merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A']),shell=True)
        merge_FW_C2T.wait()
        merge_RC_G2A.wait()

        if library==2:
            #if mismatches==-1: 
            if ungapped==False: # indels support enabled
                FW_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A'], type_of_hits, gpu_id[0], length),shell=True)
                FW_G2A_map.wait()
                logger.info('Forward reads with Gs converted to As mapped to the second index')
                RC_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T'], type_of_hits, gpu_id[0], length),shell=True)
                RC_C2T_map.wait()
                logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')

            else: # indels support disabled
                FW_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -s %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A'], mismatches, type_of_hits, gpu_id[0], length),shell=True)
                FW_G2A_map.wait()
                logger.info('Forward reads with Gs converted to As mapped to the second index')
                RC_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -s %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T'], mismatches, type_of_hits, gpu_id[0], length),shell=True)
                RC_C2T_map.wait()
                logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')

            merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A']),shell=True)
            merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T']),shell=True)
            merge_FW_G2A.wait()
            merge_RC_C2T.wait()

    # multiple GPUs can be used
    else:
        # up to 2 cards can be used
        if n_dev==2 or n_dev==3:
            if ungapped==False: # indels support enabled
                FW_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T'], type_of_hits, gpu_id[0], length),shell=True)
                RC_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A'], type_of_hits, gpu_id[1], length),shell=True)

            else: # indels support disabled
                FW_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T'], type_of_hits, mismatches, gpu_id[0], length),shell=True)
                RC_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A'], type_of_hits, mismatches, gpu_id[1], length),shell=True)

            FW_C2T_map.wait()
            RC_G2A_map.wait()
            logger.info('Forward reads with Cs converted to Ts mapped to the first index')
            logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
            merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T']),shell=True)
            merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A']),shell=True)
            merge_FW_C2T.wait()
            merge_RC_G2A.wait()

            if library==2:
                #if mismatches==-1:
                if ungapped==False: # indels support enabled
                    FW_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A'], type_of_hits, gpu_id[0], length),shell=True)
                    RC_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T'], type_of_hits, gpu_id[1], length),shell=True)
                else: # indels support disabled
                    FW_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -s %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A'], mismatches, type_of_hits, gpu_id[0], length),shell=True)
                    RC_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -s %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T'], mismatches, type_of_hits, gpu_id[1], length),shell=True)
                FW_G2A_map.wait()
                RC_C2T_map.wait()
                logger.info('Forward reads with Gs converted to As mapped to the second index')
                logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
                merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A']),shell=True)
                merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T']),shell=True)
                merge_FW_G2A.wait()
                merge_RC_C2T.wait()

        # up to 4 cards can be used
        elif n_dev==4:
	    if library==1:
	      p_chunks = split_reads_files(reads_fnames, query_format) 
	      p_reads_fnames=list()
	      for chunk in range(p_chunks):
		rf=reads_fnames.copy() 
		tmp_rf = dict()
		for fname in rf:
		  tmp_rf[fname]=rf[fname]+'.'+str(chunk).zfill(len(str(p_chunks)))
		p_reads_fnames.append(tmp_rf)
	      if ungapped==False: # indels support enabled
                FW_C2T_map_0=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[0]['FW_C2T'], type_of_hits, gpu_id[0], length),shell=True)
                RC_G2A_map_0=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[0]['RC_G2A'], type_of_hits, gpu_id[1], length),shell=True)
                
                FW_C2T_map_1=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[1]['FW_C2T'], type_of_hits, gpu_id[2], length),shell=True)
                RC_G2A_map_1=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[1]['RC_G2A'], type_of_hits, gpu_id[3], length),shell=True)
                
                FW_C2T_map_0.wait()         
		RC_G2A_map_0.wait()
		FW_C2T_map_1.wait()
		RC_G2A_map_1.wait()
                
	      else: # indels support disabled
		FW_C2T_map_0=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[0]['FW_C2T'], type_of_hits, mismatches, gpu_id[0], length),shell=True)
                RC_G2A_map_0=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[0]['RC_G2A'], type_of_hits, mismatches, gpu_id[1], length),shell=True)
                
                FW_C2T_map_1=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[1]['FW_C2T'], type_of_hits, mismatches, gpu_id[2], length),shell=True)
                RC_G2A_map_1=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, p_reads_fnames[1]['RC_G2A'], type_of_hits, mismatches, gpu_id[3], length),shell=True)
                
		FW_C2T_map_0.wait()         
		RC_G2A_map_0.wait()
		FW_C2T_map_1.wait()
		RC_G2A_map_1.wait()
              
              logger.info('Forward reads with Cs converted to Ts mapped to the first index')
	      logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
	      logger.info('Forward reads with Gs converted to As mapped to the second index')
	      logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
	      merge_FW_C2T_0=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, p_reads_fnames[0]['FW_C2T']),shell=True)
	      merge_RC_G2A_0=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, p_reads_fnames[0]['RC_G2A']),shell=True)
	      merge_FW_C2T_1=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, p_reads_fnames[1]['FW_C2T']),shell=True)
	      merge_RC_G2A_1=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, p_reads_fnames[1]['RC_G2A']),shell=True)
	      
	      merge_FW_C2T_0.wait()
	      merge_RC_G2A_0.wait()
	      merge_FW_C2T_1.wait()
	      merge_RC_G2A_1.wait()
	      
	      merge_FW_C2T=Popen('nohup cat %s %s > %s '%(p_reads_fnames[0]['FW_C2T']+'.out', p_reads_fnames[1]['FW_C2T']+'.out', reads_fnames['FW_C2T']+'.out'),shell=True)
	      merge_RC_G2A=Popen('nohup cat %s %s > %s '%(p_reads_fnames[0]['RC_G2A']+'.out', p_reads_fnames[1]['RC_G2A']+'.out', reads_fnames['RC_G2A']+'.out'),shell=True)
	      merge_FW_C2T.wait()
	      merge_RC_G2A.wait()
	      merge_FW_C2T_reads=Popen('nohup cat %s %s > %s '%(p_reads_fnames[0]['FW_C2T'], p_reads_fnames[1]['FW_C2T'], reads_fnames['FW_C2T']),shell=True)
	      merge_RC_G2A_reads=Popen('nohup cat %s %s > %s '%(p_reads_fnames[0]['RC_G2A'], p_reads_fnames[1]['RC_G2A'], reads_fnames['RC_G2A']),shell=True)
	      merge_FW_C2T_reads.wait()
	      merge_RC_G2A_reads.wait()
	      
                
            else: #library==2
	      if ungapped==False: # indels support enabled
		  FW_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T'], type_of_hits, gpu_id[0], length),shell=True)
		  RC_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A'], type_of_hits, gpu_id[1], length),shell=True)
		  FW_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A'], type_of_hits, gpu_id[2], length),shell=True)
		  RC_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T'], type_of_hits, gpu_id[3], length),shell=True)
	      
	      else: # indels support disabled
		  FW_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T'], type_of_hits, mismatches, gpu_id[0], length),shell=True)
		  RC_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -h %s -s %s -c %s -b 2 -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A'], type_of_hits, mismatches, gpu_id[1], length),shell=True)
		  FW_G2A_map=Popen('nohup %ssoap3-dp single %sFW_G2A.fa.index %s -s %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A'], mismatches, type_of_hits, gpu_id[2], length),shell=True)
		  RC_C2T_map=Popen('nohup %ssoap3-dp single %sFW_C2T.fa.index %s -s %s -h %s -b 2 -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T'], mismatches, type_of_hits, gpu_id[3], length),shell=True)
		  
	        
	      FW_C2T_map.wait()
	      RC_G2A_map.wait()
	      FW_G2A_map.wait()
	      RC_C2T_map.wait()
	      logger.info('Forward reads with Cs converted to Ts mapped to the first index')
	      logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
	      logger.info('Forward reads with Gs converted to As mapped to the second index')
	      logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
	      
	      merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T']),shell=True)
	      merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A']),shell=True)
	      merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A']),shell=True)
	      merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T']),shell=True)
	      merge_FW_C2T.wait()
	      merge_RC_G2A.wait()
	      merge_FW_G2A.wait()
	      merge_RC_C2T.wait()
		


def map_pair_end_reads(soap3_path, indexes_path, reads_fnames, mismatches, maxInsertSize, minInsertSize, logger, library, gpu_id, type_of_hits, ungapped, length):
    '''
    Invoke SOAP3-dp to map the reads
    '''

    n_dev = len(gpu_id)

    # a single GPU used
    if n_dev==1:
	if ungapped==False: # indels support enabled
	  FW_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T_1'], reads_fnames['FW_G2A_2'],
	  type_of_hits, maxInsertSize, minInsertSize, gpu_id[0], length),shell=True)
	  FW_C2T_map.wait() # wait to synchronize GPU threads
	  logger.info('Forward reads with Cs converted to Ts mapped to the first index')
	  RC_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A_1'], reads_fnames['RC_C2T_2'],  type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
	  RC_G2A_map.wait()
	  os.remove(reads_fnames['FW_C2T_1']+'.unpair')
	  os.remove(reads_fnames['RC_G2A_1']+'.unpair')
	  logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
	  merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T_1']),shell=True)
	  merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A_1']),shell=True)
	  merge_FW_C2T.wait()
	  merge_RC_G2A.wait()
	else: # indels support disabled
	  FW_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T_1'], reads_fnames['FW_G2A_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize, gpu_id[0], length),shell=True)
	  FW_C2T_map.wait() # wait to synchronize GPU threads
	  logger.info('Forward reads with Cs converted to Ts mapped to the first index')
	  RC_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A_1'], reads_fnames['RC_C2T_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
	  RC_G2A_map.wait()
	  os.remove(reads_fnames['FW_C2T_1']+'.unpair')
	  os.remove(reads_fnames['RC_G2A_1']+'.unpair')
	  logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
	  merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T_1']),shell=True)
	  merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A_1']),shell=True)
	  merge_FW_C2T.wait()
	  merge_RC_G2A.wait()

        if library==2:
	    if ungapped==False: # indels support enabled
	      FW_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A_1'], reads_fnames['FW_C2T_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
	      FW_G2A_map.wait()
	      logger.info('Forward reads with Gs converted to As mapped to the second index')
	      RC_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T_1'], reads_fnames['RC_G2A_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
	      RC_C2T_map.wait()
	      os.remove(reads_fnames['FW_G2A_1']+'.unpair')
	      os.remove(reads_fnames['RC_C2T_1']+'.unpair')
	      logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
	      merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A_1']),shell=True)
	      merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T_1']),shell=True)
	      merge_FW_G2A.wait()
	      merge_RC_C2T.wait()
	    else: # indel support disabled
	      FW_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A_1'], reads_fnames['FW_C2T_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
	      FW_G2A_map.wait()
	      logger.info('Forward reads with Gs converted to As mapped to the second index')
	      RC_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T_1'], reads_fnames['RC_G2A_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
	      RC_C2T_map.wait()
	      os.remove(reads_fnames['FW_G2A_1']+'.unpair')
	      os.remove(reads_fnames['RC_C2T_1']+'.unpair')
	      logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
	      merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A_1']),shell=True)
	      merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T_1']),shell=True)
	      merge_FW_G2A.wait()
	      merge_RC_C2T.wait()

    # multiple GPUs can be used
    else:
        # up to 2 cards can be used
        if n_dev==2:
	    if ungapped==False: # indels support enabled
	      FW_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T_1'], reads_fnames['FW_G2A_2'], type_of_hits, maxInsertSize, minInsertSize, gpu_id[0], length),shell=True)
	      RC_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A_1'], reads_fnames['RC_C2T_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[1], length),shell=True)
	      FW_C2T_map.wait() # wait to synchronize GPU threads
	      logger.info('Forward reads with Cs converted to Ts mapped to the first index')
	      RC_G2A_map.wait()
	      os.remove(reads_fnames['FW_C2T_1']+'.unpair')
	      os.remove(reads_fnames['RC_G2A_1']+'.unpair')
	      logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
	      merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T_1']),shell=True)
	      merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A_1']),shell=True)
	      merge_FW_C2T.wait()
	      merge_RC_G2A.wait()
	      
	      
	    else: # indels support disabled
	      FW_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T_1'], reads_fnames['FW_G2A_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize, gpu_id[0], length),shell=True)
	      RC_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A_1'], reads_fnames['RC_C2T_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[1], length),shell=True)
	      FW_C2T_map.wait() # wait to synchronize GPU threads
	      os.remove(reads_fnames['FW_C2T_1']+'.unpair')
	      os.remove(reads_fnames['RC_G2A_1']+'.unpair')
	      
	      
	      logger.info('Forward reads with Cs converted to Ts mapped to the first index')
	      RC_G2A_map.wait()
	      logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
	      merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T_1']),shell=True)
	      merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A_1']),shell=True)
	      merge_FW_C2T.wait()
	      merge_RC_G2A.wait()

            if library==2:
		if ungapped==False: # indels support enabled
		  FW_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A_1'], reads_fnames['FW_C2T_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
		  RC_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T_1'], reads_fnames['RC_G2A_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[1], length),shell=True)
		  FW_G2A_map.wait()
		  logger.info('Forward reads with Gs converted to As mapped to the second index')
		  RC_C2T_map.wait()
		  os.remove(reads_fnames['FW_G2A_1']+'.unpair')
		  os.remove(reads_fnames['RC_C2T_1']+'.unpair')
		  logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
		  merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A_1']),shell=True)
		  merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T_1']),shell=True)
		  merge_FW_G2A.wait()
		  merge_RC_C2T.wait()

		else: # indels support disabled
		  FW_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A_1'], reads_fnames['FW_C2T_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[0], length),shell=True)
		  RC_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T_1'], reads_fnames['RC_G2A_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[1], length),shell=True)
		  FW_G2A_map.wait()
		  os.remove(reads_fnames['FW_G2A_1']+'.unpair')
		  os.remove(reads_fnames['RC_C2T_1']+'.unpair')
		  logger.info('Forward reads with Gs converted to As mapped to the second index')
		  RC_C2T_map.wait()
		  logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
		  merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A_1']),shell=True)
		  merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T_1']),shell=True)
		  merge_FW_G2A.wait()
		  merge_RC_C2T.wait()
        # up to 4 cards can be used
        elif n_dev==4:
	    if ungapped==False: # indels support enabled
	      FW_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T_1'], reads_fnames['FW_G2A_2'], type_of_hits, maxInsertSize, minInsertSize, gpu_id[0], length),shell=True)
	      RC_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A_1'], reads_fnames['RC_C2T_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[1], length),shell=True)
	      os.remove(reads_fnames['FW_C2T_1']+'.unpair')
	      os.remove(reads_fnames['RC_G2A_1']+'.unpair')
	      merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T_1']),shell=True)
	      merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A_1']),shell=True)
	      merge_FW_C2T.wait()
	      merge_RC_G2A.wait()
	    else: # indels support disabled
	      FW_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_C2T_1'], reads_fnames['FW_G2A_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize, gpu_id[0], length),shell=True)
	      RC_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -s %s -h %s -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_G2A_1'], reads_fnames['RC_C2T_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[1], length),shell=True)
	      os.remove(reads_fnames['FW_C2T_1']+'.unpair')
	      os.remove(reads_fnames['RC_G2A_1']+'.unpair')
	      merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T_1']),shell=True)
	      merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A_1']),shell=True)
	      merge_FW_C2T.wait()
	      merge_RC_G2A.wait()
	    
            if library==2:
		if ungapped==False: # indels support enabled
		  FW_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -h 2 -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A_1'], reads_fnames['FW_C2T_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[2], length),shell=True)
		  RC_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -h 2 -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T_1'], reads_fnames['RC_G2A_2'], type_of_hits, maxInsertSize, minInsertSize,  gpu_id[3], length),shell=True)
		  FW_G2A_map.wait()
		  logger.info('Forward reads with Gs converted to As mapped to the second index')
		  RC_C2T_map.wait()
		  os.remove(reads_fnames['FW_G2A_1']+'.unpair')
		  os.remove(reads_fnames['RC_C2T_1']+'.unpair')
		  logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
		  merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A_1']),shell=True)
		  merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T_1']),shell=True)
		  merge_FW_G2A.wait()
		  merge_RC_C2T.wait()
		else: # indels support disabled
		  FW_G2A_map=Popen('nohup %ssoap3-dp pair %sFW_C2T.fa.index %s %s -s %s -h 2 -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['FW_G2A_1'], reads_fnames['FW_C2T_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[2], length),shell=True)
		  RC_C2T_map=Popen('nohup %ssoap3-dp pair %sFW_G2A.fa.index %s %s -s %s -h 2 -b 2 -u %s -v %s -c %s -p -L %s'%(soap3_path, indexes_path, reads_fnames['RC_C2T_1'], reads_fnames['RC_G2A_2'], mismatches, type_of_hits, maxInsertSize, minInsertSize,  gpu_id[3], length),shell=True)
		  FW_G2A_map.wait()
		  os.remove(reads_fnames['FW_G2A_1']+'.unpair')
		  os.remove(reads_fnames['RC_C2T_1']+'.unpair')
		  logger.info('Forward reads with Gs converted to As mapped to the second index')
		  RC_C2T_map.wait()
		  logger.info('Reverse complement reads with Cs converted to Ts mapped to the first index\n')
		  merge_FW_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_G2A_1']),shell=True)
		  merge_RC_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_C2T_1']),shell=True)
		  merge_FW_G2A.wait()
		  merge_RC_C2T.wait()

            FW_C2T_map.wait() # wait to synchronize GPU threads
            logger.info('Forward reads with Cs converted to Ts mapped to the first index')
            RC_G2A_map.wait()
            logger.info('Reverse complement reads with Gs converted to As mapped to the first index')
            merge_FW_C2T=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['FW_C2T_1']),shell=True)
            merge_RC_G2A=Popen('nohup %smerge-sam.sh %s'%(UTILS_PATH, reads_fnames['RC_G2A_1']),shell=True)
            merge_FW_C2T.wait()
            merge_RC_G2A.wait()

 
def remove_ambiguous(reads_fnames, library, edit_distance, single_end, indexes_path, rrbs, all_valid=False):
    '''
    Remove those reads that match at least 2 times in all possible alignments (different strands)
    '''
    
    if single_end: idx=''
    else: idx='_1'

    FW_C2T_ALIGN, FW_C2T_POS = get_alignments(reads_fnames['FW_C2T'+idx], int(edit_distance), '+FW', single_end, all_valid)
    RC_G2A_ALIGN, RC_G2A_POS = get_alignments(reads_fnames['RC_G2A'+idx], int(edit_distance), '-FW', single_end, all_valid)
    
    if library == 2:
        FW_G2A_ALIGN, FW_G2A_POS = get_alignments(reads_fnames['FW_G2A'+idx], int(edit_distance), '-RC', single_end, all_valid)
        RC_C2T_ALIGN, RC_C2T_POS = get_alignments(reads_fnames['RC_C2T'+idx], int(edit_distance), '+RC', single_end, all_valid)
  
    if library==1: mappings = [(FW_C2T_ALIGN, FW_C2T_POS), (RC_G2A_ALIGN, RC_G2A_POS)]
    else: mappings = [(FW_C2T_ALIGN, FW_C2T_POS), (RC_G2A_ALIGN, RC_G2A_POS), (FW_G2A_ALIGN, FW_G2A_POS), (RC_C2T_ALIGN, RC_C2T_POS)]
    
      
    if True:	  
      if True:#w_ambiguous==False:
	  ambiguous=set()
	  if library == 1: # directional
	    poss_ambiguous = set(FW_C2T_ALIGN.keys()).intersection(set(RC_G2A_ALIGN.keys()))
	    for read_id in poss_ambiguous:
	      # ambiguous are those reads that present at least a mapping
	      # with the lower number of differences in at least two different alignments
	      for d in range(int(edit_distance)+1):
		if (FW_C2T_ALIGN[read_id][d]!=0 and RC_G2A_ALIGN[read_id][d]!=0):
		  if (FW_C2T_POS[read_id][0]['score']==RC_G2A_POS[read_id][0]['score']):
		    ambiguous.add(read_id)
		    break #continue
		  elif (FW_C2T_POS[read_id][0]['score']>RC_G2A_POS[read_id][0]['score']):
		    del(RC_G2A_ALIGN[read_id]); del(RC_G2A_POS[read_id])
		    break
		  elif (FW_C2T_POS[read_id][0]['score']<RC_G2A_POS[read_id][0]['score']):  
		    del(FW_C2T_ALIGN[read_id]); del(FW_C2T_POS[read_id])
		    break
		elif (FW_C2T_ALIGN[read_id][d]!=0 and RC_G2A_ALIGN[read_id][d]==0):
		    del(RC_G2A_ALIGN[read_id]); del(RC_G2A_POS[read_id])
		    break
		elif (FW_C2T_ALIGN[read_id][d]==0 and RC_G2A_ALIGN[read_id][d]!=0):
		    del(FW_C2T_ALIGN[read_id]); del(FW_C2T_POS[read_id])
		    break
		else: continue
	  else: # non-directional
	    poss_ambiguous = set().union(*(set(FW_C2T_ALIGN.keys()).intersection(set(RC_G2A_ALIGN.keys())),	set(FW_C2T_ALIGN.keys()).intersection(set(FW_G2A_ALIGN.keys())), set(FW_C2T_ALIGN.keys()).intersection(set(RC_C2T_ALIGN.keys())), set(RC_G2A_ALIGN.keys()).intersection(set(FW_G2A_ALIGN.keys())),	    set(RC_G2A_ALIGN.keys()).intersection(set(RC_C2T_ALIGN.keys())), set(FW_G2A_ALIGN.keys()).intersection(set(RC_C2T_ALIGN.keys()))))
	    
	    #ambiguous=set()
	    for read_id in poss_ambiguous:
	      for d in range(int(edit_distance)+1):
		alignment_score = {'FW_C2T':0, 'RC_G2A':0, 'FW_G2A':0, 'RC_C2T':0}
		if single_end:
		  if read_id in FW_C2T_ALIGN:
		    if FW_C2T_ALIGN[read_id][d]!=0: 
		      alignment_score['FW_C2T'] = max([mapped_pos['score'] for mapped_pos in FW_C2T_POS[read_id] if mapped_pos['ed']==d])
		  if read_id in RC_G2A_ALIGN: 
		    if RC_G2A_ALIGN[read_id][d]!=0: 
		      alignment_score['RC_G2A'] = max([mapped_pos['score'] for mapped_pos in RC_G2A_POS[read_id] if mapped_pos['ed']==d])
		  if read_id in FW_G2A_ALIGN: 
		    if FW_G2A_ALIGN[read_id][d]!=0: 
		      alignment_score['FW_G2A'] = max([mapped_pos['score'] for mapped_pos in FW_G2A_POS[read_id] if mapped_pos['ed']==d])
		  if read_id in RC_C2T_ALIGN: 
		    if RC_C2T_ALIGN[read_id][d]!=0: 
		      alignment_score['RC_C2T'] = max([mapped_pos['score'] for mapped_pos in RC_C2T_POS[read_id] if mapped_pos['ed']==d])
		else:
		  if read_id in FW_C2T_ALIGN:
		    if FW_C2T_ALIGN[read_id][d]!=0: 
		      alignment_score['FW_C2T'] = FW_C2T_POS[read_id][0]['score']
		  if read_id in RC_G2A_ALIGN: 
		    if RC_G2A_ALIGN[read_id][d]!=0: 
		      alignment_score['RC_G2A'] = RC_G2A_POS[read_id][0]['score']
		  if read_id in FW_G2A_ALIGN: 
		    if FW_G2A_ALIGN[read_id][d]!=0: 
		      alignment_score['FW_G2A'] = FW_G2A_POS[read_id][0]['score']
		  if read_id in RC_C2T_ALIGN: 
		    if RC_C2T_ALIGN[read_id][d]!=0: 
		      alignment_score['RC_C2T'] = RC_C2T_POS[read_id][0]['score']
		
			  
		max_score = max(alignment_score.values())
		aligned_strands = [x for x,y in alignment_score.items() if y==max_score]
		if len(aligned_strands)==1: # a unique best alignment
		  if aligned_strands[0]=='FW_C2T':
		    if read_id in RC_G2A_ALIGN: del(RC_G2A_ALIGN[read_id]); del(RC_G2A_POS[read_id])
		    if read_id in FW_G2A_ALIGN: del(FW_G2A_ALIGN[read_id]); del(FW_G2A_POS[read_id])
		    if read_id in RC_C2T_ALIGN: del(RC_C2T_ALIGN[read_id]); del(RC_C2T_POS[read_id])
		    break
		  elif aligned_strands[0]=='RC_G2A':	
		    if read_id in FW_C2T_ALIGN: del(FW_C2T_ALIGN[read_id]); del(FW_C2T_POS[read_id])
		    if read_id in FW_G2A_ALIGN: del(FW_G2A_ALIGN[read_id]); del(FW_G2A_POS[read_id])
		    if read_id in RC_C2T_ALIGN: del(RC_C2T_ALIGN[read_id]); del(RC_C2T_POS[read_id])
		    break
		  elif aligned_strands[0]=='FW_G2A':	
		    if read_id in FW_C2T_ALIGN: del(FW_C2T_ALIGN[read_id]); del(FW_C2T_POS[read_id])
		    if read_id in RC_G2A_ALIGN: del(RC_G2A_ALIGN[read_id]); del(RC_G2A_POS[read_id])
		    if read_id in RC_C2T_ALIGN: del(RC_C2T_ALIGN[read_id]); del(RC_C2T_POS[read_id])
		    break
		  elif aligned_strands[0]=='RC_C2T':	
		    if read_id in FW_C2T_ALIGN: del(FW_C2T_ALIGN[read_id]); del(FW_C2T_POS[read_id])
		    if read_id in RC_G2A_ALIGN: del(RC_G2A_ALIGN[read_id]); del(RC_G2A_POS[read_id])
		    if read_id in FW_G2A_ALIGN: del(FW_G2A_ALIGN[read_id]); del(FW_G2A_POS[read_id])
		    break 
		else:
		  ambiguous.add(read_id)
		  break #continue
	      
	  del poss_ambiguous
	  
	  for read in ambiguous:
	     if True:#try:
		  if read in FW_C2T_ALIGN: 
		    del(FW_C2T_ALIGN[read]); del(FW_C2T_POS[read])
		  if read in RC_G2A_ALIGN:
		    del(RC_G2A_ALIGN[read]); del(RC_G2A_POS[read])
		  if library==2:
		      if read in FW_G2A_ALIGN:
			del(FW_G2A_ALIGN[read]); del(FW_G2A_POS[read])
		      if read in RC_C2T_ALIGN:
			del(RC_C2T_ALIGN[read]); del(RC_C2T_POS[read])
	      #except KeyError: pass    
	  
	  # free the memory
	  del(FW_C2T_ALIGN); del(RC_G2A_ALIGN)
	  if library==2:
	      del(FW_G2A_ALIGN); del(RC_C2T_ALIGN)
   
    
    if (library==1): return [FW_C2T_POS, RC_G2A_POS]
    return [FW_C2T_POS, RC_G2A_POS, FW_G2A_POS, RC_C2T_POS]


  
def get_valid_reads(valid_mappings, bs_reads_fname, library):
    '''
    Return only the not ambiguous reads
    '''
    valid_read_ids = set()
    valid_read_ids.update(set(valid_mappings[0].keys()))
    valid_read_ids.update(set(valid_mappings[1].keys()))
    if library==2:
        valid_read_ids.update(set(valid_mappings[2].keys()))
        valid_read_ids.update(set(valid_mappings[3].keys()))
    reads = {}
    for line in fileinput.input(bs_reads_fname):
        l = line.split()
        read_id = l[1][1:]
        if read_id in valid_read_ids:
            reads[read_id] = {}
            reads[read_id]['header'] = l[1]+' '+l[2]
            reads[read_id]['read'] = l[-1] # the original bisulfite-treated read
    fileinput.close()
    return reads

def calc_mismatches(read, reference, rule='TC'):
    '''
    Calculate the number of mismatches.
    '''
    pairs = []
    pairs = [read[i]+reference[i] for i in range(min([len(read), len(reference)])) if read[i]!=reference[i] and read[i]!="N" and reference[i]!="N"]
    return len([paired for paired in pairs if paired != rule])

    
def get_header(out_path, single_end):
  s=''
  if single_end: fin = out_path+'/FW_C2T.fastq.tmp.0.out'
  else: fin = out_path+'/FW_C2T_1.fastq.tmp.0.out'
  for line in fileinput.input(fin):
    if line[0]=='@': s+=line
    else: break
  fileinput.close()
  fout=open(out_path+'/header', 'w')
  fout.write(s)
  fout.close()

def methylation_levels(read, reference):
    '''
    Calculate the methylation levels
    
        - bases that not involving cytosines
        X   methylated C in CHG context
        x unmethylated C in CHG context
        H   methylated C in CHH context
        h unmethylated C in CHH context
        Z   methylated C in CpG context
        z unmethylated C in CpG context
    '''

    H = ['A','C','T']
    reference = reference.replace('_','')
    methylation = str()
    level = '-'
    try:
      for i in range(len(read)):
	  if read[i] not in ['C','T']: level = '-'
	  elif read[i]=='T' and reference[i+2]=='C': # unmethylated Cs
	      if reference[i+3]=='G': level = 'x'
	      elif reference[i+3] in H :
		  if reference[i+4]=='G': level = 'y'
		  elif reference[i+4] in H: level = 'z'
	  elif read[i]=='C' and reference[i+2]=='C': # methylated Cs
	      if reference[i+3]=='G': level = 'X'
	      elif reference[i+3] in H: 
		  if reference[i+4]=="G": level = 'Y'
		  elif reference[i+4] in H: level = 'Z'
	  else: level = '-'
	  methylation = methylation + level
    except: pass # err: print err for debug
    return methylation


def four_nt_analysis_single(strand_alignments, reference_seqs, library, methylation, mismatches, bs_reads_fname, out_path, n, ed_limit, ungapped, rrbs, ref_names_conv, indexes_path, red_site, chunk, chunks, w_ambiguous, end_to_end, logger):
  
  
    
    XR={0:'CT', 1:'CT', 2:'GA', 3:'GA'}
    XG={0:'CT', 1:'GA', 2:'CT', 3:'GA'}
    #FLAG={0:'0', 1:'16', 2:'16', 3:'0'} # consider only bit 0x10
    FLAG={1:'0', 2:'16', 3:'16', 4:'0'} # consider only bit 0x10 
    n_alignments = dict()
    
    # load into the memory the (successfully) mapped reads
    if rrbs:
      for i in range(len(strand_alignments)):
	for k in strand_alignments[i].keys():
	  if strand_alignments[i][k]==[]: del strand_alignments[i][k]
      
    valid_mapped_reads = get_valid_reads(strand_alignments, bs_reads_fname, library)
    if chunks!=0: out_alignments = open(out_path+'/'+ALIGNMENTS_FNAME+'-'+str(chunk), 'w')
    else: out_alignments = open(out_path+'/'+ALIGNMENTS_FNAME, 'w')
    if ungapped==False: mismatches=ed_limit

    i=0
    for alignments in strand_alignments:
        i+=1
        if methylation: logger.info('Analyzing edit distance (4-letter nt alphabet) and methylation - strand %d of %d'%(i, len(strand_alignments)))
        else: logger.info('Analyzing edit distance (4-letter nt alphabet) - strand %d of %d'%(i, len(strand_alignments)))
        
	fragments=dict()
	nb_alg=0
	#print '\n[Debug] Alignments in 3-letter nt alphabet', len(alignments.keys())
	temp_found=0; temp_mapped=0 #for debug
	#try:
	if True:
	  for read_id in alignments.keys():
	      found_hits = dict()
	      for hit in range(len(alignments[read_id])): 
		position = alignments[read_id][hit]['position']
		strand = alignments[read_id][hit]['strand']
		strand_fa = alignments[read_id][hit]['strand_fa']
		seq_id = alignments[read_id][hit]['seq_id'].zfill(4) 
		
		if rrbs:
		  if i%2==1: fname = indexes_path+seq_id+'_'+FRAGMENTS_FNAME_F
		  else:  fname = indexes_path+seq_id+'_'+FRAGMENTS_FNAME_R
		nb_alg+=1
		cigar = alignments[read_id][hit]['cigar']

		cigar_op = 'MIDNSHP=X'
		p_cigar_op = dict([(j, cigar[j]) for j in range(len(cigar)) if cigar[j] in cigar_op])

		indels = ('I' in cigar) or ('D' in cigar) or ('S' in cigar)
		
		
		if (i%2==1): read_seq = valid_mapped_reads[read_id]['read'].upper()
		else: read_seq = reverse_compl(valid_mapped_reads[read_id]['read'].upper())
		
		if not rrbs:
		  reference_long = reference_seqs[seq_id][alignments[read_id][hit]['position']-2-1:alignments[read_id][hit]['position']+len(read_seq)+2-1].upper()
		  reference = reference_long[2:-2]
		else:
		  if i%2==1: k='FW'
		  else:  k='RC'
		  reference_long = reference_seqs[seq_id][k][alignments[read_id][hit]['position']-2-1:alignments[read_id][hit]['position']+len(read_seq)+2-1].upper()
		  reference = reference_long[2:-2]
		
		offset=0
		reference_no_clip=''
		if indels:
		  
		    tmp_read_seq=''
		    tmp_reference=''
		    soft_clipped=[None,None]
		    
		    k = 0 # cigar string shift index
		    idx_r = 0 # read sequence shift index
		    idx_R = 0 # reference sequence shift index
		    
		    insertions=0
		    deletions=0
		    for j in sorted(p_cigar_op.iterkeys()):
			step = int(cigar[k:j])
			if (p_cigar_op[j]=='I'):# insertion
			    tmp_reference+='-'*step
			    tmp_read_seq+=read_seq[idx_r:idx_r+step]
			    idx_r+=step
			    offset+=step
			    insertions+=step
			elif (p_cigar_op[j]=='S'): # soft clipping
			    #tmp_reference+=reference[idx_R:idx_R+step]
			    #tmp_read_seq+=read_seq[idx_r:idx_r+step]
			    offset+=step	  
			    if j==len(cigar)-1: # end clipping
			      soft_clipped[1]=step
			      tmp_reference+=reference[idx_R:idx_R+step]
			      tmp_read_seq+=read_seq[idx_r:idx_r+step]
			      idx_r+=step
			      idx_R+=step
			    else: 
			      soft_clipped[0]=step # front clipping
			      if i%2==1:
				tmp_reference+=reference[idx_R:idx_R+step]
				tmp_read_seq+=read_seq[idx_r:idx_r+step]
				idx_r+=step
				idx_R+=step
			      else:
				tmp_read_seq+=read_seq[idx_r:idx_r+step]
				idx_r+=step
			elif p_cigar_op[j]=='D': # deletion
			    tmp_read_seq+='-'*step
			    tmp_reference+=reference[idx_R:idx_R+step]
			    idx_R+=step
			    deletions+=step
			else: # match or mismatch
			    tmp_read_seq+=read_seq[idx_r:idx_r+step]
			    tmp_reference+=reference[idx_R:idx_R+step]
			    idx_r+=step
			    idx_R+=step
			k = j+1


		    if soft_clipped[0]!=None: 
		      tmp_read_seq=tmp_read_seq[soft_clipped[0]:]
		    if soft_clipped[1]!=None:
		      if i%2==1:
			tmp_read_seq=tmp_read_seq[:-soft_clipped[1]]
			if (soft_clipped[0]==None): soft_clipped[0]=0
			tmp_reference=tmp_reference[:-soft_clipped[1]-soft_clipped[0]]
		      else:
			tmp_read_seq=tmp_read_seq[:-soft_clipped[1]]
			tmp_reference=tmp_reference[:-soft_clipped[1]]
		      
		    read_seq=tmp_read_seq
		    reference_no_clip=reference
		    reference=tmp_reference
		    
		else: reference_no_clip = reference
		    
		if rrbs:
		  if i%2==1: fname = indexes_path+seq_id+'_'+FRAGMENTS_FNAME_F
		  else: fname = indexes_path+seq_id+'_'+FRAGMENTS_FNAME_R
		
		if library==1:  
		  if (i%2==1): n_mis = calc_mismatches(read_seq, reference) 
		  else: n_mis = calc_mismatches(read_seq, reference, 'AG')
		else:
		  if i==1 or i==4: n_mis = calc_mismatches(read_seq, reference)
		  if i==2 or i==3: n_mis = calc_mismatches(read_seq, reference, 'AG')
		
		
		if end_to_end and 'S' in cigar: n_mis=None # sometimes soap3-dp reports local aligmnents in e2e mode
		
		if (n_mis!=None and n_mis <= mismatches):
		  
		  found=True
		  if rrbs:
		    if not fragments.has_key(seq_id):
		      fragments_f = open(fname, 'rb')
		      fragments[seq_id] = marshal.load(fragments_f)
		      fragments_f.close()  
		      
		      
		    f_id=None; f_s=None; f_e=None
		    if i%2==1: f_s = position 
		    else: 
		      if cigar[sorted(p_cigar_op.iterkeys())[0]]=='S': offset=int(cigar[0:sorted(p_cigar_op.iterkeys())[0]])
		      else: offset=0
		      f_s= position  + len(read_seq) - len(red_site[red_site.find('-')+1:]) 
		    try:
		      if i%2==1:
			f_id = fragments[seq_id][f_s][2]
			f_e = fragments[seq_id][f_s][1]
			f_s = fragments[seq_id][f_s][0]
			position = f_s
		      else:
			f_id = fragments[seq_id][f_s][2]
			f_e = fragments[seq_id][f_s][0]
			f_s = fragments[seq_id][f_s][1]
			position = f_s + (f_e - f_s) - len(read_seq) 
		       
		      if n_mis not in found_hits: found_hits[n_mis]=list()
		      found_hits[n_mis].append({'hit':hit, 'position': position, 'cigar': cigar, 'ref': reference_no_clip, 'f_id': f_id, 'f_s': f_s, 'f_e': f_e})  
		    
		    except:
		      found=False; 
		      temp_found+=1; #for debug
		  else:
		    if n_mis not in found_hits: found_hits[n_mis]=list()
		    found_hits[n_mis].append({'hit':hit, 'position': position, 'cigar': cigar, 'ref': reference_no_clip})
	      
	      if len(found_hits)>0:
		temp_mapped+=1
		best_score = min(found_hits)
		n_mis = max(found_hits, key=found_hits.get)
		if len(found_hits[best_score])==1 or w_ambiguous==True:
		  if not n_alignments.has_key(n_mis): n_alignments[n_mis]=0
		  n_alignments[n_mis]+=1
		  
		  hit = found_hits[best_score][0]['hit']
		  n_mis = best_score
		  if i%2==1: k='FW'
		  else:  k='RC'
		  if not rrbs:
		    reference_longx = reference_seqs[seq_id][alignments[read_id][hit]['position']-2-1:alignments[read_id][hit]['position']+len(read_seq)+2-1].upper()
		  else:
		    reference_longx = reference_seqs[seq_id][k][alignments[read_id][hit]['position']-2-1:alignments[read_id][hit]['position']+len(read_seq)+2-1].upper()
		      
		  methylation_seq = '' # by default no methylation levels are calculated
		  if methylation: methylation_seq = 'XM:Z:'+ methylation_levels(read_seq, reference_longx)
		  
		  fread_id = valid_mapped_reads[read_id]['header'].split()[0]
		  fread_id = fread_id*(fread_id[0]!='@') + fread_id[1:]*(fread_id[0]=='@')
		    
		  if rrbs:
		    out_alignments.write(fread_id + '\t' + FLAG[i]+'\t' + ref_names_conv[seq_id].zfill(4) + '\t' + str(found_hits[best_score][0]['position']) + '\t' + '255' + '\t' + found_hits[best_score][0]['cigar'] + '\t' + '*' + '\t'+ '0' + '\t' + '0' + '\t' + found_hits[best_score][0]['ref'] + '\t' + '*' + '\t' + 'NM:i:'+str(n_mis) + '\t' + methylation_seq + '\t' + 'XR:Z:'+XR[i-1] + '\t' + 'XG:Z:'+XG[i-1] + '\t' + 'YF:'+str(found_hits[best_score][0]['f_id']) + '\t' + 'YS:'+str(found_hits[best_score][0]['f_s']) + '\t' + 'YE:'+str(found_hits[best_score][0]['f_e']) + '\n') 
		  else:
		    out_alignments.write(fread_id + '\t' + FLAG[i] + '\t' + ref_names_conv[seq_id].zfill(4) + '\t' + str(found_hits[best_score][0]['position']) + '\t' + '255' + '\t' + found_hits[best_score][0]['cigar'] + '\t' + '*' + '\t' + '0' + '\t' + '0' + '\t' + found_hits[best_score][0]['ref'] + '\t' + '*' + '\t' + 'NM:i:'+str(n_mis) + '\t' + methylation_seq + '\t' + 'XR:Z:'+XR[i-1] + '\t' + 'XG:Z:'+XG[i-1] + '\n')
		  
		    
        #except Exception, err:  print '[Debug]', err #pass
        #print '[Debug] Mapped:', temp_mapped
        #print '[Debug] Fragments not found:', temp_found
        #print '\n'
    out_alignments.close()
    return n_alignments



def four_nt_analysis_paired(strand_alignments, reference_seqs, library, methylation, mismatches, bs_reads_fname, out_path, n, ed_limit, ungapped, rrbs, ref_names_conv, indexes_path, red_site, chunk, chunks, end_to_end, logger):
  
  
    
    XR={0:'CT', 1:'CT', 2:'GA', 3:'GA'}
    XG={0:'CT', 1:'GA', 2:'CT', 3:'GA'}
    FLAG={1:'0', 2:'16', 3:'16', 4:'0'} # consider only bit 0x10 
    n_alignments = dict()
    
    # load into the memory the (successfully) mapped reads
    if rrbs:
      for i in range(len(strand_alignments)):
	for k in strand_alignments[i].keys():
	  if strand_alignments[i][k]==[]: del strand_alignments[i][k]
    
    valid_mapped_reads = [None]*2
    valid_mapped_reads[0] = get_valid_reads(strand_alignments, bs_reads_fname[0], library)
    valid_mapped_reads[1] = get_valid_reads(strand_alignments, bs_reads_fname[1], library)
    if chunks!=0: out_alignments = open(out_path+'/'+ALIGNMENTS_FNAME+'-'+str(chunk), 'w')
    else: out_alignments = open(out_path+'/'+ALIGNMENTS_FNAME, 'w')
    if ungapped==False: mismatches=ed_limit

    
    i=0
    for alignments in strand_alignments:
        i+=1
        if methylation: logger.info('Analyzing edit distance (4-letter nt alphabet) and methylation - strand %d of %d'%(i, len(strand_alignments)))
        else: logger.info('Analyzing edit distance (4-letter nt alphabet) - strand %d of %d'%(i, len(strand_alignments)))
        
	fragments=dict()
	nb_alg=0
	#print '\n[Debug] Alignments in 3-letter nt alphabet', len(alignments.keys())
	temp_found=0; temp_mapped=0 #for debug
	
	found = dict(zip(range(2), [False]*len(range(2))))
	read_seq_len = dict(zip(range(2), [None]*len(range(2))))
	#try:
	if True:
	  for pair_id in alignments.keys():
	      found = dict(zip(range(2), [False]*len(range(2))))
	      position = dict(zip(range(2), [None]*len(range(2))))
	      strand = dict(zip(range(2), [None]*len(range(2))))
	      strand_fa = dict(zip(range(2), [None]*len(range(2))))
	      seq_id = dict(zip(range(2), [None]*len(range(2)))) 
	      f_id = None #dict(zip(range(2), [None]*len(range(2))))
	      f_s = dict(zip(range(2), [None]*len(range(2))))
	      f_e = dict(zip(range(2), [None]*len(range(2))))
	      cigar = dict(zip(range(2), [None]*len(range(2)))) 
	      tmp_fs=0
	      prev_sc=[0,0]
	      prev_ii=0
	      for read in range(2):#reads.values():
		if ((read==0) or (read==1 and found[0]==True)):
		  position[read] = alignments[pair_id][0]['position'][read]
		  strand[read] = alignments[pair_id][0]['strand'][read]
		  strand_fa[read] = alignments[pair_id][0]['strand_fa'][read]
		  seq_id[read] = alignments[pair_id][0]['seq_id'][read].zfill(4)# note that only an alignment for a read can exists (ambiguous have been removed)
		
		  if rrbs:
		    if i%2==1: fname = indexes_path+seq_id[read]+'_'+FRAGMENTS_FNAME_F
		    else: fname = indexes_path+seq_id[read]+'_'+FRAGMENTS_FNAME_R
		  nb_alg+=1
		  
		  cigar[read] = alignments[pair_id][0]['cigar'][read]
		  cigar_op = 'MIDNSHP=X'
		  p_cigar_op = dict([(j, cigar[read][j]) for j in range(len(cigar[read])) if cigar[read][j] in cigar_op])

		  indels = ('I' in cigar[read]) or ('D' in cigar[read]) or ('S' in cigar[read])
		  
		  
		  if (i%2==1): 
		    if read==0: read_seq = valid_mapped_reads[read][pair_id]['read'].upper()
		    else: read_seq = reverse_compl(valid_mapped_reads[read][pair_id]['read'].upper())
		  else: 
		    if read==0: read_seq = reverse_compl(valid_mapped_reads[read][pair_id]['read'].upper())
		    else: read_seq = valid_mapped_reads[read][pair_id]['read'].upper()
		  
		  if not rrbs:
		    if read==0: reference_long = reference_seqs[seq_id[read]][position[read]-2-1:position[read]+len(read_seq)+2-1].upper()
		    else: reference_long = reference_seqs[seq_id[read]][position[read]-2-1:position[read]+len(read_seq)+2-1].upper()
		  else:
		    if i%2==1: k='FW'
		    else: k='RC'
		    
		    if read==0: reference_long = reference_seqs[seq_id[read]][k][position[read]-2-1:position[read]+len(read_seq)+2-1].upper()
		    else: reference_long = reference_seqs[seq_id[read]][k][position[read]-2-1:position[read]+len(read_seq)+2-1].upper()
		      
		  reference = reference_long[2:-2]
		    
		    
		    
		  offset=0
		  k = 0 # cigar string shift index
		  idx_r = 0 # read sequence shift index
		  idx_R = 0 # reference sequence shift index
		  
		  reference_no_clip=''
		  soft_clipped=[0,0]
		  
		  read_seq_len[read]=len(read_seq)
		  ii=0
		  if indels:
		  
		    tmp_read_seq=''
		    tmp_reference=''
		    #soft_clipped=[None,None]
		    
		    k = 0 # cigar string shift index
		    idx_r = 0 # read sequence shift index
		    idx_R = 0 # reference sequence shift index
		    for j in sorted(p_cigar_op.iterkeys()):
			step = int(cigar[read][k:j])
			if (p_cigar_op[j]=='I'):# insertion
			    tmp_reference+='-'*step
			    tmp_read_seq+=read_seq[idx_r:idx_r+step]
			    idx_r+=step
			    offset+=step
			    ii+=step
			elif (p_cigar_op[j]=='S'): # soft clipping
			    offset+=step	  
			    if j==len(cigar)-1: # end clipping
			      soft_clipped[1]=step
			      tmp_reference+=reference[idx_R:idx_R+step]
			      tmp_read_seq+=read_seq[idx_r:idx_r+step]
			      idx_r+=step
			      idx_R+=step
			    else: 
			      soft_clipped[0]=step # front clipping
			      if i%2==1:
				tmp_reference+=reference[idx_R:idx_R+step]
				tmp_read_seq+=read_seq[idx_r:idx_r+step]
				idx_r+=step
				idx_R+=step
			      else:
				tmp_read_seq+=read_seq[idx_r:idx_r+step]
				idx_r+=step  
			elif p_cigar_op[j]=='D': # deletion
			    tmp_read_seq+='-'*step
			    tmp_reference+=reference[idx_R:idx_R+step]
			    idx_R+=step
			    ii-=step
			else: # match or mismatch
			    tmp_read_seq+=read_seq[idx_r:idx_r+step]
			    tmp_reference+=reference[idx_R:idx_R+step]
			    idx_r+=step
			    idx_R+=step
			k = j+1
		  
		    if soft_clipped[0]!=None: 
		      tmp_read_seq=tmp_read_seq[soft_clipped[0]:]
		    if soft_clipped[1]!=None:
		      if i%2==1:
			tmp_read_seq=tmp_read_seq[:-soft_clipped[1]]
			if (soft_clipped[0]==None): soft_clipped[0]=0
			tmp_reference=tmp_reference[:-soft_clipped[1]-soft_clipped[0]]
		      else:
			tmp_read_seq=tmp_read_seq[:-soft_clipped[1]]
			tmp_reference=tmp_reference[:-soft_clipped[1]] 
			      
		    read_seq=tmp_read_seq
		    reference_no_clip=reference
		    reference=tmp_reference
		    
		  else: reference_no_clip = reference
		    
		  
		  if rrbs:
		    if i%2==1: fname = indexes_path+seq_id[read]+'_'+FRAGMENTS_FNAME_F
		    else: fname = indexes_path+seq_id[read]+'_'+FRAGMENTS_FNAME_R
		      
		  if (i%2==1): 
		    if read==0: n_mis = calc_mismatches(read_seq, reference) 
		    else:n_mis = calc_mismatches(read_seq, reference)#, 'AG') 
		  else: 
		    if read==0: n_mis = calc_mismatches(read_seq, reference, 'AG')
		    else: n_mis = calc_mismatches(read_seq, reference, 'AG')
		        
		  if (n_mis!=None and n_mis <= mismatches):
		    if read==1: temp_mapped+=1
		    found[read]=True
		    if rrbs:
		      if not fragments.has_key(seq_id[read]):
			fragments_f = open(fname, 'rb')
			fragments[seq_id[read]] = marshal.load(fragments_f)
			fragments_f.close() 
		      
		      if i%2==1: 
			if read==0: 
			  f_s[read] = position[read]
			  tmp_fs = position[read]
			else:
			  f_s[read] = position[read] + len(read_seq)
		      else:
			if read==0: 
			  f_s[read] = position[read] + len(read_seq) - len(red_site[red_site.find('-')+1:]) #- offset
			  tmp_fs = position[read]
			else:
			  f_s[read] = position[read] 
		      try:
			if i%2==1:
			  if read==0:
			    f_id = fragments[seq_id[read]][f_s[read]][2]
			    f_e[read] = fragments[seq_id[read]][f_s[read]][1]
			    f_s[read] = fragments[seq_id[read]][f_s[read]][0]
			    position[read] = f_s[read]
			  else:
			    f_e[read]=f_s[0]
			    real_frag_size = f_e[0]-f_s[0]
			    detected_frag_size = position[read] - tmp_fs + read_seq_len[read] - ii - soft_clipped[0]
			    if detected_frag_size == real_frag_size:
			      position[read] = f_e[0] -  read_seq_len[1]
			      f_e[read]=f_s[0]
			      found[read]=True
			    else: 
			      found[read]=False
			else:
			  if read==0:
			    f_id = fragments[seq_id[read]][f_s[read]][2]
			    f_e[read] = fragments[seq_id[read]][f_s[read]][0]
			    f_s[read] = fragments[seq_id[read]][f_s[read]][1]
			    position[read] = f_s[read]
			    prev_sc = soft_clipped
			    prev_ii = ii
			  else:
			    f_e[read]=f_s[0]
			    real_frag_size = f_e[0]-f_s[0]
			    detected_frag_size = tmp_fs - position[read] + read_seq_len[0] + 1 - prev_sc[0] - prev_ii
			    if detected_frag_size==real_frag_size:
			      position[read] = f_e[0] - read_seq_len[1]#len(read_seq)
			      f_e[read]=f_s[0]
			      found[read]=True
			    else: 
			      found[read]=False  
		      except:
			found[read]=False; 
			temp_found+=1; #for debug
			temp_mapped-=1
		    
	      if found[0] and found[1]:
		  if not n_alignments.has_key(n_mis): n_alignments[n_mis]=0
		  n_alignments[n_mis]+=1
		  
		  insert_size = position[1] + len(read_seq) - position[0]
		  
		  if i%2==1: k='FW'
		  else:  k='RC'
		  
		  if not rrbs:
		    reference_longx = reference_seqs[seq_id[read]][position[read]-2-1:position[read]+len(read_seq)+2-1].upper()
		  else:
		    reference_longx = reference_seqs[seq_id[read]][k][position[read]-2-1:position[read]+len(read_seq)+2-1].upper()
		      
		  methylation_seq = '' # by default no methylation level are calculated
		  if methylation: methylation_seq = methylation_levels(read_seq, reference_longx)
		  
		  fread_id_1 = valid_mapped_reads[0][pair_id]['header'].split()[0]
		  fread_id_1 = fread_id_1*(fread_id_1[0]!='@') + fread_id_1[1:]*(fread_id_1[0]=='@')
		  
		  fread_id_2 = valid_mapped_reads[1][pair_id]['header'].split()[0]
		  fread_id_2 = fread_id_2*(fread_id_2[0]!='@') + fread_id_2[1:]*(fread_id_2[0]=='@')
		    
		  if rrbs:		    
		    out_alignments.write(fread_id_1 + '\t' + FLAG[i]+'\t' + ref_names_conv[seq_id[0]].zfill(4) + '\t' + str(position[0]) + '\t' + '255' + '\t' + cigar[0]+ '\t' + ref_names_conv[seq_id[1]]  + '\t'+ str(position[1]) + '\t' + '0' + '\t' + str(insert_size)+ '\t' + reference + '\t' + '*' + '\t' + 'NM:i:'+str(n_mis) + '\t' + 'XM:Z:'+methylation_seq + '\t' + 'XR:Z:'+XR[i-1] + '\t' + 'XG:Z:'+XG[i-1] + '\t' + 'YF:'+str(f_id) + '\t' + 'YS:'+str(f_s[0]) + '\t' + 'YE:'+str(f_e[0]) + '\n') 
		    
		    out_alignments.write(fread_id_2 + '\t' + FLAG[i]+'\t' + ref_names_conv[seq_id[1]].zfill(4) + '\t' + str(position[1]) + '\t' + '255' + '\t' + cigar[1]+ '\t' + ref_names_conv[seq_id[0]]  + '\t'+ str(position[0]) + ' ' + '0' + '\t' + '-'+str(insert_size) + '\t' + reference + '\t' + '*' + '\t' + 'NM:i:'+str(n_mis) + '\t' + 'XM:Z:'+methylation_seq + '\t' + 'XR:Z:'+XR[i-1] + '\t' + 'XG:Z:'+XG[i-1] + '\t' + 'YF:'+str(f_id) + '\t' + 'YS:'+str(f_s[1]) + '\t' + 'YE:'+str(f_e[1]) + '\n') 		
		  else:
		    out_alignments.write(fread_id_1 + '\t' + FLAG[i]+'\t' + ref_names_conv[seq_id[0]].zfill(4) + '\t' + str(position[0]) + '\t' + '255' + '\t' + cigar[0]+ '\t' + ref_names_conv[seq_id[1]]  + '\t'+ str(position[1]) + '\t' + '0' + '\t' + str(insert_size)+ '\t' + reference + ' ' + '*' + '\t' + 'NM:i:'+str(n_mis) + '\t' + 'XM:Z:'+methylation_seq + '\t' + 'XR:Z:'+XR[i-1] + '\t' + 'XG:Z:'+XG[i-1] + '\n') 
		    
		    out_alignments.write(fread_id_2 + '\t' + FLAG[i]+'\t' + ref_names_conv[seq_id[1]].zfill(4) + '\t' + str(position[1]) + '\t' + '255' + '\t' + cigar[1]+ '\t' + ref_names_conv[seq_id[0]]  + '\t'+ str(position[0]) + '\t' + '0' + '\t' +  '-'+str(insert_size) + '\t' + reference + '\t' + '*' + '\t' + 'NM:i:'+str(n_mis) + '\t' + 'XM:Z:'+methylation_seq + '\t' + 'XR:Z:'+XR[i-1] + '\t' + 'XG:Z:'+XG[i-1] + '\n') 	
		      
        #except Exception, err:  print '[Debug]', err #pass
        #print '[Debug] Mapped:', temp_mapped
        #print '[Debug] Fragments not found:', temp_found
        #print '\n'
    return n_alignments


def four_nt_analysis(strand_alignments, reference_seqs, library, methylation, mismatches, bs_reads_fname, out_path, n, ed_limit, ungapped, rrbs, ref_names_conv, indexes_path, red_site, single_end, chunk, chunks, w_ambiguous, end_to_end, logger):
  if single_end: 
    return four_nt_analysis_single(strand_alignments, reference_seqs, library, methylation, mismatches, bs_reads_fname, out_path, n, ed_limit, ungapped, rrbs, ref_names_conv, indexes_path, red_site, chunk, chunks, w_ambiguous, end_to_end, logger)
  return  four_nt_analysis_paired(strand_alignments, reference_seqs, library, methylation, mismatches, bs_reads_fname, out_path, n, ed_limit, ungapped, rrbs, ref_names_conv, indexes_path, red_site, chunk, chunks, end_to_end, logger)
  

def split_file(filename, chunk=4*10**6):
    fns={}
    i=0
    with open(filename, 'r') as datafile:
        groups = groupby(datafile, key=lambda k, line=count(): next(line) // chunk)
        for k, group in groups:
	    with open(filename+'-'+str(i).zfill(2), 'w') as outfile:
                outfile.write(''.join(group))
                fns[k]=outfile.name   
            i+=1
    #return fns                     

result=list()
def add_result(value):
  result.append(value)

   
def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func



# main
#if __name__ == "__main__":
def GPUBSMaligner():

    from optparse import OptionParser
    parser = OptionParser()

    #------------------------------------------#
    #            Set options                   #
    #------------------------------------------#
    parser.set_defaults(infilename=None)
    parser.add_option("-s", "--reads", dest="infilename",help="The query file (FASTA or FASTQ format) [For alignments of single-end reads]", metavar="FILE")

    parser.set_defaults(infilename1=None)
    parser.add_option("-1", "--reads1", dest="infilename1",help="A query file (FASTA or FASTQ format) [For alignments of paired-end reads]", metavar="FILE")

    parser.set_defaults(infilename2=None)
    parser.add_option("-2", "--reads2", dest="infilename2",help="A query file (FASTA or FASTQ format)[For alignments of paired-end reads]", metavar="FILE")

    parser.set_defaults(soap3path="~/soap3/")
    parser.add_option("-S", "--soap3", dest="soap3path",help="The path of SOAP3-dp [~/soap3-dp/]", metavar="PATH")

    parser.set_defaults(minInsertSize=20)
    parser.add_option("-v", "--min_insert_size:", dest="minInsertSize", help="Minimum value of insert size [For alignments of paired-end reads]")
    
    parser.set_defaults(maxInsertSize=500)
    parser.add_option("-u", "--max_insert_size:", dest="maxInsertSize", help="Maximum value of insert size [For alignments of paired-end reads]")

    parser.set_defaults(dbpath="indexes/")
    parser.add_option("-i", "--indexes_path", dest="indexes_path", help="The directory of the indexes (generated in preprocessing genome) [indexes/]", metavar="PATH")

    #parser.set_defaults(mismatches='-1')
    parser.set_defaults(mismatches='5')
    parser.add_option("-m", "--mismatches", dest="mismatches", help="Maximum number of mismatches allowed [default 5]", metavar="INT") #. Do not use this option to take into account indels in the 

    parser.set_defaults(mis_soap3='0')
    parser.add_option("--mis_soap3", dest="mis_soap3", help="Use this option to set the maximum number of mismatches allowed in the first step of SOAP3-dp [0-4].", metavar="INT") #. Do not use this option to take into account indels in the 
    
    parser.add_option("--e2e", dest="end_to_end", action='callback', callback=optional_arg('empty'), help="Use this option to disable soft clipping.")
    
    parser.set_defaults(type_of_hits='1')
    parser.add_option("-H", "--hits", dest="type_of_hits", help="All valid alignments: 1 - All best alignments: 2 - Unique best alignments: 3 (DEAULT)")

    parser.set_defaults(max_hits='2')
    parser.add_option("--max_hits", dest="max_hits", help="Maximum number of outputs allowed for each read for read alignment [2].")
    
    parser.set_defaults(m_s='1')
    parser.add_option("--m_s", dest="m_s", help="It defines the score for match [1].")
    
    parser.set_defaults(ms_s='-3')
    parser.add_option("--ms_s", dest="ms_s", help="It defines the score for mismatch [-3].")
    
    parser.set_defaults(go_s='-4')
    parser.add_option("--go_s", dest="go_s", help="It defines the score for opening a gap [-4].")
    
    parser.set_defaults(ge_s='-1')
    parser.add_option("--ge_s", dest="ge_s", help="It defines the score for extending a gap [-1].")
    
    parser.set_defaults(max_fl_clip=None)
    parser.add_option("--max_fl_clip", dest="max_fl_clip", help="It defines the maximum length allowed from the front of the read to be clipped (for ungapped mode only)")
    parser.set_defaults(max_el_clip=None)
    parser.add_option("--max_el_clip", dest="max_el_clip", help="It defines the maximum length allowed from the end of the read to be clipped (for ungapped mode only)")
    
    parser.set_defaults(library=1) 
    parser.add_option("-l", "--library", dest="library", help="BS read protocol: 1 for directional and 2 for non directional")

    parser.add_option("-R", "--rrbs", dest="rrbs", action='callback', callback=optional_arg('empty'), help="Use this option for RRBS data")
    
    parser.set_defaults(red_site="C-CGG")
    parser.add_option("-d", "--red_site", dest="red_site",help="Use this option to set the restriction enzime: e.g., C-CGG for MspI digestion, T-CGA for TaqI digestion (only for RRBS data). [C-CGG]", metavar="STR")
    
    parser.set_defaults(length=120)
    parser.add_option("-L", "--length", dest="length", help="Length of the longest read in the query file [120]")
    
    parser.add_option("-M", "--methylation", dest="methylation", action='callback',callback=optional_arg('empty'), help="Use this option to calculate methylation levels")

    #parser.set_defaults(n_reads=-1)
    #parser.add_option("-N", "--max_reads", dest="n_reads", help="Use this option to analyze the reads in chunks of N items. Use -1 By default GPU-BSM does not split the reads.", metavar="INT")
    parser.set_defaults(n_reads=10000000)
    parser.add_option("-N", "--max_reads", dest="n_reads", help="Use this option to analyze the reads in chunks of N items [10000000]. ", metavar="INT")
    
    parser.set_defaults(adapters=None)
    parser.add_option("-A", dest="adapters", action="append", help="Adapter sequence(s) to be removed form 3' of the reads. Adapters are trimmed using cutadapt. By default adapter trimming is not performed")
    
    parser.set_defaults(job_id=None)
    parser.add_option("-o", "--output", dest="job_id", help="Output files will be writed into this directory. If not specified, GPU-BSM automatically generates a job identifier and then creates an output directory using as name the job identifier. It the directory exists, GPU-BSM does not overwrite it.")
        
    parser.set_defaults(adp_error_rate=0.1)
    parser.add_option("-e", dest="adp_error_rate", help="Maximum allowed error rate for adapters (default: 0.1)")

    parser.set_defaults(adp_overlap=3)
    parser.add_option("-O", "--overlap", dest="adp_overlap", help="Minimum overlap length. If the overlap between the read and the adapter is shorter than LENGTH, the read is not modified.This reduces the no. of bases trimmed purely due to short random adapter matches (default: 3).")

    parser.add_option("-a", "--ambiguous", dest="w_ambiguous", action='callback', callback=optional_arg('empty'), help="Use this option to not remove ambiguous mapped reads")
    
    parser.add_option("--dp", dest="dp", action='callback', callback=optional_arg('empty'), help="Use only dynamic programming to look for both gapped and ungapped alignments")
    
    parser.add_option("--ungapped", dest="ungapped", action='callback', callback=optional_arg('empty'), help="Use this option to look only for ungapped alignments")
    
    parser.add_option("-g", "--gpu", dest="gpu", default=[], help="Use this option to specify the gpu(s) identifier. If not specified GPU-BSM uses up to four GPU cards.", action='append', metavar='RECIPIENT')
    
    parser.set_defaults(n_threads="1")
    #parser.add_option("-p", dest="n_threads", help="Use this option to use multiple CPU-cores.", metavar="INT")

    
    
    #------------------------------------------#
    #            Check options                 #
    #------------------------------------------#
    (options, args) = parser.parse_args()
    parser.parse_args(args)
    try:
        # bs treated reads - for single-end alignments
        reads_file = options.infilename
        # bs treated reads - for pair-end alignments
        reads_file1 = options.infilename1
        reads_file2 = options.infilename2
        
        rrbs = False
        if options.rrbs: rrbs = True
        red_site=options.red_site

        single_end = is_single_end(reads_file, reads_file1, reads_file2) #single_end is True for single-end alignment, it is False for pair-end alignments

        if single_end: check_file(reads_file)
        else:
            check_file(reads_file1)
            check_file(reads_file2)

        # bs read library (Lister or Cokus)  
        library = options.library
        library = int(library)
        check_BS_protocol(library)

        # looking for GPUs 
        n_dev = count_devices()
        gpu_id = []
	for dev_id in options.gpu:
	  gpu_id.append(check_gpu_id(dev_id, n_dev))
	  
        if len(gpu_id)==0:
            gpu_id = get_devices(n_dev, library)

	
	# looking for CPU-cores
	n_threads = options.n_threads
	n_threads = check_threads_option(n_threads)

        if single_end==False:
            maxInsertSize = options.maxInsertSize
            minInsertSize = options.minInsertSize
            if (maxInsertSize==None or minInsertSize==None): raise InsertSizeException()
            maxInsertSize = int(maxInsertSize)
            minInsertSize = int(minInsertSize)

        # soap3-dp (first step) allowed mismatches
        mis_soap3 = check_soap3_mismatches(options.mis_soap3)
        # nb of mismatches
        mismatches = check_mismatches(options.mismatches)
        
        length = options.length
        length = int(length)
	
        m_s, ms_s, go_s, ge_s = check_alignment_scores(options.m_s, options.ms_s, options.go_s, options.ge_s)
        
        if options.max_fl_clip==None: max_fl_clip=int(length*0.7)
        else: max_fl_clip=options.max_fl_clip
        if options.max_el_clip==None: max_el_clip=int(length*0.7)
        else: max_el_clip=options.max_el_clip
        max_fl_clip, max_el_clip = check_clipping(max_fl_clip, max_el_clip)
        
        type_of_hits = check_type_of_hits(options.type_of_hits)

        methylation=False
        if options.methylation: methylation=True 

        w_ambiguous=False
        if options.w_ambiguous: w_ambiguous=True
        
        dp=False
        if options.dp: dp=True
        
        ungapped=False
        if options.ungapped: ungapped=True
        
        if (ungapped and dp): raise MappingStrategyException()
  
	ed_limit = mismatches
	
        n_reads = check_n_reads(options.n_reads)
        
        try:
	  adp_error_rate=float(options.adp_error_rate)
	  if adp_error_rate<0 or adp_error_rate>1: raise ADPErrorRateTypeException()
	except ValueError: raise ADPErrorRateTypeException()
	
	adapters=options.adapters
	if adapters!=None:
	  if library==2 and len(adapters)==1: raise AdaptersOptionException()
	
	try:
	  adp_overlap=int(options.adp_overlap) 
	  if adp_overlap<0: raise ADPOverlapTypeException()
	except ValueError: raise ADPOverlapTypeException()
	
	# the path of SOAP3-dp
        soap3_path = options.soap3path
        soap3_path = str(soap3_path)
        if soap3_path[-1] !="/": soap3_path = soap3_path+"/"
        check_dir(soap3_path) # check if the path exists

	max_hits = check_max_hits(options.max_hits)
	
        if dp: mis_soap3='0'
        if ungapped: mis_soap3='4'
        change_soap3_ini_file(soap3_path, mis_soap3, dp, max_hits, options.end_to_end, m_s, ms_s, go_s, ge_s, max_fl_clip, max_el_clip) # change Soap3MisMatchAllow and SkipSOAP3Alignment settings in the soap3.ini file

        # the path of the indexes previously calcutated for the reference genome
        indexes_path = options.indexes_path
        indexes_path = str(indexes_path)
        if indexes_path[-1] !="/": indexes_path = indexes_path+"/"
        check_dir(indexes_path)
        
    except IOError:
        print '[ERROR] File %s does not exist'%(reads_file)
        exit()
    except BSProtocolError:
        print '[ERROR] BS treated reads protocol not supported: 1 for Lister - 2 for Cokus'
        parser.print_help()
        exit()
    except SOAP3MismatchesError:
        print '[ERROR] SOAP3-dp allows up to 4 mismatches at its first alignment step'
        parser.print_help()
        exit()
    except SOAP3MisOptionTypeException:
	print '[ERROR] Use an integer value for --mis_soap3 option'
        parser.print_help()
        exit()
    except DirectoryError, err:
        print '[ERROR] ', err
        exit()
    except InsertSizeException:
        print '[ERROR] Use option -u and -v for maxInsertSize and minInsertSize'
        parser.print_help()
        exit()
    except QueryException:
        print '[ERROR] Use option -s for single-end alignment or options -1 and -2 for pair-end alignment'
        parser.print_help()
        exit()
    except GPUOptionTypeException:
        print '[ERROR] Use an integer value for -g option'
        parser.print_help()
        exit()
    except InvalidGPUidException:
        print '[ERROR] Invalid GPU identifier for -g option'
        exit()
    except ClippingOptionTypeException:
	print '[ERROR] Use an integer value for --max_fl_clip and --max_el_clip options'
        parser.print_help()
        exit()
    except ThreadsOptionTypeException:
        print '[ERROR] Use an integer value for -p option'
        parser.print_help()
	exit()     
    except NReadsOptionTypeException:
	print '[ERROR] Use an integer value for -N option'
        parser.print_help()
	exit()     
    except HitsOptionTypeException:
        print '[ERROR] Use an integer value for -H option'
        parser.print_help()
        exit()
    except MaxHitsOptionTypeException:    
        print '[ERROR] Use an integer value for -h option'
        parser.print_help()
        exit()
    except InvalidHitsOptionException:
        print '[ERROR] Invalid value for -H option'
        parser.print_help()
        exit()
        
    except MatchScoreOptionTypeException:
        print '[ERROR] Use an integer value for --m_s option'
        parser.print_help()
        exit()    
    except MismatchScoreOptionTypeException:
        print '[ERROR] Use an integer value for --ms_s option'
        parser.print_help()
        exit()    
    except GapOpenScoreOptionTypeException:
        print '[ERROR] Use an integer value for --go_s option'
        parser.print_help()
        exit()    
    except GapExtendScoreOptionTypeException:
        print '[ERROR] Use an integer value for --ge_s option'
        parser.print_help()
        exit()     
    except MismatchesOptionTypeException():
        print '[ERROR] Use an integer value for -m option'
        parser.print_help()
        exit()
    except MismatchesOptionException():
        print '[ERROR] Invalid value for -m option'
        parser.print_help()
        exit()
    except EDLimitOptionTypeException():
        print '[ERROR] Use an integer value for -I option'
        parser.print_help()
        exit()
    except EDLimitOptionException():
        print '[ERROR] Invalid value for -I option. Only positive values.'
        parser.print_help() 
        exit()
    except MappingStrategyException():
        print '[ERROR] Options --dp and --ungapped cannot be used together.'
        parser.print_help()
        exit()    
    except ADPErrorRateTypeException():
        print '[ERROR] Invalid value for -e option.'
        parser.print_help() 
        exit()
    except ADPOverlapTypeException():  
	print '[ERROR] Invalid value for -O option.'
        parser.print_help() 
        exit()
    except AdaptersOptionException():
        print '[ERROR] Set two adapter sequences for pair-end sequencing.'
        parser.print_help() 
        exit()
    except Exception, err:
        print '[ERROR] ', err
        parser.print_help()
        exit()

    #------------------------------------------#
    #            Set logger                    #
    #------------------------------------------#
    job_id = options.job_id
    if job_id==None:
      job_id = str(random.randint(1000000,9999999)) # a job identifier
      out_path ='output/'
      ensure_dir(out_path)
      out_path = out_path + job_id
      os.mkdir(out_path) # the directory where results are stored
    else:
      out_path = job_id
      try:
	create_path(out_path)
      except DirectoryError, err:
	print '[ERROR] ', err
        exit()
      
    log_path = out_path + '/' + 'log' + '.log' # log file
    
    logger = get_logger(log_path)
    logger.info('\n# ---------- Summarizing parameters ---------- #\n')
    logger.info('**************************************************\n')
    logger.info('BS reads filename: %s'%(reads_file))
    logger.info('%s data'%((rrbs==False) and 'WGBS' or 'RRBS'))
    logger.info('%s library'%((library==1) and 'Directional' or 'Non directional'))
    logger.info('SOAP3-dp path: %s'%(soap3_path))
    logger.info('Reference genome indexes [path]: %s'%(indexes_path))
    logger.info('Maximum allowed mismatches: %s'%(mismatches))
    logger.info('SOAP3-dp alignments that will be analyzed: %s'%({1:'all valid alignments', 2:'all best alignments', 3:'unique best alignments'}[type_of_hits]))
    logger.info('%s devices installed'%(n_dev))
    logger.info('%s GPU(s) will be exploited for analysis'%(len(gpu_id)))
    logger.info('%s parallel threads will be launched'%(n_threads))
    logger.info('GPU(s) identified by the following ID(s) %s will be used'%(gpu_id))
    logger.info('Indels support: %s '%((ungapped==False and 'True' or 'False')))
    logger.info('Adapter sequences %s'%(adapters))
    logger.info('Max hits per read %s'%(max_hits))
    logger.info('Skip SOAP3 when look for gapped alignments: %s '%((dp==True and 'True' or 'False')))
    logger.info('**************************************************\n')
    
    #------------------------------------------#
    #            Start the job                 #
    #------------------------------------------#
    start_time = time.time()
    #logger.info('Job # %s started\n'%(job_id))
    logger.info('Job started\n')
    logger.info('Results will be stored in the %s directory'%(out_path))
    logger.info('**************************************************\n')


    # create temporary files to store the reads converted according to the adopted protocol
    reads_fnames = converted_reads_files(reads_file, reads_file1, reads_file2, library, single_end, out_path)
    logger.info('The following temporary files %s have been created'%(reads_fnames.values()))
    
    # detect the format of the query (FASTQ/FASTA)
    try:
        if single_end: query_format=detect_query_format(reads_file)
        else:
            query_format=detect_query_format(reads_file1)
            if query_format!=detect_query_format(reads_file2): raise MultiQueryFormatException()
    except QueryFormatException:
        logger.error('Query type not supported')
        sys.exit(0)
    except MultiQueryFormatException:
        logger.error('Query files of different type')
        sys.exit(0)

    #------------------------------------------#
    #          Trimming adapters reads         #
    #------------------------------------------#
    
    if adapters!=None:
      logger.info('Removing adapter sequences')
      if library==1:
	dir_name, fname = os.path.split(reads_file)
	base_fname = os.path.splitext(fname)[0]
	out_reads_file = os.path.join(dir_name, TRIMMED_FILE_PREFIX+fname)
	info_file = out_path+'/'+base_fname+'_cutadapt.info'
	logger.info('Statistics will be stored in %s'%(info_file))
	#shutil.copyfile(reads_file, out_reads_file)
	remove_adapters(adapters[0], reads_file, out_reads_file, info_file, adp_overlap, adp_error_rate)
	reads_file = out_reads_file     
      else: 
	dir_name1, fname1 = os.path.split(reads_file1)
	dir_name2, fname2 = os.path.split(reads_file2)
	base_fname1 = os.path.splitext(fname1)[0]
	base_fname2 = os.path.splitext(fname2)[0]
	out_reads_file1 = os.path.join(dir_name, TRIMMED_FILE_PREFIX+fname1)
	out_reads_file2 = os.path.join(dir_name, TRIMMED_FILE_PREFIX+fname2)
	info_file1 = out_path+'/'+base_fname1+'_cutadapt.info'
	info_file2 = out_path+'/'+base_fname2+'_cutadapt.info'
	logger.info('Statistics will be stored in %s and in %s'%(info_file1, info_file2))
	#shutil.copyfile(reads_file1, out_reads_file1)
	#shutil.copyfile(reads_file2, out_reads_file2)
	if len(adapters)==2:
	  remove_adapters(adapters[0], reads_file1, out_reads_file1, info_file1, adp_overlap, adp_error_rate)
	  remove_adapters(adapters[1], reads_file2, out_reads_file2, info_file2, adp_overlap, adp_error_rate)
	else:
	  remove_adapters(adapters[0], reads_file1, out_reads_file1, info_file1, adp_overlap, adp_error_rate)
	  remove_adapters(adapters[0], reads_file2, out_reads_file2, info_file2, adp_overlap, adp_error_rate)
	reads_file1 = out_reads_file1     
	reads_file2 = out_reads_file2
	
    #------------------------------------------#
    #          Converting bs-reads             #
    #------------------------------------------#
    logger.info('Reads file in %s format'%(query_format))
    logger.info('Converting the reads')
    if single_end: bs_reads_fname = out_path+'/'+'bs_reads'
    else: bs_reads_fname = [out_path+'/'+'bs_reads_1', out_path+'/'+'bs_reads_2']
    if single_end:
        nb_reads = reads_conversion_single_end(reads_fnames, reads_file, query_format, out_path, bs_reads_fname, library)
    else: # pair ends
        nb_reads = reads_conversion_paired_end(reads_fnames, reads_file1, query_format, out_path, bs_reads_fname, library, 1) # first read
        reads_conversion_paired_end(reads_fnames, reads_file2, query_format, out_path, bs_reads_fname, library, 2) # second read
    logger.info('%s Reads have been converted'%(nb_reads))
    logger.info('**************************************************\n')
    
    #------------------------------------------#
    #            Split the data                #
    #------------------------------------------#
    if n_reads!=-1: 
      chunks = split_reads_files(reads_fnames, query_format, n_reads) 
      logger.info('Data file(s) splitted')
    else: chunks=0
    partial_results = list()
    rf=reads_fnames.copy() 
    references_loaded = False
    
    for chunk in range(chunks + 1*(n_reads==-1)):
      
      if chunks!=0:
	for fname in rf: reads_fnames[fname]=rf[fname]+'.'+str(chunk).zfill(len(str(chunks)))
	logger.info('Analyzing chunk %d of %d'%(chunk+1, chunks))
	
      #------------------------------------------#
      #          Mapping reads                   #
      #------------------------------------------#
      logger.info('Mapping reads')
      mapping_time = time.time()
      if single_end: map_single_end_reads(soap3_path, indexes_path, reads_fnames, mis_soap3, logger, library, gpu_id, type_of_hits, ungapped, length)
      else: map_pair_end_reads(soap3_path, indexes_path, reads_fnames, mis_soap3, maxInsertSize, minInsertSize, logger, library, gpu_id, type_of_hits, ungapped, length)
      os.system('rm '+ out_path+'/*gout*')
      logger.info('Reads have been mapped in %s sec'%(time.time() - mapping_time))
      logger.info('**************************************************\n')
      
      
      #------------------------------------------#
      #     Removing not uniquely alignments     #
      #------------------------------------------#
      if ungapped==False: valid_mappings=remove_ambiguous(reads_fnames, library, ed_limit, single_end, indexes_path, rrbs, True)
      else: valid_mappings=remove_ambiguous(reads_fnames, library, mismatches, single_end, indexes_path, rrbs, True)
      logger.info('Ambiguous mappings have been removed')
      logger.info('**************************************************\n')
      
      #------------------------------------------#
      #          Post-processing                 #
      #------------------------------------------#
      logger.info('Post-processing phase started')
      reference_seqs={}
      
      
      ref_names_f=open(indexes_path+REF_NAMES_CONVERSION_FNAME, 'rb')
      ref_names_conv = pickle.load(ref_names_f)
      ref_names_f.close()

      
      # load the reference sequences
      reference = open(indexes_path+REFERENCE_FNAME, 'rb')
      reference_seqs = marshal.load(reference)
      reference.close()
      
      n=0
      if not references_loaded:
	sort_seq_names = reference_seqs.keys()
	sort_seq_names.sort() 
	for seq_id in sort_seq_names:#reference_seqs.keys():
	  n+=1
	  seq_name = ref_names_conv[seq_id]
	  if rrbs: logger.info('Reference sequence: %s size: %d bp'%(seq_name, len(reference_seqs[seq_id]['FW'])))
	  else: logger.info('Reference sequence: %s size: %d bp'%(seq_name, len(reference_seqs[seq_id])))
	references_loaded=True  
      
      n_alignments=four_nt_analysis(valid_mappings, reference_seqs, library, methylation, mismatches, bs_reads_fname, out_path, n, ed_limit, ungapped, rrbs, ref_names_conv, indexes_path, red_site, single_end, chunk, chunks, w_ambiguous, options.end_to_end, logger)
      partial_results .append(n_alignments)
      
      logger.info('False positives removed')
      logger.info('**************************************************\n')
    
    n_alignments=dict()
    
    for result in partial_results:
      for err in result:
	if err not in n_alignments: n_alignments[err]=result[err]
	else: n_alignments[err]+=result[err]
    
    get_header(out_path, single_end)
    
    if chunks!=0:
      merge_results=Popen('nohup cat %s %s > %s'%(out_path+'/header', out_path+'/'+ALIGNMENTS_FNAME+'-*', out_path+'/'+ALIGNMENTS_FNAME),shell=True)
      merge_results.wait()
    else:
      merge_results=Popen('nohup cat %s %s > %s'%(out_path+'/header', out_path+'/'+ALIGNMENTS_FNAME, out_path+'/'+ALIGNMENTS_FNAME+'_'),shell=True)
      merge_results.wait()
      rename=Popen('nohup mv %s %s'%(out_path+'/'+ALIGNMENTS_FNAME+'_', out_path+'/'+ALIGNMENTS_FNAME),shell=True)
      rename.wait()
    
    
    logger.info('Results')
    logger.info('BS-reads: \t %d'%(nb_reads))
    if len(n_alignments)!=0: logger.info('Uniquely aligned reads: \t %d'%(reduce(lambda n,m:n+m,n_alignments.values())))
    else: logger.info('Uniquely aligned reads: 0')
    for n_mis in n_alignments.keys():
        if ungapped: logger.info('Alignments with %d mismatches: %d \t'%(n_mis, n_alignments[n_mis]))
        else: logger.info('Alignments with %d differences: %d \t'%(n_mis, n_alignments[n_mis]))

    logger.info('Elapsed time: %s sec'%(time.time() - start_time))

    
    # remove temporary files
    if single_end: os.remove(bs_reads_fname)
    else:
      os.remove(bs_reads_fname[0])
      os.remove(bs_reads_fname[1])
    os.system('rm '+ out_path+'/*tmp*')
    os.system('rm '+ out_path+'/header')
    if chunks!=0: os.system('rm '+  out_path+'/'+ALIGNMENTS_FNAME+'-*')


    
