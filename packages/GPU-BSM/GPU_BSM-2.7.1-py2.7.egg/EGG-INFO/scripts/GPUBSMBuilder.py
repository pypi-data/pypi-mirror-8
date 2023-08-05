
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


import fileinput
import string
import os
import operator
import shelve
import pickle
import marshal
import time
import subprocess
from utilities import *
from subprocess import Popen
from optparse import OptionParser


def get_re_sites(sequence, red_site):
  '''
  Look for restriction enzime sites
  '''
  site_pos=list()
  for i in range(len(sequence) - len(red_site)):
    if sequence[i:i+len(red_site)]==red_site: site_pos.append(i)
  return site_pos

def get_DNA_fragments(site_pos, min_len_rrseq, max_len_rrseq, red_site_info):
  '''
  Look for valid DNA fragments 
  '''
  valid_fragments={'FW':list(), 'RC': list()} # coordinates of the fragments in the original reference
  new_positions=list() # updated coordinates in the reduced representation of the reference
  first_fragment=True
  for i in range(len(site_pos)-1): 
    fragment_len = site_pos[i+1]-site_pos[i]
    if fragment_len>=min_len_rrseq and fragment_len<=max_len_rrseq: 
      if first_fragment:
	valid_fragments['FW'].append((site_pos[i]+red_site_info[0], site_pos[i+1]))
	valid_fragments['RC'].append((site_pos[i]+red_site_info[0], site_pos[i+1]))
	first_fragment=False
      else: 
	valid_fragments['FW'].append((site_pos[i]+red_site_info[0]+1, site_pos[i+1]))
	valid_fragments['RC'].append((site_pos[i]+red_site_info[0], site_pos[i+1]))
      
  del site_pos
  return valid_fragments
  

def mask_sequence(sequence, DNA_fragments, red_site_info):
  '''
  Mask invalid DNA regions
  '''
  nb_fragment=0
  masked=''
  fragment=''
  watch=True
  
  for i in range(len(sequence)):
    if nb_fragment<=len(DNA_fragments)-1:
      if nb_fragment>0 and watch:
	if DNA_fragments[nb_fragment][0]==DNA_fragments[nb_fragment-1][1]: 
	  masked+=sequence[i]
	  fragment+=sequence[i]
	  watch=False
      if i>=DNA_fragments[nb_fragment][0] and i<=DNA_fragments[nb_fragment][1]:
	masked+=sequence[i]
	fragment+=sequence[i]
      if i==DNA_fragments[nb_fragment][1]: 
	nb_fragment+=1; fragment=''; watch=True 
  return masked

  
def resolve_dig_sites(dig_rep):
  '''
  Generate digestion sequences according to the IUPAC encoding
  '''
  sites=[' ']
  seq=dig_rep[0]
  for n in seq:
    rep = IUPAC(n)
    tmp = sorted(sites*len(rep))
    i=0
    for j in range(len(tmp)):
      if i==len(rep):i=0
      tmp[j]=tmp[j]+rep[i]
      i+=1
    sites=tmp
  for i in range(len(sites)): sites[i]=sites[i].strip()
  return sites

def get_DNA_fragments_masked_sequence(DNA_fragments):
  DNA_fragments_masked_seq = list()
  try:  
    DNA_fragments_masked_seq.append((1, DNA_fragments[0][1]-DNA_fragments[0][0]+1))
    for i in range(len(DNA_fragments)):
      if i>0:
	DNA_fragments_masked_seq.append((DNA_fragments_masked_seq[i-1][1], DNA_fragments_masked_seq[i-1][1]+DNA_fragments[i][1]-DNA_fragments[i][0]+1))
  except: pass	  
  return DNA_fragments_masked_seq
  
def digestion(sequence, red_sites, min_len_rrseq, max_len_rrseq, logger, header, red_site_info):
  '''
  Cut the sequence according to the RRBS protocol parameters
  '''
  re_sites=list()
  for red_site in red_sites:
    tmp = get_re_sites(sequence, red_site)
    for s in tmp: re_sites.append(s)
  re_sites=sorted(re_sites)
  min_len_rrseq+=red_site_info[1]
  max_len_rrseq+=red_site_info[1]
  DNA_fragments = get_DNA_fragments(re_sites, min_len_rrseq, max_len_rrseq, red_site_info)
  logger.info("Reference sequence: %s - valid DNA fragments: %d "%(header, len(DNA_fragments['FW'])))
  masked_sequence = dict()
  masked_sequence['FW'] = mask_sequence(sequence, DNA_fragments['FW'], red_site_info)
  masked_sequence['RC'] = mask_sequence(sequence, DNA_fragments['RC'], red_site_info)
  DNA_fragments_masked_seq = dict()
  DNA_fragments_masked_seq['FW'] =  get_DNA_fragments_masked_sequence(DNA_fragments['FW'])
  DNA_fragments_masked_seq['RC'] =  get_DNA_fragments_masked_sequence(DNA_fragments['RC'])
  return masked_sequence, DNA_fragments, DNA_fragments_masked_seq

def get_reference(fasta_file, ref_path, logger, red_site, min_len_rrseq, max_len_rrseq, indexes_path, fragments_info, red_site_info, rrbs=False):
    '''
    Load the reference sequence into the memory
    '''

    reference = {}
    sequence = ''
    header = ''
    nb_of_seqs = 0
    refd = shelve.open(ref_path+"refname.shelve",'n')
    
    ref_name_conversions = dict()
        
    all_fragments_f=dict()
    all_fragments_r=dict()
    f_cnt=0
    for line in fileinput.input(fasta_file):
        l=line.split()
        if line[0]!=">":
		sequence=sequence+line[:-1]
        elif line[0]==">":
		if header=='':
                    nb_of_seqs+=1
                    header=l[0][1:]
                    short_header=str(nb_of_seqs).zfill(4)
                    ref_name_conversions[short_header]=header
                else:
		    sequence=sequence.upper()
		    if rrbs: 
		      sequence, fragments, fragments_masked_seq = digestion(sequence, red_site, min_len_rrseq, max_len_rrseq, logger, header, red_site_info)
		      all_fragments_f[short_header]=dict()
		      all_fragments_r[short_header]=dict()
		      f_idx=0 # fragment number identifier
		      for i in range(len(fragments['FW'])):
			
			all_fragments_f[short_header][fragments_masked_seq['FW'][i][0]]=(fragments['FW'][i][0], fragments['FW'][i][1]+red_site_info[1], f_idx)
			all_fragments_r[short_header][fragments_masked_seq['RC'][i][1]]=(fragments['RC'][i][1]+red_site_info[1], fragments['RC'][i][0], f_idx)
			f_idx+=1
			f_cnt+=1
			
			fragments_info.write(str(f_cnt).ljust(40) + header.ljust(40) + str(f_idx).ljust(40) + str(fragments['FW'][i][0]).ljust(40) + str(fragments['FW'][i][1]+red_site_info[1]).ljust(40) + '\n')
		      
                    reference[short_header]=sequence
                    if rrbs:
			logger.info("Reference sequence: %s %d bp"%(header,len(sequence['FW'])))
                    	refd[short_header]=[header,len(sequence['FW'])]
		    else:
			logger.info("Reference sequence: %s %d bp"%(header,len(sequence)))
                    	refd[short_header]=[header,len(sequence)]
                    sequence=''
                    header=l[0][1:]
                    nb_of_seqs+=1
                    short_header=str(nb_of_seqs).zfill(4)
                    ref_name_conversions[short_header]=header
    logger.info("Reference sequence: %s %d bp"%(header,len(sequence)))
    refd[short_header]=[header,len(sequence)]	
    refd.close()
    output = open(indexes_path+REF_NAMES_CONVERSION_FNAME, 'wb')
    pickle.dump(ref_name_conversions, output)
    output.close()
    sequence=sequence.upper()
    if rrbs: 
      sequence, fragments, fragments_masked_seq = digestion(sequence, red_site, min_len_rrseq, max_len_rrseq, logger, header, red_site_info)
      all_fragments_f[short_header]=dict()
      all_fragments_r[short_header]=dict()
      f_idx=0
      for i in range(len(fragments['FW'])):
	all_fragments_f[short_header][fragments_masked_seq['FW'][i][0]]=(fragments['FW'][i][0], fragments['FW'][i][1]+red_site_info[1], f_idx)
	all_fragments_r[short_header][fragments_masked_seq['RC'][i][1]]=(fragments['RC'][i][1]+red_site_info[1], fragments['RC'][i][0], f_idx)
	f_idx+=1
	f_cnt+=1
	fragments_info.write(str(f_cnt).ljust(40) + header.ljust(40) + str(f_idx).ljust(40) + str(fragments['FW'][i][0]).ljust(40) + str(fragments['FW'][i][1]+red_site_info[1]).ljust(40) + '\n')
      f_idx=0
      
			
    if rrbs:
      for seq_id in all_fragments_f.keys():
	fragments_f_fname = indexes_path+seq_id+'_'+FRAGMENTS_FNAME_F
    	fragments_f_file = open(fragments_f_fname,'wb')
    	marshal.dump(all_fragments_f[seq_id], fragments_f_file)
    	fragments_f_file.close()
    
	fragments_r_fname = indexes_path+seq_id+'_'+FRAGMENTS_FNAME_R
	fragments_r_file = open(fragments_r_fname,'wb')
	marshal.dump(all_fragments_r[seq_id], fragments_r_file)
	fragments_r_file.close()
	
    
    reference[short_header]=sequence
    refd.close()
    
    return reference


def conversion(fname, reference, f, t):
    '''
    Convert Cs to Ts or Gs to As in the reference sequences
    f: from
    t: to
    '''
    outf=open(fname,'w')
    for sequence_id in reference.keys():
            outf.write('>%s'%(sequence_id)+"\n")
            sequence=reference[sequence_id]
            sequence=sequence.replace(f, t)
            outf.write('%s'%(sequence)+'\n')
    outf.close()
    
def conversion_rrbs(fname, reference, f, t, strand):
    '''
    Convert Cs to Ts or Gs to As in the reference sequences
    f: from
    t: to
    '''
    outf=open(fname,'w')
    for sequence_id in reference.keys():
            outf.write('>%s'%(sequence_id)+"\n")
            sequence=reference[sequence_id][strand]
            sequence=sequence.replace(f, t)
            outf.write('%s'%(sequence)+'\n')
    outf.close()

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
def GPUBSMbuilder():

    #------------------------------------------#
    #            Set options                   #
    #------------------------------------------#
    parser = OptionParser()
    parser.add_option("-r", "--reference", dest="filename",help="The reference fasta file", metavar="FILE")
    
    parser.add_option("-R", "--rrbs", dest="rrbs", action='callback', callback=optional_arg('empty'), help="Use this option for RRBS data")

    
    parser.set_defaults(red_site='C-CGG')
    parser.add_option("-d", "--red_site", dest="red_site",help="Use this option to set restriction enzime digestion site: e.g., C-CGG for MspI digestion, T-CGA for TaqI digestion (only for RRBS data). [C-CGG]", metavar="STR")
    
    parser.set_defaults(min_len_rrseq=40)
    parser.add_option("-m", dest="min_len_rrseq",help="Minimum DNA fragments length compatible with the RRBS protocol [default: 40]", metavar="INT")
    
    parser.set_defaults(max_len_rrseq=220)
    parser.add_option("-M", dest="max_len_rrseq",help="Maximum DNA fragments length compatible with the RRBS protocol [default: 220]", metavar="INT")
    
    parser.set_defaults(indexes_path="indexes/")
    parser.add_option("-i", "--index_path", dest="indexes_path",help="The directory of the indexes [indexes/]", metavar="PATH")

    parser.set_defaults(soap3path="~/soap3-dp")
    parser.add_option("-S", "--soap3", dest="soap3path",help="The path of SOAP3-dp [~/soap3-dp/]", metavar="PATH")


    #------------------------------------------#
    #            Check options                 #
    #------------------------------------------#
    (options, args) = parser.parse_args()
    if options.filename==None:
        print '[ERROR] Use -f/--file option to specify a reference sequence file.'
        parser.print_help()
        exit()
    try:
        fasta_file=options.filename
        fasta_file=str(fasta_file)
        check_file(fasta_file) # check if the file exists

        indexes_path = options.indexes_path
        indexes_path = str(indexes_path)
        if indexes_path[-1] !="/": indexes_path=indexes_path+"/"
        create_path(indexes_path)# if the directory does not exist it will be created

        rrbs=False
        red_site=list()
        red_site.append(options.red_site.upper())
        min_len_rrseq=options.min_len_rrseq
        max_len_rrseq=options.max_len_rrseq
        if options.rrbs:
	  rrbs=True
	  red_site=list()
	  red_site_info=[options.red_site.find('-'), len(options.red_site)-len(options.red_site[:options.red_site.find('-')])]
	  options.red_site=options.red_site.replace('-','')
	  red_site.append(options.red_site.upper())
	  red_site=resolve_dig_sites(red_site)
	  min_len_rrseq=check_red_site_length(min_len_rrseq)
	  max_len_rrseq=check_red_site_length(max_len_rrseq)
        
        soap3_path=options.soap3path
        soap3_path=str(soap3_path)
        if soap3_path[-1] !="/": soap3_path=soap3_path+"/"
        check_dir(soap3_path) # check if the path exists

    except IOError:
        print '[ERROR] File %s does not exist'%(fasta_file)
        exit()
    except DirectoryError, err:
        print '[ERROR] ', err
        exit()
    except REDSizeOptionTypeException:
	print 'Invalid values for -m / -M option(s)'
	exit()

    #------------------------------------------#
    #            Set logger                    #
    #------------------------------------------#

    log_file = indexes_path + 'log' + '.log' # log file
    logger = get_logger(log_file)
    
    #------------------------------------------#
    #            Start the job                 #
    #------------------------------------------#

    logger.info('Job started\n')
    logger.info('Reference genome file: %s'%(fasta_file))
    if rrbs: logger.info('Indexes will be build to handle RRBS data')
    else: logger.info('Indexes will be build to handle WGBS data') 
    logger.info('SOAP3-dp path: %s'%(soap3_path))
    logger.info('Indexes files will be stored in the %s directory\n'%(indexes_path))


    start_time = time.time()
    if rrbs: 
      fragments_info = open(indexes_path+FRAGMENTS_FNAME, 'w')
      logger.info('Fragments info will be stored in %s \n'%(indexes_path+FRAGMENTS_FNAME))
      fragments_info.write('#'.ljust(40)  + 'seq ID'.ljust(40)  + 'chr_fragment ID'.ljust(40) + 'start'.ljust(40) + 'end'.ljust(40)+'\n')
      reference = get_reference(fasta_file, indexes_path, logger, red_site, min_len_rrseq, max_len_rrseq, indexes_path, fragments_info, red_site_info, rrbs)
      fragments_info.close()
      
    else: 
      reference = get_reference(fasta_file, indexes_path, logger, red_site, min_len_rrseq, max_len_rrseq, indexes_path, None, None, rrbs)
    
    #------------------------------------------#
    #           Serialize ref sequences        #
    #------------------------------------------#
    serialize_data = open(indexes_path+REFERENCE_FNAME,'wb')
    marshal.dump(reference, serialize_data)
    serialize_data.close()
   
		      
    
    #------------------------------------------#
    #       C-to-T and G-to-A conversions      #
    #------------------------------------------#
    if not rrbs:
      logger.info('Cs to Ts conversion')
      conversion(indexes_path+'FW_C2T.fa', reference, 'C', 'T')
      logger.info('Gs to As conversion')
      conversion(indexes_path+'FW_G2A.fa', reference, 'G', 'A')
    else:
      logger.info('Cs to Ts conversion')
      conversion_rrbs(indexes_path+'FW_C2T.fa', reference, 'C', 'T', 'FW')
      logger.info('Gs to As conversion')
      conversion_rrbs(indexes_path+'FW_G2A.fa', reference, 'G', 'A', 'RC')

    #------------------------------------------#
    #       SOAP3-builder to build indexes     #
    #------------------------------------------#
    logger.info('Build the 2BWT indexes')
    index_1_C2T=Popen('nohup %ssoap3-dp-builder %sFW_C2T.fa > %sFW_C2T.log'%(soap3_path, indexes_path, indexes_path),shell=True)
    logger.info('GPU-BSM is building the (first) 2BWT index for the reference sequence with Cs converted to Ts')
    
    index_2_G2A=Popen('nohup %ssoap3-dp-builder %sFW_G2A.fa > %sFW_G2A.log'%(soap3_path, indexes_path, indexes_path),shell=True)
    logger.info('GPU-BSM is building the (second) 2BWT index for the reference sequence with Gs converted to As')
    
    index_1_C2T.wait()
    index_2_G2A.wait()
    
    logger.info('The indexes have been built')
    
    logger.info('Converting the 2BWT indexes to the GPU2-BWT indexes')

    GPU2_BWT_index1_C2T = Popen('nohup %sBGS-Build  %sFW_C2T.fa.index'%(soap3_path, indexes_path), shell=True)
    GPU2_BWT_index1_C2T.wait()
    logger.info('First index converted')
    GPU2_BWT_index2_G2A = Popen('nohup %sBGS-Build  %sFW_G2A.fa.index'%(soap3_path, indexes_path), shell=True)
    GPU2_BWT_index2_G2A.wait()
    logger.info('Second index converted')

    elapsed_time = (time.time() - start_time)
    logger.info('Job finished')
    logger.info('Elapsed Time: %s sec'%(elapsed_time));
    
