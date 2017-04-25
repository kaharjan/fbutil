#!/usr/bin/env python2.7
"""
Script to do statics in  Freebase 
"""
from collections import defaultdict
import logging
import gzip
logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

def read_mids_names(f):
    log.info('Reading mids,names..')
    mids = frozenset([m.strip().split("\t")[0] for m in gzip.open(f, 'rb').readlines()])
    log.info('...len of mids (%d).' % len(mids))
    names_dict={}
    for m in gzip.open(f,'rb').readlines():
	mid,name=m.strip().split('\t')
	names_dict[mid]=name	
    log.info('..len of name_dict (%d).' % len(names_dict))
    return mids,names_dict



def mid(s):
    s = s.strip('<>')
    if s.startswith('http://rdf.freebase.com/ns/m.'):
        return s[27:]
def cleanTriplet(s):
	s=s.strip('<>')
        if s.startswith('http://rdf.freebase.com/ns/m.'):
	    return s[27:]
	elif s.startswith('http://rdf.freebase.com/'):
	    return s[23:]
	elif s.startswith('http://'):
	    return s[7:]
 	return s


def sortAndWriteDict(targetDict,outfilename):
    with open(outfilename,'w') as f:
        for item in sorted(targetDict,key=targetDict.get,reverse=True):
            #f.write("%s"+"\t%d"+"\t."%(item,targetDict[item]))
	    line="{0}\t{1}\t.\n".format(item,targetDict[item])
	    f.write(line)		
def sortCleanAndWriteDict(targetDict,outfilename):
    with open(outfilename,'w') as f:
	for item in sorted(targetDict,key=targetDict.get,reverse=True):
	    line="{0}\t{1}\t.\n".format(cleanTriplet(item),targetDict[item],reverse=True)
	    f.write(line)    

def main(inputfile_name, outputfile_name):
   # sDict=defaultdict(int)	
   # pDict=defaultdict(int)
    oDict=defaultdict(int)
   # mid_set,name_dict = read_mids_names(midsf)
   # out_file = open(outputfile_name,'w')
    log.info('statistics about freebase relation ...')
    for i, line in enumerate(gzip.open(inputfile_name, 'rb')):
        if i % 1000000 == 0:
            log.info('..%d..' % i)
        fields = line.strip().split('\t')
        if len(fields) != 4:
            log.warn('Unexpected format: %s' % line)
        s, p, o, t = fields
    #    sDict[s]+=1
#	pDict[p]+=1
	oDict[o]+=1


    log.info('all line is %i\n ..done.'%i)
   # sortAndWriteDict(sDict,outputfile_name+".subj")
   # sortAndWriteDict(pDict,outputfile_name+".pred")
    sortAndWriteDict(oDict,outputfile_name+".objec")
   # sortCleanAndWriteDict(sDict,outputfile_name+".clean.subj")
  #  sortCleanAndWriteDict(pDict,outputfile_name+".clean.pred")
    sortCleanAndWriteDict(oDict,outputfile_name+".clean.objec")

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Do staticst freebase Subjects, Objects and Relations in Freebase')
    p.add_argument('inputname', help='Freebase RDF input file name')
    p.add_argument('outputname', help='Output file name')   
    args = p.parse_args()
    log.info('reading arg...')
    main(args.inputname, args.outputname)
   
